#!/usr/bin/env python3
"""
Setup script for JakLike User Web App
This script helps you configure admin IDs and other settings
"""

import os
import json

def get_telegram_id_instructions():
    print("\n" + "="*60)
    print("📱 HOW TO GET YOUR TELEGRAM ID")
    print("="*60)
    print("1. Open Telegram and search for @userinfobot")
    print("2. Send /start to the bot")
    print("3. The bot will reply with your Telegram ID")
    print("4. Copy that number (it looks like: 123456789)")
    print("5. Use it in the setup below")
    print("="*60 + "\n")

def setup_admin_ids():
    print("👑 ADMIN SETUP")
    print("Enter the Telegram IDs of users who should have admin access.")
    print("Leave empty when done adding admins.\n")
    
    admin_ids = []
    
    while True:
        admin_id = input(f"Enter admin Telegram ID #{len(admin_ids) + 1} (or press Enter to finish): ").strip()
        
        if not admin_id:
            break
            
        try:
            admin_id = int(admin_id)
            if admin_id > 0:
                admin_ids.append(admin_id)
                print(f"✅ Added admin ID: {admin_id}")
            else:
                print("❌ Invalid ID. Please enter a positive number.")
        except ValueError:
            print("❌ Invalid ID. Please enter a number.")
    
    return admin_ids

def setup_database():
    print("\n🗄️  DATABASE SETUP")
    print("Make sure your bot_data.db file is in the same directory as this script.")
    
    if os.path.exists("bot_data.db"):
        print("✅ Found bot_data.db")
        return True
    else:
        print("❌ bot_data.db not found!")
        print("Please ensure your bot database file is in the same directory.")
        return False

def create_config_file(admin_ids, db_exists):
    config_content = f'''# Configuration file for JakLike User Web App

# Admin Telegram IDs (users with admin access)
ADMIN_IDS = {admin_ids}

# Database configuration
DB_FILE = "bot_data.db"

# SMM API Configuration (update these with your actual API details)
SMM_API_URL = "https://chhean-smm.net/api/v2"
SMM_API_KEY = "8bf8bc269ff40c0f472aff557505a485"

# App configuration
APP_NAME = "JakLike"
APP_VERSION = "1.0.0"
DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5001

# Security settings
SECRET_KEY = None  # Will be auto-generated if None
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Balance sync settings
AUTO_SYNC_INTERVAL = 30  # seconds
BALANCE_UPDATE_ENABLED = True

# Features
ENABLE_ADMIN_CONTROLS = True
ENABLE_BALANCE_SYNC = True
ENABLE_TRANSACTION_HISTORY = True
'''
    
    try:
        with open("config.py", "w") as f:
            f.write(config_content)
        print("✅ Created config.py successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create config.py: {e}")
        return False

def show_next_steps():
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("Next steps:")
    print("1. ✅ Install dependencies: pip install -r requirements.txt")
    print("2. ✅ Run the web app: python user_app.py")
    print("3. ✅ Open your browser: http://localhost:5001")
    print("4. ✅ Login with any Telegram ID from your bot database")
    print("\n📱 Your users can now:")
    print("   • Access their bot balance through the web")
    print("   • View their order history")
    print("   • Check transaction details")
    print("   • Use the mobile-friendly interface")
    print("\n👑 Admin users can:")
    print("   • Check SMM provider API balance")
    print("   • Access admin-only features")
    print("="*60)

def main():
    print("🚀 JakLike User Web App Setup")
    print("="*40)
    
    # Check database
    db_exists = setup_database()
    if not db_exists:
        print("\n❌ Please fix the database issue and run this script again.")
        return
    
    # Get admin IDs
    get_telegram_id_instructions()
    admin_ids = setup_admin_ids()
    
    if not admin_ids:
        print("⚠️  No admin IDs provided. Only basic user features will be available.")
        admin_ids = []
    
    # Create config file
    if create_config_file(admin_ids, db_exists):
        show_next_steps()
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()




