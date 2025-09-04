#!/usr/bin/env python3
"""
JakLike - Combined Launcher
Runs both Telegram bot and Mini App simultaneously
"""

import subprocess
import sys
import time
import os
from threading import Thread

def run_bot():
    """Run the Telegram bot"""
    print("🤖 Starting Telegram Bot...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🤖 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

def run_mini_app():
    """Run the Mini App"""
    print("📱 Starting Mini App...")
    try:
        subprocess.run([sys.executable, "user_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n📱 Mini App stopped by user")
    except Exception as e:
        print(f"❌ Mini App error: {e}")

def main():
    print("🚀 JakLike - Starting Both Services...")
    print("=" * 50)
    
    # Check if required files exist
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        return
    
    if not os.path.exists("user_app.py"):
        print("❌ Error: user_app.py not found!")
        return
    
    if not os.path.exists("bot_data.db"):
        print("⚠️  Warning: bot_data.db not found. Run setup_database.py first!")
        print("   python setup_database.py")
        print()
    
    print("📋 Services to start:")
    print("   🤖 Telegram Bot (main.py)")
    print("   📱 Mini App (user_app.py)")
    print()
    print("💡 Press Ctrl+C in this window to stop both services")
    print("=" * 50)
    
    # Start both services in separate threads
    bot_thread = Thread(target=run_bot, daemon=True)
    app_thread = Thread(target=run_mini_app, daemon=True)
    
    try:
        bot_thread.start()
        time.sleep(2)  # Give bot time to start
        
        app_thread.start()
        time.sleep(2)  # Give app time to start
        
        print("✅ Both services started successfully!")
        print()
        print("🌐 Mini App: http://localhost:5000")
        print("🤖 Bot: Running in background")
        print()
        print("⏳ Keep this window open to run both services...")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping both services...")
        print("✅ Services stopped successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()




