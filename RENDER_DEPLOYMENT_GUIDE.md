# 🚀 JakLike Mini App - Render.com Deployment Guide

## ✨ What We've Fixed & Added

### ✅ **Fixed Issues:**
1. **AttributeError Fixed**: Converted `sqlite3.Row` objects to dictionaries to prevent errors
2. **Auto Telegram ID Detection**: Mini app now automatically detects user's Telegram ID
3. **Seamless Login**: No more manual Telegram ID entry needed

### 🆕 **New Features:**
1. **Telegram Web App Integration**: Automatic user detection from mini app context
2. **Smart Routing**: Serves appropriate template based on request type
3. **Fallback Support**: Manual login still available if needed

## 🌐 Deploy to Render.com

### Step 1: Prepare Your Code

Make sure you have these files ready:
- ✅ `user_app.py` (updated with fixes)
- ✅ `telegram_webapp.html` (new mini app template)
- ✅ `config.py` (your configuration)
- ✅ `requirements.txt` (dependencies)
- ✅ `bot_data.db` (your database)

### Step 2: Create Render Configuration

Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: jaklike-mini-app
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn user_app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: PORT
        value: 10000
```

### Step 3: Update Requirements

Ensure your `requirements.txt` includes:

```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
requests==2.31.0
gunicorn==21.2.0
```

### Step 4: Update Config for Production

Edit your `config.py`:

```python
# Configuration file for JakLike User Web App

# Admin Telegram IDs (add your admin users here)
ADMIN_IDS = [
    123456789,  # Replace with actual admin Telegram ID
    987654321,  # Replace with actual admin Telegram ID
]

# Database configuration
DB_FILE = "bot_data.db"

# SMM API Configuration
SMM_API_URL = "https://chhean-smm.net/api/v2"
SMM_API_KEY = "8bf8bc269ff40c0f472aff557505a485"

# App configuration
APP_NAME = "JakLike"
APP_VERSION = "1.0.0"
DEBUG_MODE = False  # Set to False for production
HOST = "0.0.0.0"
PORT = 10000  # Render uses port 10000

# Security settings
SECRET_KEY = None  # Will be auto-generated
SESSION_TIMEOUT = 3600

# Balance sync settings
AUTO_SYNC_INTERVAL = 30
BALANCE_UPDATE_ENABLED = True

# Features
ENABLE_ADMIN_CONTROLS = True
ENABLE_BALANCE_SYNC = True
ENABLE_TRANSACTION_HISTORY = True
```

### Step 5: Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment with mini app integration"
git push origin main
```

## 🚀 Deploy on Render.com

### Step 1: Create Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Verify your email

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository

### Step 3: Configure Service

**Basic Settings:**
- **Name**: `jaklike-mini-app`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn user_app:app --bind 0.0.0.0:$PORT`

**Environment Variables:**
- `PYTHON_VERSION`: `3.9.16`
- `PORT`: `10000`

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build (2-5 minutes)
3. Your app will be at: `https://jaklike-mini-app.onrender.com`

## 📱 Integrate with Your Bot

### Add Mini App Button

Add this to your `main.py` bot file:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def show_mini_app(update, context):
    """Show mini app button to users"""
    keyboard = [[InlineKeyboardButton(
        "🌐 Open JakLike Mini App", 
        web_app=WebAppInfo(url="https://jaklike-mini-app.onrender.com")
    )]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🎯 **JakLike Mini App**\n\n"
        "Access your account from anywhere! Click below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Add command handler
dispatcher.add_handler(CommandHandler("miniapp", show_mini_app))
```

### Add to Main Menu

```python
def main_menu(update, context):
    """Main menu with mini app option"""
    keyboard = [
        [InlineKeyboardButton("🌐 Mini App", callback_data="open_mini_app")],
        [InlineKeyboardButton("💰 Add Funds", callback_data="add_funds")],
        [InlineKeyboardButton("📦 Order Services", callback_data="order_services")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🎯 **JakLike Services**\nChoose an option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
```

## 🔧 Test Your Mini App

### Test Auto-Login
1. **Send `/miniapp`** to your bot
2. **Click the button** to open mini app
3. **Should auto-login** without asking for Telegram ID
4. **See your balance** and dashboard

### Test Manual Fallback
1. **Open mini app directly** in browser
2. **Should show manual login** if no Telegram context
3. **Enter Telegram ID** manually
4. **Access dashboard** normally

## 🌟 How It Works Now

### For Mini App Users:
1. **Click mini app button** in bot
2. **Automatically logged in** using Telegram context
3. **See real-time balance** synced from bot
4. **Access all features** seamlessly

### For Web Users:
1. **Visit URL directly** in browser
2. **Manual login** with Telegram ID
3. **Same experience** as mini app users
4. **Full functionality** available

## 🔒 Security Features

### Automatic Protection:
- ✅ **Session management** with timeouts
- ✅ **Admin-only functions** restricted
- ✅ **Database validation** for all requests
- ✅ **CSRF protection** built-in

### Mini App Security:
- ✅ **Telegram verification** of user identity
- ✅ **Secure session creation** after verification
- ✅ **Fallback authentication** for web users

## 📊 Monitor Your App

### Render Dashboard:
- **Logs**: Real-time application logs
- **Metrics**: Performance and usage stats
- **Uptime**: Service availability
- **Deployments**: Build and deployment history

### App Health Check:
- **Visit**: `https://jaklike-mini-app.onrender.com/api/status`
- **Check**: Feature status and configuration
- **Monitor**: Balance sync and admin controls

## 🆘 Troubleshooting

### Common Issues:

**Build Fails:**
```bash
# Check requirements.txt has all dependencies
# Verify Python version compatibility
# Ensure all files are committed to GitHub
```

**App Won't Start:**
```bash
# Verify start command: gunicorn user_app:app --bind 0.0.0.0:$PORT
# Check environment variables
# Review build logs for errors
```

**Mini App Not Working:**
```bash
# Verify URL in bot button matches deployed URL
# Check Telegram Web App integration
# Test manual login as fallback
```

**Database Issues:**
```bash
# Ensure bot_data.db is accessible
# Check file permissions
# Verify database path in config.py
```

## 🎯 Next Steps

### After Deployment:
1. **Test mini app** with your bot
2. **Share with users** via bot commands
3. **Monitor performance** and user feedback
4. **Set up custom domain** (optional)

### Future Enhancements:
- **Real-time notifications** via Telegram
- **Advanced analytics** dashboard
- **Multi-language support** for web interface
- **Payment integration** directly in web app

---

## 🎉 You're All Set!

Your JakLike Mini App is now:
- ✅ **Deployed on Render.com**
- ✅ **Integrated with your bot**
- ✅ **Auto-login working**
- ✅ **All errors fixed**
- ✅ **Ready for users!**

**Users can now:**
1. **Click mini app button** in your bot
2. **Get instant access** to their account
3. **Check balance** in real-time
4. **Manage orders** from anywhere
5. **Enjoy mobile-friendly** interface

**No more manual login needed!** 🚀

---

**Need help?** Check the troubleshooting section or let me know if you encounter any issues!




