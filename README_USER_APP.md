# 🎯 JakLike User Web App

A mobile-first web interface that allows all users to access their JakLike SMM bot functionality through a beautiful web dashboard, just like the reference image you showed!

## ✨ Features

- **📱 Mobile-First Design**: Optimized for mobile devices with responsive design
- **🔐 User Authentication**: Login with Telegram ID (same as bot)
- **💰 Real-Time Balance Sync**: Funds added in bot appear instantly in web app
- **📊 Dashboard**: Overview of your account and quick actions
- **📦 Order History**: View all your SMM service orders
- **👤 Profile Management**: Account settings and statistics
- **🌐 Web Access**: Use your SMM services anywhere, not just in Telegram
- **👑 Admin Controls**: Special features for admin users only

## 🚀 Quick Start

### 1. Setup Admin Configuration

```bash
# Run the setup script to configure admin users
python setup_admin.py
```

**Follow the prompts to:**
- Add admin Telegram IDs (users who can check API balance)
- Verify your bot database is accessible
- Create the configuration file

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the User Web App

```bash
python user_app.py
```

### 4. Access the Web App

Open your browser and go to: `http://localhost:5001`

### 5. Login with Your Telegram ID

- Get your Telegram ID from the bot by sending `/start`
- Use that ID to login to the web app
- Access all your bot functionality through the web interface!

## 🔄 Fund Synchronization

### How It Works:
1. **Real-Time Sync**: When users add funds in the bot, they appear instantly in the web app
2. **Automatic Updates**: Balance refreshes every 30 seconds automatically
3. **Database Connection**: Web app reads directly from your bot's database
4. **No Manual Updates**: Everything stays in sync automatically

### For Users:
- Add funds through the bot (Telegram Stars, Bakong QR, etc.)
- See updated balance immediately in the web app
- Check transaction history and spending details
- Monitor account activity from anywhere

## 👑 Admin Features

### Admin-Only Functions:
- **API Balance Checking**: Check SMM provider balance
- **System Status**: View app configuration and features
- **Enhanced Controls**: Access to admin-only sections

### How to Set Admin Users:
1. Run `python setup_admin.py`
2. Enter the Telegram IDs of users who should have admin access
3. Save the configuration
4. Admin users will see special controls when they login

## 📱 How It Works

### For Users:
1. **Login**: Enter your Telegram ID (the same one you use with the bot)
2. **Dashboard**: See your balance, stats, and quick actions
3. **Balance**: Check your SMM provider balance and transaction history
4. **Orders**: View all your service orders and their status
5. **Profile**: Manage your account settings and view statistics

### For Bot Owners:
- Users can now access your SMM services through a web interface
- Reduces dependency on Telegram for basic operations
- Better user experience for balance checking and order tracking
- Mobile-friendly design works on all devices
- **Funds sync automatically** between bot and web app

## 🌐 Hosting Options

### Option 1: Local Development (Testing)
```bash
python user_app.py
# Access at http://localhost:5001
```

### Option 2: Free Hosting (Recommended)

#### A. Render.com (Free Tier)
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Deploy as a Web Service
4. Your app will be available at: `https://your-app-name.onrender.com`

#### B. Railway.app (Free Tier)
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically
4. Get a public URL like: `https://your-app-name.railway.app`

#### C. Heroku (Free Tier Discontinued)
- Consider paid plans or alternatives

### Option 3: VPS Hosting
```bash
# Install on Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx
pip3 install -r requirements.txt

# Run with Gunicorn
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 user_app:app

# Configure Nginx as reverse proxy
```

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Create .env file
FLASK_SECRET_KEY=your_secret_key_here
SMM_API_URL=https://chhean-smm.net/api/v2
SMM_API_KEY=your_api_key_here
```

### Database
- Uses your existing `bot_data.db` file
- No additional setup required
- Automatically connects to your bot's database
- **Real-time synchronization** with bot data

### Admin Configuration
```python
# In config.py
ADMIN_IDS = [123456789, 987654321]  # Add your admin Telegram IDs here
```

## 📱 Mobile App Feel

The web app is designed to feel like a native mobile app:

- **Bottom Navigation**: Easy access to all sections
- **Card-based Design**: Clean, modern interface
- **Touch-friendly**: Large buttons and smooth interactions
- **Responsive**: Works perfectly on all screen sizes
- **Fast Loading**: Optimized for mobile networks
- **Real-time Updates**: Balance and data stay current

## 🔒 Security Features

- **Session Management**: Secure user sessions with timeout
- **Telegram ID Verification**: Only registered bot users can access
- **Admin Controls**: Restricted access to sensitive functions
- **CSRF Protection**: Built-in Flask security
- **Secure Headers**: Production-ready security headers

## 🚀 Deployment Checklist

### Before Deploying:
- [ ] Run `python setup_admin.py` to configure admins
- [ ] Test locally with `python user_app.py`
- [ ] Verify database connection
- [ ] Check all templates render correctly
- [ ] Test user login flow
- [ ] Verify API endpoints work
- [ ] Test admin functions with admin user

### After Deploying:
- [ ] Test on mobile devices
- [ ] Verify HTTPS works (if applicable)
- [ ] Check performance on slow connections
- [ ] Monitor error logs
- [ ] Test user registration flow
- [ ] Verify fund synchronization works

## 🎨 Customization

### Colors and Branding
Edit the CSS variables in each template:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #007bff;
}
```

### Logo and Branding
Replace the JakLike branding with your own:
- Update titles and headers
- Change the color scheme
- Add your logo
- Customize the welcome messages

### Admin Controls
Customize what admin users can access:
```python
# In config.py
ENABLE_ADMIN_CONTROLS = True
ENABLE_BALANCE_SYNC = True
ENABLE_TRANSACTION_HISTORY = True
```

## 📊 Analytics and Monitoring

### Built-in Features:
- User session tracking
- Page view logging
- Error monitoring
- Performance metrics
- Balance synchronization logs

### Add External Analytics:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>

<!-- Facebook Pixel -->
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>
```

## 🆘 Support and Troubleshooting

### Common Issues:

1. **Port Already in Use**
   ```bash
   # Change port in config.py
   PORT = 5002
   ```

2. **Database Connection Error**
   - Ensure `bot_data.db` exists in the same directory
   - Check file permissions
   - Verify database is not locked by bot

3. **Template Errors**
   - Verify all template files are in `templates/` folder
   - Check for syntax errors in HTML

4. **Login Issues**
   - Verify user exists in database
   - Check Telegram ID format
   - Ensure bot database is accessible

5. **Admin Functions Not Working**
   - Run `python setup_admin.py` to configure admin IDs
   - Check `config.py` file exists
   - Verify admin Telegram IDs are correct

6. **Balance Not Syncing**
   - Check database connection
   - Verify `ENABLE_BALANCE_SYNC = True` in config
   - Check bot database for recent balance updates

### Getting Help:
- Check the Flask error logs
- Verify all dependencies are installed
- Test with a simple user account first
- Run the setup script to reconfigure

## 🎯 Next Steps

### Immediate:
1. Run `python setup_admin.py` to configure admins
2. Test the web app locally
3. Deploy to a free hosting service
4. Share the URL with your users

### Future Enhancements:
- Add real-time order updates
- Implement push notifications
- Add more payment methods
- Create admin dashboard
- Add user registration through web
- Implement referral system
- Add transaction webhooks

## 🌟 Success Metrics

Track these to measure success:
- **User Adoption**: How many users use the web app
- **Session Duration**: Time spent on web vs bot
- **Feature Usage**: Which pages are most visited
- **User Satisfaction**: Feedback and ratings
- **Conversion Rate**: Web users who place orders
- **Balance Sync Success**: How often funds sync correctly

## 🔄 Fund Sync Testing

### Test Fund Synchronization:
1. **Add funds in bot**: Use Telegram Stars or other payment methods
2. **Check web app**: Balance should update within 30 seconds
3. **Verify accuracy**: Web app balance should match bot balance
4. **Test transactions**: Order services and verify balance decreases

### Monitor Sync Status:
```bash
# Check app status
curl http://localhost:5001/api/status

# Check user balance
curl http://localhost:5001/api/user_balance
```

---

**🎉 Congratulations!** You now have a professional web interface for your SMM bot that all users can access. This gives your users the flexibility to use your services anywhere, anytime, while maintaining the same functionality they love from the Telegram bot.

**💰 Key Benefits:**
- **Real-time fund synchronization** between bot and web app
- **Admin-only balance checking** for security
- **Mobile-first design** that matches your reference images
- **Automatic updates** every 30 seconds
- **Secure user authentication** with Telegram IDs

**Need help?** Check the troubleshooting section or run `python setup_admin.py` to reconfigure!
