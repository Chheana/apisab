#!/usr/bin/env python3
"""
Setup script to create services table and populate it with service data
"""

import sqlite3

# Service data organized by quantity (ascending order)
SERVICES_DATA = [
    # TikTok Combo Services (Likes + Views) - Organized by quantity
    {"name": "100 Likes + 1K Views - $0.10", "price": 0.10, "category": "TikTok", "service_type": "combo", "quantity": 100, "views": 1000, "likes": 100, "sort_order": 1},
    {"name": "250 Likes + 2K Views - $0.18", "price": 0.18, "category": "TikTok", "service_type": "combo", "quantity": 250, "views": 2000, "likes": 250, "sort_order": 2},
    {"name": "500 Likes + 5K Views - $0.29", "price": 0.29, "category": "TikTok", "service_type": "combo", "quantity": 500, "views": 5000, "likes": 500, "sort_order": 3},
    {"name": "1K Likes + 10K Views - $0.45", "price": 0.45, "category": "TikTok", "service_type": "combo", "quantity": 1000, "views": 10000, "likes": 1000, "sort_order": 4},
    {"name": "2K Likes + 13K Views - $0.85", "price": 0.85, "category": "TikTok", "service_type": "combo", "quantity": 2000, "views": 13000, "likes": 2000, "sort_order": 5},
    {"name": "3K Likes + 15K Views - $1.29", "price": 1.29, "category": "TikTok", "service_type": "combo", "quantity": 3000, "views": 15000, "likes": 3000, "sort_order": 6},
    {"name": "5K Likes + 30K Views - $1.99", "price": 1.99, "category": "TikTok", "service_type": "combo", "quantity": 5000, "views": 30000, "likes": 5000, "sort_order": 7},
    {"name": "10K Likes + 50K Views - $3.89", "price": 3.89, "category": "TikTok", "service_type": "combo", "quantity": 10000, "views": 50000, "likes": 10000, "sort_order": 8},
    {"name": "20K Likes + 90K Views - $6.49", "price": 6.49, "category": "TikTok", "service_type": "combo", "quantity": 20000, "views": 90000, "likes": 20000, "sort_order": 9},
    {"name": "30K Likes + 130K Views - $9.49", "price": 9.49, "category": "TikTok", "service_type": "combo", "quantity": 30000, "views": 130000, "likes": 30000, "sort_order": 10},
    {"name": "40K Likes + 160K Views - $12.49", "price": 12.49, "category": "TikTok", "service_type": "combo", "quantity": 40000, "views": 160000, "likes": 40000, "sort_order": 11},
    {"name": "50K Likes + 190K Views - $13.49", "price": 13.49, "category": "TikTok", "service_type": "combo", "quantity": 50000, "views": 190000, "likes": 50000, "sort_order": 12},
    {"name": "100K Likes + 230K Views - $19.99", "price": 19.99, "category": "TikTok", "service_type": "combo", "quantity": 100000, "views": 230000, "likes": 100000, "sort_order": 13},
    
    # TikTok Views Only - Organized by quantity
    {"name": "10K Views - $0.10", "price": 0.10, "category": "TikTok", "service_type": "views", "quantity": 10000, "views": 10000, "sort_order": 1},
    {"name": "20K Views - $0.15", "price": 0.15, "category": "TikTok", "service_type": "views", "quantity": 20000, "views": 20000, "sort_order": 2},
    {"name": "30K Views - $0.20", "price": 0.20, "category": "TikTok", "service_type": "views", "quantity": 30000, "views": 30000, "sort_order": 3},
    {"name": "40K Views - $0.25", "price": 0.25, "category": "TikTok", "service_type": "views", "quantity": 40000, "views": 40000, "sort_order": 4},
    {"name": "50K Views - $0.30", "price": 0.30, "category": "TikTok", "service_type": "views", "quantity": 50000, "views": 50000, "sort_order": 5},
    {"name": "60K Views - $0.36", "price": 0.36, "category": "TikTok", "service_type": "views", "quantity": 60000, "views": 60000, "sort_order": 6},
    {"name": "70K Views - $0.40", "price": 0.40, "category": "TikTok", "service_type": "views", "quantity": 70000, "views": 70000, "sort_order": 7},
    {"name": "80K Views - $0.45", "price": 0.45, "category": "TikTok", "service_type": "views", "quantity": 80000, "views": 80000, "sort_order": 8},
    {"name": "90K Views - $0.50", "price": 0.50, "category": "TikTok", "service_type": "views", "quantity": 90000, "views": 90000, "sort_order": 9},
    {"name": "100K Views - $1", "price": 1.00, "category": "TikTok", "service_type": "views", "quantity": 100000, "views": 100000, "sort_order": 10},
    
    # TikTok Followers - Organized by quantity (100, 500, 1K, 2K, 5K, 10K)
    {"name": "100 Followers - $0.45", "price": 0.45, "category": "TikTok", "service_type": "followers", "quantity": 100, "sort_order": 1},
    {"name": "500 Followers - $1.50", "price": 1.50, "category": "TikTok", "service_type": "followers", "quantity": 500, "sort_order": 2},
    {"name": "1K Followers - $2.50", "price": 2.50, "category": "TikTok", "service_type": "followers", "quantity": 1000, "sort_order": 3},
    {"name": "2K Followers - $4.50", "price": 4.50, "category": "TikTok", "service_type": "followers", "quantity": 2000, "sort_order": 4},
    {"name": "5K Followers - $11.50", "price": 11.50, "category": "TikTok", "service_type": "followers", "quantity": 5000, "sort_order": 5},
    {"name": "10K Followers - $20.00", "price": 20.00, "category": "TikTok", "service_type": "followers", "quantity": 10000, "sort_order": 6},
    
    # TikTok Saves - Organized by quantity
    {"name": "100 Saves - $0.12", "price": 0.12, "category": "TikTok", "service_type": "saves", "quantity": 100, "sort_order": 1},
    {"name": "500 Saves - $0.60", "price": 0.60, "category": "TikTok", "service_type": "saves", "quantity": 500, "sort_order": 2},
    {"name": "1K Saves - $1.10", "price": 1.10, "category": "TikTok", "service_type": "saves", "quantity": 1000, "sort_order": 3},
    
    # TikTok Shares - Organized by quantity
    {"name": "100 Shares - $0.25", "price": 0.25, "category": "TikTok", "service_type": "shares", "quantity": 100, "sort_order": 1},
    {"name": "500 Shares - $1.00", "price": 1.00, "category": "TikTok", "service_type": "shares", "quantity": 500, "sort_order": 2},
    {"name": "1K Shares - $1.50", "price": 1.50, "category": "TikTok", "service_type": "shares", "quantity": 1000, "sort_order": 3},
    
    # Facebook Services - Organized by quantity
    {"name": "500 Page Followers - $1.30", "price": 1.30, "category": "Facebook", "service_type": "page_followers", "quantity": 500, "sort_order": 1},
    {"name": "1K Page Followers - $2.00", "price": 2.00, "category": "Facebook", "service_type": "page_followers", "quantity": 1000, "sort_order": 2},
    {"name": "5K Page Followers - $7.80", "price": 7.80, "category": "Facebook", "service_type": "page_followers", "quantity": 5000, "sort_order": 3},
    {"name": "10K Page Followers - $13.00", "price": 13.00, "category": "Facebook", "service_type": "page_followers", "quantity": 10000, "sort_order": 4},
    
    {"name": "500 Profile Followers - $1", "price": 1.00, "category": "Facebook", "service_type": "profile_followers", "quantity": 500, "sort_order": 1},
    {"name": "1K Profile Followers - $1.5", "price": 1.50, "category": "Facebook", "service_type": "profile_followers", "quantity": 1000, "sort_order": 2},
    {"name": "5K Profile Followers - $7.50", "price": 7.50, "category": "Facebook", "service_type": "profile_followers", "quantity": 5000, "sort_order": 3},
    {"name": "10K Profile Followers - $13.00", "price": 13.00, "category": "Facebook", "service_type": "profile_followers", "quantity": 10000, "sort_order": 4},
    
    # Telegram Services - Organized by quantity
    {"name": "500 Members (7-Day) - $0.70", "price": 0.70, "category": "Telegram", "service_type": "members_7day", "quantity": 500, "sort_order": 1},
    {"name": "1K Members (7-Day) - $1.40", "price": 1.40, "category": "Telegram", "service_type": "members_7day", "quantity": 1000, "sort_order": 2},
    {"name": "3K Members (7-Day) - $3.20", "price": 3.20, "category": "Telegram", "service_type": "members_7day", "quantity": 3000, "sort_order": 3},
    
    {"name": "500 Members (30-Day) - $0.90", "price": 0.90, "category": "Telegram", "service_type": "members_30day", "quantity": 500, "sort_order": 1},
    {"name": "1K Members (30-Day) - $2.50", "price": 2.50, "category": "Telegram", "service_type": "members_30day", "quantity": 1000, "sort_order": 2},
    {"name": "3K Members (30-Day) - $6.00", "price": 6.00, "category": "Telegram", "service_type": "members_30day", "quantity": 3000, "sort_order": 3},
    
    {"name": "500 Members (Lifetime) - $2.50", "price": 2.50, "category": "Telegram", "service_type": "members_lifetime", "quantity": 500, "sort_order": 1},
    {"name": "1K Members (Lifetime) - $4.50", "price": 4.50, "category": "Telegram", "service_type": "members_lifetime", "quantity": 1000, "sort_order": 2},
    {"name": "3K Members (Lifetime) - $12.00", "price": 12.00, "category": "Telegram", "service_type": "members_lifetime", "quantity": 3000, "sort_order": 3},
]

def setup_services_table():
    """Create services table and populate it with data"""
    
    try:
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        print("🔧 Setting up services table...")
        
        # Drop existing services table if it exists
        cursor.execute("DROP TABLE IF EXISTS services")
        
        # Create services table
        cursor.execute("""
            CREATE TABLE services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                service_type TEXT NOT NULL,
                quantity INTEGER,
                views INTEGER,
                likes INTEGER,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Services table created")
        
        # Insert service data
        for service in SERVICES_DATA:
            cursor.execute("""
                INSERT INTO services (name, price, category, service_type, quantity, views, likes, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                service['name'],
                service['price'],
                service['category'],
                service['service_type'],
                service.get('quantity'),
                service.get('views'),
                service.get('likes'),
                service.get('sort_order', 0)
            ))
        
        conn.commit()
        print(f"✅ Inserted {len(SERVICES_DATA)} services")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM services")
        count = cursor.fetchone()[0]
        print(f"✅ Total services in database: {count}")
        
        # Show sample data
        cursor.execute("SELECT name, price, category, service_type FROM services LIMIT 5")
        sample = cursor.fetchall()
        print("\n📋 Sample services:")
        for row in sample:
            print(f"  • {row[0]} | ${row[1]:.2f} | {row[2]} | {row[3]}")
        
        conn.close()
        print("\n🎉 Services database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up services table: {e}")
        return False

if __name__ == "__main__":
    setup_services_table()

