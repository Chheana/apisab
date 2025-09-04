from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import sqlite3
import os
from datetime import datetime, timedelta
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
DB_FILE = "bot_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = get_db_connection()
    try:
        # For now, let's use a simple admin check
        # You can expand this later with a proper users table
        if username == "admin" and password == "admin123":
            return True
        return False
    finally:
        conn.close()

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        # Get basic stats
        total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_balance = conn.execute('SELECT SUM(balance) FROM users').fetchone()[0] or 0.0
        orders_today = conn.execute("SELECT COUNT(*) FROM orders WHERE DATE(created_at) = DATE('now')").fetchone()[0]
        
        # Get recent orders
        recent_orders = conn.execute('''
            SELECT o.*, u.balance 
            FROM orders o 
            JOIN users u ON o.user_id = u.user_id 
            ORDER BY o.created_at DESC 
            LIMIT 10
        ''').fetchall()
        
        # Get recent users
        recent_users = conn.execute('''
            SELECT * FROM users 
            ORDER BY created_at DESC 
            LIMIT 10
        ''').fetchall()
        
        stats = {
            'total_users': total_users,
            'total_balance': total_balance,
            'orders_today': orders_today
        }
        
    finally:
        conn.close()
    
    return render_template('dashboard.html', stats=stats, recent_orders=recent_orders, recent_users=recent_users)

@app.route('/users')
def users():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    finally:
        conn.close()
    
    return render_template('users.html', users=users)

@app.route('/orders')
def orders():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        orders = conn.execute('''
            SELECT o.*, u.balance 
            FROM orders o 
            JOIN users u ON o.user_id = u.user_id 
            ORDER BY o.created_at DESC
        ''').fetchall()
    finally:
        conn.close()
    
    return render_template('orders.html', orders=orders)

@app.route('/api/stats')
def api_stats():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    try:
        # Get daily stats for the last 7 days
        stats = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            orders_count = conn.execute(
                "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ?", 
                (date,)
            ).fetchone()[0]
            
            topup_amount = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM balance_history WHERE DATE(created_at) = ? AND type = 'deposit'", 
                (date,)
            ).fetchone()[0]
            
            stats.append({
                'date': date,
                'orders': orders_count,
                'topup': float(topup_amount)
            })
        
        return jsonify(stats)
    finally:
        conn.close()

@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        if user:
            return jsonify(dict(user))
        return jsonify({'error': 'User not found'}), 404
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




