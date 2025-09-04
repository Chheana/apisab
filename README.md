# 🎯 JakLike SMM Web Dashboard

A modern web dashboard for managing your JakLike SMM Telegram bot. This dashboard provides a user-friendly interface to monitor users, orders, and bot statistics.

## ✨ Features

- **📊 Dashboard**: Real-time statistics and charts
- **👥 User Management**: View and manage all bot users
- **📦 Order Management**: Track and update order statuses
- **🔍 Search & Filter**: Find users and orders quickly
- **📱 Responsive Design**: Works on desktop and mobile
- **🎨 Modern UI**: Beautiful Bootstrap-based interface

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
python app.py
```

### 3. Access the Dashboard

Open your browser and go to: `http://localhost:5000`

### 4. Login

- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
JakLike/
├── app.py                 # Main Flask application
├── main.py               # Your existing Telegram bot
├── bot_data.db           # SQLite database
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard
│   ├── users.html       # Users management
│   └── orders.html      # Orders management
└── README.md            # This file
```

## 🔧 Configuration

### Database Connection

The dashboard automatically connects to your existing `bot_data.db` file. Make sure it's in the same directory as `app.py`.

### Admin Credentials

To change the default admin credentials, edit the `verify_user` function in `app.py`:

```python
def verify_user(username, password):
    # Replace with your own authentication logic
    if username == "your_username" and password == "your_password":
        return True
    return False
```

### Port Configuration

To change the port, modify the last line in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

## 📊 Dashboard Features

### Statistics Cards
- Total Users
- Total Balance
- Orders Today
- Growth Rate

### Charts
- **Weekly Statistics**: Line chart showing orders and top-ups over time
- **Service Distribution**: Pie chart showing service usage breakdown

### Recent Activity
- Latest orders with status indicators
- New user registrations
- Real-time updates

## 👥 User Management

### View Users
- Search by user ID or any text
- Filter by balance, orders, language
- View detailed user information

### Manage Funds
- Add funds to user accounts
- Remove funds with reason tracking
- View transaction history

## 📦 Order Management

### Track Orders
- View all orders with status
- Filter by status (pending, processing, completed, failed)
- Search orders by package or URL

### Update Status
- Change order status
- Add notes to status changes
- Track order progress

## 🔒 Security Features

- Session-based authentication
- CSRF protection
- Input validation
- Secure password handling

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔄 Integration with Bot

The dashboard connects to your existing bot database and provides:

1. **Real-time Data**: Live statistics from your bot
2. **User Management**: Manage bot users through the web interface
3. **Order Tracking**: Monitor and update order statuses
4. **Analytics**: Visual insights into bot performance

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure `bot_data.db` exists in the same directory
   - Check file permissions

2. **Port Already in Use**
   - Change the port in `app.py`
   - Kill existing processes using the port

3. **Template Errors**
   - Ensure all template files are in the `templates/` folder
   - Check for syntax errors in HTML files

### Logs

The application logs to the console. Check for error messages when starting the app.

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] User management API
- [ ] Order automation
- [ ] Payment integration
- [ ] Multi-language support
- [ ] Mobile app

## 📞 Support

If you encounter any issues:

1. Check the console logs for error messages
2. Verify your database file exists and is accessible
3. Ensure all dependencies are installed correctly
4. Check that the port isn't being used by another application

## 📄 License

This project is part of your JakLike SMM bot system.

---

**Happy managing! 🎉**




