import os
import asyncio
from flask import Flask, render_template, request, jsonify, redirect, url_for
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from dotenv import load_dotenv, set_key
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for authentication state
auth_session = None
auth_phone = None
auth_phone_code_hash = None

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_SECRET = os.getenv('SESSION_SECRET', '')

if not API_ID or not API_HASH:
    logger.warning("API_ID and API_HASH not configured")

try:
    API_ID = int(API_ID) if API_ID else None
except ValueError:
    API_ID = None

def run_async(coro):
    """Run async function in a thread-safe way by creating a new event loop"""
    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as pool:
        future = pool.submit(run_in_new_loop)
        return future.result()

@app.route('/')
def index():
    """Main page - check if bot is configured"""
    session_configured = SESSION_SECRET and len(SESSION_SECRET) > 50
    api_configured = API_ID and API_HASH
    
    # If API not configured, redirect to config page
    if not api_configured:
        return redirect(url_for('config'))
    
    return render_template('index.html', 
                         session_configured=session_configured,
                         api_configured=api_configured)

@app.route('/config')
def config():
    """Configuration page for API credentials"""
    return render_template('config.html', api_id=os.getenv('API_ID', ''), api_hash=os.getenv('API_HASH', ''))

@app.route('/api/save-config', methods=['POST'])
def save_config():
    """Save API credentials to .env file"""
    try:
        data = request.json
        api_id = data.get('api_id', '').strip()
        api_hash = data.get('api_hash', '').strip()
        
        if not api_id or not api_hash:
            return jsonify({'success': False, 'error': 'Both API ID and API Hash are required'})
        
        # Validate API_ID is numeric
        try:
            int(api_id)
        except ValueError:
            return jsonify({'success': False, 'error': 'API ID must be a number'})
        
        # Create .env file if it doesn't exist
        env_file = '.env'
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f:
                f.write('# Telegram Bot Configuration\n')
        
        # Save to .env file
        set_key(env_file, 'API_ID', api_id)
        set_key(env_file, 'API_HASH', api_hash)
        
        # Update global variables
        global API_ID, API_HASH
        API_ID = int(api_id)
        API_HASH = api_hash
        
        logger.info("API credentials saved successfully")
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/setup')
def setup():
    """Setup page for authentication"""
    if not API_ID or not API_HASH:
        return render_template('error.html', 
                             error="API_ID and API_HASH not configured",
                             message="Please configure your API credentials first.")
    return render_template('setup.html')

@app.route('/api/send-code', methods=['POST'])
def send_code():
    """Send verification code to phone number"""
    global auth_client, auth_phone, auth_phone_code_hash
    
    try:
        data = request.json
        phone = data.get('phone')
        
        if not phone:
            return jsonify({'success': False, 'error': 'Phone number is required'})
        
        if not API_ID or not API_HASH:
            return jsonify({'success': False, 'error': 'API credentials not configured'})
        
        async def send():
            global auth_session, auth_phone_code_hash
            # Create client inside async context
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            result = await client.send_code_request(phone)
            auth_phone_code_hash = result.phone_code_hash
            # Save session string for later use
            auth_session = client.session.save()
            await client.disconnect()
            return True
        
        run_async(send())
        auth_phone = phone
        
        return jsonify({'success': True, 'message': 'Verification code sent to your Telegram!'})
    
    except Exception as e:
        logger.error(f"Error sending code: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    """Verify the code and complete authentication"""
    global auth_session, auth_phone, auth_phone_code_hash
    
    try:
        data = request.json
        code = data.get('code')
        password = data.get('password', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'Verification code is required'})
        
        if not auth_session or not auth_phone:
            return jsonify({'success': False, 'error': 'Please send code first'})
        
        async def verify():
            # Recreate client with saved session in this event loop
            client = TelegramClient(StringSession(auth_session), API_ID, API_HASH)
            await client.connect()
            
            try:
                # Try to sign in with the code
                await client.sign_in(auth_phone, code, phone_code_hash=auth_phone_code_hash)
            except SessionPasswordNeededError:
                # 2FA is enabled, need password
                if not password:
                    await client.disconnect()
                    return {'needs_password': True}
                await client.sign_in(password=password)
            except PhoneCodeInvalidError:
                await client.disconnect()
                return {'error': 'Invalid verification code'}
            
            # Get user info
            me = await client.get_me()
            
            # Get session string
            session_string = client.session.save()
            
            await client.disconnect()
            
            return {
                'success': True,
                'user': {
                    'name': me.first_name,
                    'username': me.username,
                    'phone': me.phone
                },
                'session': session_string
            }
        
        result = run_async(verify())
        
        if result.get('needs_password'):
            return jsonify({'success': False, 'needs_password': True, 
                          'error': '2FA is enabled. Please enter your password.'})
        
        if result.get('error'):
            return jsonify({'success': False, 'error': result['error']})
        
        if result.get('success') and result.get('session'):
            env_file = '.env'
            if not os.path.exists(env_file):
                with open(env_file, 'w') as f:
                    f.write('# Telegram Bot Configuration\n')
            
            set_key(env_file, 'SESSION_SECRET', result['session'])
            logger.info("Session string automatically saved to .env file")
            
            global SESSION_SECRET
            SESSION_SECRET = result['session']
        
        return jsonify(result)
    
    except PhoneCodeInvalidError:
        return jsonify({'success': False, 'error': 'Invalid verification code. Please try again.'})
    except Exception as e:
        logger.error(f"Error verifying code: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/bot')
def bot_page():
    """Bot control page"""
    session_configured = SESSION_SECRET and len(SESSION_SECRET) > 50
    
    if not session_configured:
        return redirect(url_for('setup'))
    
    return render_template('bot.html')

@app.route('/settings')
def settings():
    """Settings page"""
    base_name = os.getenv('BASE_NAME', 'Hashir')
    auto_reply = os.getenv('AUTO_REPLY_MESSAGE', "I'll respond when I get online")
    
    return render_template('settings.html', base_name=base_name, auto_reply=auto_reply)

@app.route('/api/save-settings', methods=['POST'])
def save_settings():
    """Save bot settings to .env file"""
    try:
        data = request.json
        base_name = data.get('base_name', '').strip()
        auto_reply = data.get('auto_reply', '').strip()
        
        if not base_name:
            return jsonify({'success': False, 'error': 'Base name is required'})
        
        if not auto_reply:
            return jsonify({'success': False, 'error': 'Auto-reply message is required'})
        
        env_file = '.env'
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f:
                f.write('# Telegram Bot Configuration\n')
        
        set_key(env_file, 'BASE_NAME', base_name)
        set_key(env_file, 'AUTO_REPLY_MESSAGE', auto_reply)
        
        os.environ['BASE_NAME'] = base_name
        os.environ['AUTO_REPLY_MESSAGE'] = auto_reply
        
        logger.info(f"Settings saved: BASE_NAME={base_name}, AUTO_REPLY_MESSAGE={auto_reply}")
        return jsonify({'success': True, 'message': 'Settings saved! The bot will restart automatically.'})
    
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/docs')
def docs():
    """Documentation page"""
    return render_template('docs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
