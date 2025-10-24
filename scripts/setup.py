#!/usr/bin/env python3
"""
Interactive setup script for Telegram Userbot
Run this in the Shell to authenticate and generate your session string.
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

def main():
    print("\n" + "="*70)
    print(" Telegram Userbot - Authentication Setup")
    print("="*70)
    
    # Get API credentials
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    
    if not api_id or not api_hash:
        print("\n❌ ERROR: API_ID and API_HASH are not set!")
        print("\nPlease add them to Replit Secrets:")
        print("  1. Click the lock icon (Secrets) in the left sidebar")
        print("  2. Add API_ID with your API ID from my.telegram.org")
        print("  3. Add API_HASH with your API hash from my.telegram.org")
        print("\n")
        return
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("\n❌ ERROR: API_ID must be a number!")
        return
    
    print("\n✅ API credentials found!")
    print(f"   API_ID: {api_id}")
    print(f"   API_HASH: {api_hash[:8]}...")
    print("\n" + "-"*70)
    print("This script will help you authenticate with Telegram.")
    print("You'll need:")
    print("  • Your phone number (with country code, e.g., +1234567890)")
    print("  • Access to your Telegram account to receive a code")
    print("  • Your 2FA password (if you have it enabled)")
    print("-"*70)
    
    input("\nPress ENTER to continue...")
    
    # Run async authentication
    asyncio.run(authenticate(api_id, api_hash))

async def authenticate(api_id, api_hash):
    print("\n🔐 Starting authentication process...\n")
    
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    try:
        await client.start()
        
        me = await client.get_me()
        
        print("\n" + "="*70)
        print("✅ SUCCESS! You are now authenticated!")
        print("="*70)
        print(f"\n👤 Logged in as: {me.first_name}")
        if me.username:
            print(f"   Username: @{me.username}")
        print(f"   Phone: {me.phone}")
        
        # Get session string
        session_string = client.session.save()
        
        print("\n" + "="*70)
        print("🔑 YOUR SESSION STRING:")
        print("="*70)
        print("\n" + session_string + "\n")
        print("="*70)
        
        print("\n📋 NEXT STEPS:")
        print("-"*70)
        print("1. Copy the session string above (the long text)")
        print("2. Go to Replit Secrets (lock icon in left sidebar)")
        print("3. Find 'SESSION_SECRET' and paste the session string there")
        print("4. The bot will automatically restart and start working!")
        print("-"*70)
        
        print("\n💡 TIP: Keep this session string secure!")
        print("   It's like a password for your Telegram account.\n")
        
        await client.disconnect()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease try again and make sure:")
        print("  • You enter your phone number correctly (+countrycode)")
        print("  • You enter the verification code from Telegram")
        print("  • Your 2FA password is correct (if enabled)")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
