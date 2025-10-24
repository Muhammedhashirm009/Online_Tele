import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserStatusRecently
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_SECRET = os.getenv('SESSION_SECRET', '')

if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in environment variables")

try:
    API_ID = int(API_ID)
except ValueError:
    raise ValueError("API_ID must be a valid integer")

BASE_NAME = os.getenv('BASE_NAME', 'Hashir')
AUTO_REPLY_MESSAGE = os.getenv('AUTO_REPLY_MESSAGE', "I'll respond when I get online")

replied_users = set()
current_status = None
is_running = True

try:
    if not SESSION_SECRET or SESSION_SECRET.strip() == '':
        raise ValueError("Empty session string")
    client = TelegramClient(StringSession(SESSION_SECRET), API_ID, API_HASH)
except (ValueError, Exception) as e:
    logger.error("=" * 60)
    logger.error("SESSION_SECRET is missing or invalid!")
    logger.error("=" * 60)
    logger.error("")
    logger.error("To set up your bot, please follow these steps:")
    logger.error("1. Open the Shell tab in Replit")
    logger.error("2. Run the command: python auth.py")
    logger.error("3. Follow the prompts to enter your phone number and verification code")
    logger.error("4. Copy the generated SESSION_SECRET")
    logger.error("5. Add it to your Replit Secrets")
    logger.error("")
    logger.error("=" * 60)
    raise ValueError("SESSION_SECRET is required. Please run auth.py in the Shell to generate it.") from e

async def update_name(status):
    global current_status, replied_users
    
    if status == current_status:
        return
    
    try:
        if status == 'online':
            new_name = f"{BASE_NAME} ( Online )"
            replied_users.clear()
            logger.info("Cleared auto-reply list - back online")
        else:
            new_name = f"{BASE_NAME} ( Offline )"
        
        await client(UpdateProfileRequest(
            first_name=new_name
        ))
        current_status = status
        logger.info(f"Updated name to: {new_name}")
    except Exception as e:
        logger.error(f"Error updating name: {e}")

async def check_status():
    while is_running:
        try:
            me = await client.get_me()
            if me.status:
                if isinstance(me.status, UserStatusOnline):
                    await update_name('online')
                elif isinstance(me.status, (UserStatusOffline, UserStatusRecently)):
                    await update_name('offline')
        except Exception as e:
            logger.error(f"Error checking status: {e}")
        
        await asyncio.sleep(30)

@client.on(events.NewMessage(outgoing=True))
async def handle_own_message(event):
    global replied_users
    replied_users.clear()
    logger.info("Detected outgoing message - clearing auto-reply list")

@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
    if event.is_private and current_status == 'offline':
        user_id = event.sender_id
        
        if user_id not in replied_users:
            try:
                await event.respond(AUTO_REPLY_MESSAGE)
                replied_users.add(user_id)
                logger.info(f"Sent auto-reply to user {user_id}")
            except Exception as e:
                logger.error(f"Error sending auto-reply: {e}")

async def main():
    logger.info("Starting Telegram Userbot...")
    
    await client.start()
    logger.info("Client started successfully!")
    
    me = await client.get_me()
    logger.info(f"Logged in as: {me.first_name} (@{me.username})")
    
    asyncio.create_task(check_status())
    
    logger.info("Bot is now running. Press Ctrl+C to stop.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        is_running = False
    except Exception as e:
        logger.error(f"Fatal error: {e}")
