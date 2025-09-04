# 🚀 **JakLike: Run Bot + Mini App Simultaneously**

## ✨ **Quick Start (Choose One Method)**

### **Method 1: Double-Click Batch File (Easiest)**
1. **Double-click** `run_both.bat`
2. **Two new windows** will open automatically
3. **Done!** Both services are running

### **Method 2: Python Script**
```bash
python run_both.py
```

### **Method 3: Manual (Separate Terminals)**
```bash
# Terminal 1 - Bot
python main.py

# Terminal 2 - Mini App  
python user_app.py
```

---

## 🔧 **Setup Requirements**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Setup Database**
```bash
python setup_database.py
```

### **3. Configure Admin (First Time Only)**
```bash
python setup_admin.py
```

---

## 📱 **What You Get**

### **🤖 Telegram Bot**
- **File:** `main.py`
- **Port:** None (Telegram API)
- **Status:** Running in background
- **Features:** SMM services, payments, user management

### **📱 Mini App**
- **File:** `user_app.py`
- **Port:** `http://localhost:5000`
- **Status:** Web interface accessible
- **Features:** User dashboard, service ordering, balance sync

---

## 🌐 **Access Points**

### **Bot Users:**
- **Telegram:** Send `/start` to your bot
- **Commands:** `/balance`, `/services`, `/order`

### **Mini App Users:**
- **Web:** `http://localhost:5000`
- **Auto-login:** Telegram ID detected automatically
- **Features:** Same services, same pricing as bot

---

## 🔄 **How They Work Together**

### **Shared Database:**
- **File:** `bot_data.db`
- **Tables:** `users`, `services`, `orders`
- **Sync:** Real-time balance and order updates

### **Data Flow:**
```
User adds funds in Bot → Mini App balance updates automatically
User orders in Mini App → Bot can see the order
User checks balance in Bot → Same balance shows in Mini App
```

---

## 🚨 **Troubleshooting**

### **Port 5000 Already in Use:**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace XXXX with PID)
taskkill /PID XXXX /F
```

### **Database Errors:**
```bash
# Recreate database
python setup_database.py
```

### **Bot Not Responding:**
- Check if `main.py` is running
- Verify bot token in `config.py`
- Check internet connection

### **Mini App Not Loading:**
- Check if `user_app.py` is running
- Verify `http://localhost:5000` is accessible
- Check browser console for errors

---

## 📊 **Monitoring Both Services**

### **Bot Status:**
- Look for "Bot started successfully" message
- Check for user interaction logs
- Monitor error messages

### **Mini App Status:**
- Visit `http://localhost:5000`
- Check if login works
- Test service ordering

### **Database Status:**
- Check if `bot_data.db` file exists
- Verify tables are created
- Monitor file size growth

---

## 🔐 **Security Notes**

### **Local Development:**
- Services run on `localhost` only
- No external access by default
- Database file is local

### **Production Deployment:**
- Use `gunicorn` for mini app
- Configure proper firewall rules
- Use HTTPS in production

---

## 📝 **File Structure**
```
JakLike/
├── main.py              # Telegram Bot
├── user_app.py          # Mini App
├── run_both.py          # Python launcher
├── run_both.bat         # Windows launcher
├── bot_data.db          # Shared database
├── config.py            # Configuration
├── setup_database.py    # Database setup
├── setup_admin.py       # Admin setup
└── requirements.txt     # Dependencies
```

---

## 🎯 **Success Indicators**

### **✅ Bot Working:**
- Responds to `/start` command
- Shows available services
- Processes orders

### **✅ Mini App Working:**
- Loads at `http://localhost:5000`
- Auto-detects Telegram ID
- Shows services and balance
- Allows ordering

### **✅ Both Synced:**
- Same balance in bot and app
- Orders appear in both places
- Database updates in real-time

---

## 🚀 **Next Steps**

1. **Test Both Services:**
   - Send `/start` to bot
   - Visit mini app in browser
   - Try ordering a service

2. **Add Mini App to Bot:**
   - Use `bot_integration_example.py`
   - Add "Open Mini App" button

3. **Deploy to Production:**
   - Follow `RENDER_DEPLOYMENT_GUIDE.md`
   - Configure domain and SSL

---

**🎉 You now have both services running simultaneously!**

**Users can interact with your SMM services through either the bot or the mini app, with perfect synchronization between both platforms.**




