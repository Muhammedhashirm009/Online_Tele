import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

if not API_ID or not API_HASH:
    print("ERROR: API_ID and API_HASH must be set in environment variables")
    print("Please make sure you have provided your Telegram API credentials.")
    exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    print("ERROR: API_ID must be a valid integer")
    exit(1)

async def main():
    print("=" * 60)
    print("Telegram Userbot - First Time Setup")
    print("=" * 60)
    print()
    print("This script will help you authenticate your Telegram account")
    print("and generate a session string for deployment.")
    print()
    
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    await client.start()
    
    me = await client.get_me()
    print()
    print("=" * 60)
    print(f"Successfully logged in as: {me.first_name}")
    if me.username:
        print(f"Username: @{me.username}")
    print("=" * 60)
    print()
    
    session_string = client.session.save()
    
    print("Your SESSION_SECRET:")
    print()
    print("-" * 60)
    print(session_string)
    print("-" * 60)
    print()
    print("IMPORTANT: Save this session string securely!")
    print()
    print("Next steps:")
    print("1. Copy the session string above")
    print("2. Add it to your Replit Secrets as 'SESSION_SECRET'")
    print("   OR add it to your .env file: SESSION_SECRET=<your_session_string>")
    print("3. For Koyeb: Add it as an environment variable")
    print()
    print("Once added, you can run main.py and the bot will start automatically!")
    print()
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
