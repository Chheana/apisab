from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import sqlite3
import os
from datetime import datetime, timedelta
import hashlib
import secrets
import requests
import json

# Import configuration
try:
    from config import *
except ImportError:
    # Default configuration if config.py doesn't exist
    ADMIN_IDS = [123456789, 987654321]
    DB_FILE = "bot_data.db"
    SMM_API_URL = "https://chhean-smm.net/api/v2"
    SMM_API_KEY = "8bf8bc269ff40c0f472aff557505a485"
    DEBUG_MODE = True
    HOST = "0.0.0.0"
    PORT = 5001
    SECRET_KEY = None
    SESSION_TIMEOUT = 3600
    AUTO_SYNC_INTERVAL = 30
    BALANCE_UPDATE_ENABLED = True
    ENABLE_ADMIN_CONTROLS = True
    ENABLE_BALANCE_SYNC = True
    ENABLE_TRANSACTION_HISTORY = True

app = Flask(__name__)
app.secret_key = SECRET_KEY if SECRET_KEY else secrets.token_hex(16)

# Set session timeout
app.permanent_session_lifetime = timedelta(seconds=SESSION_TIMEOUT)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_telegram_id(telegram_id):
    """Get user from database by Telegram ID"""
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (telegram_id,)).fetchone()
        if user:
            # Convert sqlite3.Row to dict to avoid AttributeError
            return dict(user)
        return None
    finally:
        conn.close()

def is_admin(telegram_id):
    """Check if user is admin using config"""
    return telegram_id in ADMIN_IDS

def get_user_balance_with_sync(telegram_id):
    """Get user balance and sync with latest bot data"""
    if not ENABLE_BALANCE_SYNC:
        # Return basic user info if balance sync is disabled
        user = get_user_by_telegram_id(telegram_id)
        if user:
            return {
                'user_id': user['user_id'],
                'balance': user.get('balance', 0.0),
                'username': user.get('username', 'N/A'),
                'language': user.get('language', 'en'),
                'registration_date': user.get('registration_date'),
                'last_activity': user.get('last_activity'),
                'total_orders': user.get('total_orders', 0),
                'total_spent': user.get('total_spent', 0.0)
            }
        return None
    
    conn = get_db_connection()
    try:
        # Get user's current balance from database
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (telegram_id,)).fetchone()
        if user:
            # Convert sqlite3.Row to dict to avoid AttributeError
            user_dict = dict(user)
            
            # Get latest balance from bot database
            # This ensures the web app always shows the most current balance
            balance = user_dict.get('balance', 0.0) if user_dict.get('balance') else 0.0
            
            # You can add additional balance sync logic here if needed
            # For example, checking payment transactions, etc.
            
            return {
                'user_id': user_dict['user_id'],
                'balance': balance,
                'username': user_dict.get('username', 'N/A'),
                'language': user_dict.get('language', 'en'),
                'registration_date': user_dict.get('registration_date'),
                'last_activity': user_dict.get('last_activity'),
                'total_orders': user_dict.get('total_orders', 0),
                'total_spent': user_dict.get('total_spent', 0.0)
            }
        return None
    finally:
        conn.close()

def check_smm_api_balance():
    """Check SMM provider API balance - ADMIN ONLY"""
    if not ENABLE_ADMIN_CONTROLS:
        return {'success': False, 'error': 'Admin controls disabled'}
    
    try:
        url = f"{SMM_API_URL}/balance"
        params = {"key": SMM_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return {
                    'success': True,
                    'balance': data.get('balance', 0),
                    'currency': data.get('currency', 'USD')
                }
        return {'success': False, 'error': 'Failed to fetch balance'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_telegram_id_from_request():
    """Extract Telegram ID from various sources (mini app, session, form)"""
    # 1. Check if user is already logged in
    if 'user_id' in session:
        return session['user_id']
    
    # 2. Check for Telegram Web App data in request
    try:
        # Get init data from various sources
        init_data = (
            request.args.get('tgWebAppData') or 
            request.form.get('tgWebAppData') or
            request.headers.get('X-Telegram-Init-Data')
        )
        
        if init_data:
            print(f"🔍 Found Telegram Web App data: {init_data[:100]}...")
            # Parse the init data to extract user info
            # Format: hash=...&user=...&auth_date=...
            params = {}
            for item in init_data.split("&"):
                if "=" in item:
                    key, value = item.split("=", 1)
                    params[key] = value
            
            if 'user' in params:
                user_data = json.loads(params['user'])
                telegram_id = user_data.get('id')
                print(f"✅ Extracted Telegram ID: {telegram_id}")
                return telegram_id
                
    except Exception as e:
        print(f"❌ Error parsing Telegram Web App data: {e}")
    
    # 3. Check for Telegram user in request headers (if available)
    telegram_user_id = request.headers.get('X-Telegram-User-ID')
    if telegram_user_id and telegram_user_id.isdigit():
        print(f"✅ Found Telegram ID in headers: {telegram_user_id}")
        return int(telegram_user_id)
    
    # 4. Check form data (fallback)
    telegram_id = request.form.get('telegram_id')
    if telegram_id and telegram_id.isdigit():
        print(f"✅ Found Telegram ID in form: {telegram_id}")
        return int(telegram_id)
    
    print("❌ No Telegram ID found in request")
    return None

@app.route('/')
def index():
    print("🌐 Index route accessed")
    print(f"🔍 Headers: {dict(request.headers)}")
    print(f"🔍 Args: {dict(request.args)}")
    print(f"🔍 Form: {dict(request.form)}")
    
    # Try to auto-login user from mini app context
    telegram_id = extract_telegram_id_from_request()
    
    if telegram_id:
        print(f"🔍 Found Telegram ID: {telegram_id}")
        # Check if user exists in database
        user = get_user_by_telegram_id(telegram_id)
        if user:
            print(f"✅ User found in database: {user['user_id']}")
            # Auto-login user
            session.permanent = True
            session['user_id'] = user['user_id']
            session['telegram_id'] = str(telegram_id)
            session['is_admin'] = is_admin(telegram_id)
            print(f"🚀 Auto-login successful, redirecting to dashboard")
            return redirect(url_for('dashboard'))
        else:
            print(f"❌ User {telegram_id} not found in database")
    
    # Check if this is a Telegram Web App request
    is_telegram_webapp = (
        request.headers.get('X-Telegram-Bot-Api-Secret-Token') or 
        request.args.get('tgWebAppData') or
        request.headers.get('X-Telegram-Init-Data') or
        'tgWebAppData' in request.args or
        'tgWebAppData' in request.form
    )
    
    if is_telegram_webapp:
        print("📱 This is a Telegram Web App request")
        # This is a mini app request, serve the Telegram Web App template
        return render_template('telegram_webapp.html')
    
    print("🌐 Regular web request, redirecting to login")
    # If no auto-login and not a mini app, redirect to login page
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telegram_id = request.form.get('telegram_id')
        
        if telegram_id and telegram_id.isdigit():
            # Check if user exists in database
            user = get_user_by_telegram_id(int(telegram_id))
            if user:
                session.permanent = True
                session['user_id'] = user['user_id']
                session['telegram_id'] = telegram_id
                session['is_admin'] = is_admin(int(telegram_id))
                return redirect(url_for('dashboard'))
            else:
                flash('User not found. Please use the bot first to register.')
        else:
            flash('Please enter a valid Telegram ID')
    
    return render_template('user_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('steven_store_dashboard.html', user=user, is_admin=session.get('is_admin', False))

@app.route('/balance')
def balance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('user_balance.html', user=user, is_admin=session.get('is_admin', False))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get user orders
    conn = get_db_connection()
    try:
        orders = conn.execute('''
            SELECT * FROM orders 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()
        
        # Convert sqlite3.Row objects to dicts
        orders_list = [dict(order) for order in orders]
    finally:
        conn.close()
    
    return render_template('steven_store_orders.html', user=user, orders=orders_list, is_admin=session.get('is_admin', False))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('steven_store_profile.html', user=user, is_admin=session.get('is_admin', False))

@app.route('/services')
def services():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get available services from database
    conn = get_db_connection()
    try:
        services = conn.execute('''
            SELECT * FROM services 
            ORDER BY category, name
        ''').fetchall()
        
        # Convert sqlite3.Row objects to dicts
        services_list = [dict(service) for service in services]
        
        # Group services by category
        services_by_category = {}
        for service in services_list:
            category = service.get('category', 'Other')
            if category not in services_by_category:
                services_by_category[category] = []
            services_by_category[category].append(service)
            
    finally:
        conn.close()
    
    return render_template('steven_store_dashboard.html', 
                         user=user, 
                         services_by_category=services_by_category,
                         is_admin=session.get('is_admin', False))

@app.route('/services/<category>')
def services_by_category(category):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Validate category
    valid_categories = ['TikTok', 'Facebook', 'Telegram', 'Instagram', 'YouTube']
    if category not in valid_categories:
        flash('Invalid category')
        return redirect(url_for('services'))
    
    # Get services for specific category
    conn = get_db_connection()
    try:
        services = conn.execute('''
            SELECT * FROM services 
            WHERE category = ?
            ORDER BY name
        ''', (category,)).fetchall()
        
        # Convert sqlite3.Row objects to dicts
        services_list = [dict(service) for service in services]
        
        # Group services by category (will only have one category)
        services_by_category = {category: services_list}
            
    finally:
        conn.close()
    
    return render_template('steven_store_dashboard.html', 
                         user=user, 
                         services_by_category=services_by_category,
                         selected_category=category,
                         is_admin=session.get('is_admin', False))

@app.route('/order/<int:service_id>')
def order_service(service_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get service details
    conn = get_db_connection()
    try:
        service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
        if not service:
            flash('Service not found')
            return redirect(url_for('services'))
        
        service_dict = dict(service)
        
        # Check if user has enough balance
        if user['balance'] < service_dict['price']:
            flash(f'Insufficient balance. You need ${service_dict["price"]:.2f} but have ${user["balance"]:.2f}')
            return redirect(url_for('services'))
            
    finally:
        conn.close()
    
    return render_template('user_order_form.html', 
                         user=user, 
                         service=service_dict,
                         is_admin=session.get('is_admin', False))

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    try:
        # Get form data
        service_id = request.form.get('service_id')
        quantity = int(request.form.get('quantity', 1))
        link = request.form.get('link', '').strip()
        additional_info = request.form.get('additional_info', '').strip()
        
        if not service_id or not link:
            return jsonify({'success': False, 'error': 'Service ID and link are required'})
        
        # Get service details
        conn = get_db_connection()
        try:
            service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
            if not service:
                return jsonify({'success': False, 'error': 'Service not found'})
            
            service_dict = dict(service)
            total_cost = service_dict['price'] * quantity
            
            # Check balance
            if user['balance'] < total_cost:
                return jsonify({'success': False, 'error': f'Insufficient balance. Need ${total_cost:.2f}, have ${user["balance"]:.2f}'})
            
            # Create order
            order_id = conn.execute('''
                INSERT INTO orders (user_id, service_id, service_name, quantity, link, 
                                 additional_info, total_cost, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, service_id, service_dict['name'], quantity, link, 
                 additional_info, total_cost, 'pending', datetime.now())).lastrowid
            
            # Deduct balance from user
            new_balance = user['balance'] - total_cost
            conn.execute('UPDATE users SET balance = ? WHERE user_id = ?', (new_balance, user_id))
            
            # Commit transaction
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Order placed successfully!',
                'order_id': order_id,
                'total_cost': total_cost,
                'new_balance': new_balance
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get order details
    conn = get_db_connection()
    try:
        order = conn.execute('''
            SELECT o.*, s.name as service_name, s.description as service_description
            FROM orders o
            LEFT JOIN services s ON o.service_id = s.id
            WHERE o.id = ? AND o.user_id = ?
        ''', (order_id, user_id)).fetchone()
        
        if not order:
            flash('Order not found')
            return redirect(url_for('orders'))
        
        order_dict = dict(order)
        
    finally:
        conn.close()
    
    return render_template('user_order_details.html', 
                         user=user, 
                         order=order_dict,
                         is_admin=session.get('is_admin', False))

@app.route('/api/check_balance')
def api_check_balance():
    """Check SMM provider balance - ADMIN ONLY"""
    if not ENABLE_ADMIN_CONTROLS:
        return jsonify({'error': 'Admin controls disabled'}), 403
    
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not session.get('is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403
    
    # Check SMM provider balance
    api_balance = check_smm_api_balance()
    
    if api_balance['success']:
        return jsonify({
            'success': True,
            'balance': api_balance['balance'],
            'currency': api_balance['currency'],
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': api_balance['error']
        })

@app.route('/api/user_balance')
def api_user_balance():
    """Get user's current balance - synced with bot"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'balance': user['balance'],
            'currency': 'USD',
            'last_sync': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/sync_balance')
def api_sync_balance():
    """Force sync user balance with bot database"""
    if not ENABLE_BALANCE_SYNC:
        return jsonify({'error': 'Balance sync disabled'}), 403
    
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'balance': user['balance'],
            'currency': 'USD',
            'synced_at': datetime.now().isoformat(),
            'message': 'Balance synced successfully'
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/status')
def api_status():
    """Get app status and configuration"""
    return jsonify({
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'features': {
            'admin_controls': ENABLE_ADMIN_CONTROLS,
            'balance_sync': ENABLE_BALANCE_SYNC,
            'transaction_history': ENABLE_TRANSACTION_HISTORY
        },
        'config': {
            'auto_sync_interval': AUTO_SYNC_INTERVAL,
            'session_timeout': SESSION_TIMEOUT
        }
    })

@app.route('/debug')
def debug():
    """Debug route to check request data"""
    return jsonify({
        'headers': dict(request.headers),
        'args': dict(request.args),
        'form': dict(request.form),
        'method': request.method,
        'url': request.url,
        'user_agent': request.headers.get('User-Agent'),
        'telegram_id': extract_telegram_id_from_request(),
        'is_telegram_webapp': bool(
            request.headers.get('X-Telegram-Bot-Api-Secret-Token') or 
            request.args.get('tgWebAppData') or
            request.headers.get('X-Telegram-Init-Data')
        )
    })

@app.route('/test-telegram')
def test_telegram():
    """Test route to check Telegram Web App integration"""
    return render_template('auto_login.html')

@app.route('/api/telegram-webapp', methods=['GET', 'POST'])
def telegram_webapp():
    """Handle Telegram Web App initialization and auto-login"""
    try:
        print("📱 Telegram Web App API called")
        print(f"🔍 Request method: {request.method}")
        print(f"🔍 Headers: {dict(request.headers)}")
        print(f"🔍 Args: {dict(request.args)}")
        print(f"🔍 Form: {dict(request.form)}")
        
        # Get Telegram ID from various sources
        telegram_id = None
        
        # Method 1: From JSON body (POST request)
        if request.is_json:
            data = request.get_json()
            telegram_id = data.get('telegram_id')
            print(f"🔍 Telegram ID from JSON: {telegram_id}")
        
        # Method 2: From init data
        if not telegram_id:
            init_data = (
                request.args.get('tgWebAppData') or 
                request.form.get('tgWebAppData') or
                request.headers.get('X-Telegram-Init-Data')
            )
            
            if init_data:
                print(f"🔍 Found init data: {init_data[:100]}...")
                # Parse the init data
                params = {}
                for item in init_data.split("&"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        params[key] = value
                
                if 'user' in params:
                    user_data = json.loads(params['user'])
                    telegram_id = user_data.get('id')
                    print(f"🔍 Telegram ID from init data: {telegram_id}")
        
        if telegram_id:
            print(f"✅ Processing Telegram ID: {telegram_id}")
            # Check if user exists in database
            user = get_user_by_telegram_id(telegram_id)
            if user:
                print(f"✅ User found: {user['user_id']}")
                # Auto-login user
                session.permanent = True
                session['user_id'] = user['user_id']
                session['telegram_id'] = str(telegram_id)
                session['is_admin'] = is_admin(telegram_id)
                
                return jsonify({
                    'success': True,
                    'message': 'Auto-login successful',
                    'redirect': url_for('dashboard'),
                    'user_id': user['user_id'],
                    'username': user.get('username', 'N/A')
                })
            else:
                print(f"❌ User {telegram_id} not found in database")
                return jsonify({
                    'success': False,
                    'error': 'User not found in database. Please use the bot first to register.',
                    'code': 'USER_NOT_FOUND'
                })
        else:
            print("❌ No Telegram ID provided")
            return jsonify({
                'success': False,
                'error': 'No Telegram ID provided',
                'code': 'NO_TELEGRAM_ID'
            })
        
    except Exception as e:
        print(f"❌ Error in telegram_webapp: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'INTERNAL_ERROR'
        })

@app.route('/auto-login')
def auto_login():
    """Direct auto-login route for Telegram Web App"""
    try:
        print("🚀 Auto-login route accessed")
        print(f"🔍 Headers: {dict(request.headers)}")
        print(f"🔍 Args: {dict(request.args)}")
        
        # Try to extract Telegram ID
        telegram_id = extract_telegram_id_from_request()
        
        if telegram_id:
            print(f"✅ Found Telegram ID: {telegram_id}")
            # Check if user exists in database
            user = get_user_by_telegram_id(telegram_id)
            if user:
                print(f"✅ User found: {user['user_id']}")
                # Auto-login user
                session.permanent = True
                session['user_id'] = user['user_id']
                session['telegram_id'] = str(telegram_id)
                session['is_admin'] = is_admin(telegram_id)
                print(f"🚀 Auto-login successful, redirecting to dashboard")
                return redirect(url_for('dashboard'))
            else:
                print(f"❌ User {telegram_id} not found in database")
                return render_template('auto_login.html', error="User not found in database")
        else:
            print("❌ No Telegram ID found")
            return render_template('auto_login.html', error="No Telegram ID found")
            
    except Exception as e:
        print(f"❌ Error in auto-login: {e}")
        return render_template('auto_login.html', error=str(e))

@app.route('/api/services')
def api_services():
    """Get all available services"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    try:
        services = conn.execute('''
            SELECT id, name, description, price, category, min_quantity, max_quantity
            FROM services 
            ORDER BY category, name
        ''').fetchall()
        
        services_list = [dict(service) for service in services]
        
        # Group by category
        services_by_category = {}
        for service in services_list:
            category = service.get('category', 'Other')
            if category not in services_by_category:
                services_by_category[category] = []
            services_by_category[category].append(service)
        
        return jsonify({
            'success': True,
            'services': services_by_category
        })
        
    finally:
        conn.close()

@app.route('/api/place_order', methods=['POST'])
def api_place_order():
    """API endpoint for placing orders"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = get_user_balance_with_sync(user_id)
    
    if not user:
        session.clear()
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    try:
        data = request.get_json()
        service_id = data.get('service_id')
        quantity = int(data.get('quantity', 1))
        link = data.get('link', '').strip()
        additional_info = data.get('additional_info', '').strip()
        
        if not service_id or not link:
            return jsonify({'success': False, 'error': 'Service ID and link are required'})
        
        # Get service details
        conn = get_db_connection()
        try:
            service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
            if not service:
                return jsonify({'success': False, 'error': 'Service not found'})
            
            service_dict = dict(service)
            total_cost = service_dict['price'] * quantity
            
            # Check balance
            if user['balance'] < total_cost:
                return jsonify({'success': False, 'error': f'Insufficient balance. Need ${total_cost:.2f}, have ${user["balance"]:.2f}'})
            
            # Create order
            order_id = conn.execute('''
                INSERT INTO orders (user_id, service_id, service_name, quantity, link, 
                                 additional_info, total_cost, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, service_id, service_dict['name'], quantity, link, 
                 additional_info, total_cost, 'pending', datetime.now())).lastrowid
            
            # Deduct balance from user
            new_balance = user['balance'] - total_cost
            conn.execute('UPDATE users SET balance = ? WHERE user_id = ?', (new_balance, user_id))
            
            # Commit transaction
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Order placed successfully!',
                'order_id': order_id,
                'total_cost': total_cost,
                'new_balance': new_balance,
                'order': {
                    'id': order_id,
                    'service_name': service_dict['name'],
                    'quantity': quantity,
                    'link': link,
                    'total_cost': total_cost,
                    'status': 'pending',
                    'created_at': datetime.now().isoformat()
                }
            })
            
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/user_orders')
def api_user_orders():
    """Get user's orders"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    try:
        orders = conn.execute('''
            SELECT o.*, s.name as service_name, s.description as service_description
            FROM orders o
            LEFT JOIN services s ON o.service_id = s.id
            WHERE o.user_id = ? 
            ORDER BY o.created_at DESC
        ''', (user_id,)).fetchall()
        
        orders_list = [dict(order) for order in orders]
        
        return jsonify({
            'success': True,
            'orders': orders_list
        })
        
    finally:
        conn.close()

if __name__ == '__main__':
    print(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
    print(f"📱 User Web App running on http://{HOST}:{PORT}")
    print(f"🔧 Debug mode: {DEBUG_MODE}")
    print(f"👑 Admin controls: {ENABLE_ADMIN_CONTROLS}")
    print(f"💰 Balance sync: {ENABLE_BALANCE_SYNC}")
    print(f"📊 Transaction history: {ENABLE_TRANSACTION_HISTORY}")
    print(f"⏰ Auto-sync interval: {AUTO_SYNC_INTERVAL} seconds")
    print(f"🔐 Session timeout: {SESSION_TIMEOUT} seconds")
    print(f"👥 Admin IDs: {ADMIN_IDS}")
    print("\n" + "="*50)
    
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
