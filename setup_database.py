#!/usr/bin/env python3
"""
JakLike Database Setup Script
Creates necessary tables and populates with sample data
"""

import sqlite3
import os

def setup_database():
    """Setup database tables and populate with sample data"""
    
    # Check if database exists
    db_exists = os.path.exists('bot_data.db')
    
    # Connect to database
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    print("🔧 Setting up JakLike database...")
    
    # Create services table with package options
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            service_type TEXT NOT NULL,
            key_name TEXT NOT NULL,
            package_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            link TEXT NOT NULL,
            additional_info TEXT,
            total_cost REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')
    
    # Check if users table has required columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'total_orders' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN total_orders INTEGER DEFAULT 0')
        print("✅ Added total_orders column to users table")
    
    if 'total_spent' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN total_spent REAL DEFAULT 0.0')
        print("✅ Added total_spent column to users table")
    
    # Clear existing services to avoid duplicates
    cursor.execute('DELETE FROM services')
    
    # Insert services with multiple package options like in bot
    services = [
        # TikTok Combo Services (Likes + Views)
        ('100 Likes + 1K Views', 'TikTok combo package with likes and views', 0.10, 'TikTok', 100, 'combo', 'tiktok_100', '{"likes": 100, "views": 1000}'),
        ('250 Likes + 2K Views', 'TikTok combo package with likes and views', 0.18, 'TikTok', 250, 'combo', 'tiktok_250', '{"likes": 250, "views": 2000}'),
        ('500 Likes + 5K Views', 'TikTok combo package with likes and views', 0.29, 'TikTok', 500, 'combo', 'tiktok_500', '{"likes": 500, "views": 5000}'),
        ('1K Likes + 10K Views', 'TikTok combo package with likes and views', 0.45, 'TikTok', 1000, 'combo', 'tiktok_1k', '{"likes": 1000, "views": 10000}'),
        ('2K Likes + 13K Views', 'TikTok combo package with likes and views', 0.85, 'TikTok', 2000, 'combo', 'tiktok_2k', '{"likes": 2000, "views": 13000}'),
        ('3K Likes + 15K Views', 'TikTok combo package with likes and views', 1.29, 'TikTok', 3000, 'combo', 'tiktok_3k', '{"likes": 3000, "views": 15000}'),
        ('5K Likes + 30K Views', 'TikTok combo package with likes and views', 1.99, 'TikTok', 5000, 'combo', 'tiktok_5k', '{"likes": 5000, "views": 30000}'),
        ('10K Likes + 50K Views', 'TikTok combo package with likes and views', 3.89, 'TikTok', 10000, 'combo', 'tiktok_10k', '{"likes": 10000, "views": 50000}'),
        ('20K Likes + 90K Views', 'TikTok combo package with likes and views', 6.49, 'TikTok', 20000, 'combo', 'tiktok_20k', '{"likes": 20000, "views": 90000}'),
        ('30K Likes + 130K Views', 'TikTok combo package with likes and views', 9.49, 'TikTok', 30000, 'combo', 'tiktok_30k', '{"likes": 30000, "views": 130000}'),
        ('40K Likes + 160K Views', 'TikTok combo package with likes and views', 12.49, 'TikTok', 40000, 'combo', 'tiktok_40k', '{"likes": 40000, "views": 160000}'),
        ('50K Likes + 190K Views', 'TikTok combo package with likes and views', 13.49, 'TikTok', 50000, 'combo', 'tiktok_50k', '{"likes": 50000, "views": 190000}'),
        ('100K Likes + 230K Views', 'TikTok combo package with likes and views', 19.99, 'TikTok', 100000, 'combo', 'tiktok_100k', '{"likes": 100000, "views": 230000}'),
        
        # TikTok Views Only
        ('10K Views', 'TikTok views only', 0.10, 'TikTok', 10000, 'views', 'view_10k', '{"views": 10000}'),
        ('20K Views', 'TikTok views only', 0.15, 'TikTok', 20000, 'views', 'view_20k', '{"views": 20000}'),
        ('30K Views', 'TikTok views only', 0.20, 'TikTok', 30000, 'views', 'view_30k', '{"views": 30000}'),
        ('40K Views', 'TikTok views only', 0.25, 'TikTok', 40000, 'views', 'view_40k', '{"views": 40000}'),
        ('50K Views', 'TikTok views only', 0.30, 'TikTok', 50000, 'views', 'view_50k', '{"views": 50000}'),
        ('60K Views', 'TikTok views only', 0.36, 'TikTok', 60000, 'views', 'view_60k', '{"views": 60000}'),
        ('70K Views', 'TikTok views only', 0.40, 'TikTok', 70000, 'views', 'view_70k', '{"views": 70000}'),
        ('80K Views', 'TikTok views only', 0.45, 'TikTok', 80000, 'views', 'view_80k', '{"views": 80000}'),
        ('90K Views', 'TikTok views only', 0.50, 'TikTok', 90000, 'views', 'view_90k', '{"views": 90000}'),
        ('100K Views', 'TikTok views only', 1.00, 'TikTok', 100000, 'views', 'view_100k', '{"views": 100000}'),
        
        # TikTok Saves
        ('100 Saves', 'TikTok saves only', 0.12, 'TikTok', 100, 'saves', 'save_100', '{"saves": 100}'),
        ('500 Saves', 'TikTok saves only', 0.60, 'TikTok', 500, 'saves', 'save_500', '{"saves": 500}'),
        ('1K Saves', 'TikTok saves only', 1.10, 'TikTok', 1000, 'saves', 'save_1k', '{"saves": 1000}'),
        
        # TikTok Shares
        ('100 Shares', 'TikTok shares only', 0.25, 'TikTok', 100, 'shares', 'share_100', '{"shares": 100}'),
        ('500 Shares', 'TikTok shares only', 1.00, 'TikTok', 500, 'shares', 'share_500', '{"shares": 500}'),
        ('1K Shares', 'TikTok shares only', 1.50, 'TikTok', 1000, 'shares', 'share_1k', '{"shares": 1000}'),
        
        # TikTok Followers
        ('100 Followers', 'TikTok followers only', 0.45, 'TikTok', 100, 'followers', 'followers_100', '{"followers": 100}'),
        ('500 Followers', 'TikTok followers only', 1.50, 'TikTok', 500, 'followers', 'followers_500', '{"followers": 500}'),
        ('1K Followers', 'TikTok followers only', 2.50, 'TikTok', 1000, 'followers', 'followers_1k', '{"followers": 1000}'),
        ('2K Followers', 'TikTok followers only', 4.50, 'TikTok', 2000, 'followers', 'followers_2k', '{"followers": 2000}'),
        ('5K Followers', 'TikTok followers only', 11.50, 'TikTok', 5000, 'followers', 'followers_5k', '{"followers": 5000}'),
        ('10K Followers', 'TikTok followers only', 20.00, 'TikTok', 10000, 'followers', 'followers_10k', '{"followers": 10000}'),
        
        # Facebook Page Followers
        ('500 Page Followers', 'Facebook page followers', 1.30, 'Facebook', 500, 'page_followers', 'fb_page_500', '{"page_followers": 500}'),
        ('1K Page Followers', 'Facebook page followers', 2.00, 'Facebook', 1000, 'page_followers', 'fb_page_1k', '{"page_followers": 1000}'),
        ('5K Page Followers', 'Facebook page followers', 7.80, 'Facebook', 5000, 'page_followers', 'fb_page_5k', '{"page_followers": 5000}'),
        ('10K Page Followers', 'Facebook page followers', 13.00, 'Facebook', 10000, 'page_followers', 'fb_page_10k', '{"page_followers": 10000}'),
        
        # Facebook Profile Followers
        ('500 Profile Followers', 'Facebook profile followers', 1.00, 'Facebook', 500, 'profile_followers', 'fb_prof_500', '{"profile_followers": 500}'),
        ('1K Profile Followers', 'Facebook profile followers', 1.50, 'Facebook', 1000, 'profile_followers', 'fb_prof_1k', '{"profile_followers": 1000}'),
        ('5K Profile Followers', 'Facebook profile followers', 7.50, 'Facebook', 5000, 'profile_followers', 'fb_prof_5k', '{"profile_followers": 5000}'),
        ('10K Profile Followers', 'Facebook profile followers', 13.00, 'Facebook', 10000, 'profile_followers', 'fb_prof_10k', '{"profile_followers": 10000}'),
        
        # Facebook Video Views
        ('1K Video Views', 'Facebook video views', 0.20, 'Facebook', 1000, 'video_views', 'fb_view_1k', '{"video_views": 1000}'),
        ('5K Video Views', 'Facebook video views', 1.00, 'Facebook', 5000, 'video_views', 'fb_view_5k', '{"video_views": 5000}'),
        ('10K Video Views', 'Facebook video views', 1.75, 'Facebook', 10000, 'video_views', 'fb_view_10k', '{"video_views": 10000}'),
        ('100K Video Views', 'Facebook video views', 13.00, 'Facebook', 100000, 'video_views', 'fb_view_100k', '{"video_views": 100000}'),
        
        # Facebook Reactions
        ('100 Post Likes', 'Facebook post likes', 0.19, 'Facebook', 100, 'reactions_like', 'fb_like_100', '{"reactions": "like", "quantity": 100}'),
        ('500 Post Likes', 'Facebook post likes', 0.85, 'Facebook', 500, 'reactions_like', 'fb_like_500', '{"reactions": "like", "quantity": 500}'),
        ('1K Post Likes', 'Facebook post likes', 1.50, 'Facebook', 1000, 'reactions_like', 'fb_like_1k', '{"reactions": "like", "quantity": 1000}'),
        ('100 Post Love', 'Facebook post love reactions', 0.25, 'Facebook', 100, 'reactions_love', 'fb_love_100', '{"reactions": "love", "quantity": 100}'),
        ('500 Post Love', 'Facebook post love reactions', 0.95, 'Facebook', 500, 'reactions_love', 'fb_love_500', '{"reactions": "love", "quantity": 500}'),
        ('1K Post Love', 'Facebook post love reactions', 1.75, 'Facebook', 1000, 'reactions_love', 'fb_love_1k', '{"reactions": "love", "quantity": 1000}'),
        ('100 Post Wow', 'Facebook post wow reactions', 0.25, 'Facebook', 100, 'reactions_wow', 'fb_wow_100', '{"reactions": "wow", "quantity": 100}'),
        ('500 Post Wow', 'Facebook post wow reactions', 0.95, 'Facebook', 500, 'reactions_wow', 'fb_wow_500', '{"reactions": "wow", "quantity": 500}'),
        ('1K Post Wow', 'Facebook post wow reactions', 1.75, 'Facebook', 1000, 'reactions_wow', 'fb_wow_1k', '{"reactions": "wow", "quantity": 1000}'),
        ('100 Post Care', 'Facebook post care reactions', 0.25, 'Facebook', 100, 'reactions_care', 'fb_care_100', '{"reactions": "care", "quantity": 100}'),
        ('500 Post Care', 'Facebook post care reactions', 0.95, 'Facebook', 500, 'reactions_care', 'fb_care_500', '{"reactions": "care", "quantity": 500}'),
        ('1K Post Care', 'Facebook post care reactions', 1.75, 'Facebook', 1000, 'reactions_care', 'fb_care_1k', '{"reactions": "care", "quantity": 1000}'),
        ('100 Post Haha', 'Facebook post haha reactions', 0.25, 'Facebook', 100, 'reactions_haha', 'fb_haha_100', '{"reactions": "haha", "quantity": 100}'),
        ('500 Post Haha', 'Facebook post haha reactions', 0.95, 'Facebook', 500, 'reactions_haha', 'fb_haha_500', '{"reactions": "haha", "quantity": 500}'),
        ('1K Post Haha', 'Facebook post haha reactions', 1.75, 'Facebook', 1000, 'reactions_haha', 'fb_haha_1k', '{"reactions": "haha", "quantity": 1000}'),
        ('100 Post Sad', 'Facebook post sad reactions', 0.25, 'Facebook', 100, 'reactions_sad', 'fb_sad_100', '{"reactions": "sad", "quantity": 100}'),
        ('500 Post Sad', 'Facebook post sad reactions', 0.95, 'Facebook', 500, 'reactions_sad', 'fb_sad_500', '{"reactions": "sad", "quantity": 500}'),
        ('1K Post Sad', 'Facebook post sad reactions', 1.75, 'Facebook', 1000, 'reactions_sad', 'fb_sad_1k', '{"reactions": "sad", "quantity": 1000}'),
        ('100 Post Angry', 'Facebook post angry reactions', 0.25, 'Facebook', 100, 'reactions_angry', 'fb_angry_100', '{"reactions": "angry", "quantity": 100}'),
        ('500 Post Angry', 'Facebook post angry reactions', 0.95, 'Facebook', 500, 'reactions_angry', 'fb_angry_500', '{"reactions": "angry", "quantity": 500}'),
        ('1K Post Angry', 'Facebook post angry reactions', 1.75, 'Facebook', 1000, 'reactions_angry', 'fb_angry_1k', '{"reactions": "angry", "quantity": 1000}'),
        
        # Telegram Members (7-Day)
        ('500 Members (7-Day)', 'Telegram channel members for 7 days', 0.70, 'Telegram', 500, 'members_7day', 'tg_7day_500', '{"members": 500, "duration": "7-day"}'),
        ('1K Members (7-Day)', 'Telegram channel members for 7 days', 1.40, 'Telegram', 1000, 'members_7day', 'tg_7day_1k', '{"members": 1000, "duration": "7-day"}'),
        ('3K Members (7-Day)', 'Telegram channel members for 7 days', 3.20, 'Telegram', 3000, 'members_7day', 'tg_7day_3k', '{"members": 3000, "duration": "7-day"}'),
        
        # Telegram Members (30-Day)
        ('500 Members (30-Day)', 'Telegram channel members for 30 days', 0.90, 'Telegram', 500, 'members_30day', 'tg_30day_500', '{"members": 500, "duration": "30-day"}'),
        ('1K Members (30-Day)', 'Telegram channel members for 30 days', 2.50, 'Telegram', 1000, 'members_30day', 'tg_30day_1k', '{"members": 1000, "duration": "30-day"}'),
        ('3K Members (30-Day)', 'Telegram channel members for 30 days', 6.00, 'Telegram', 3000, 'members_30day', 'tg_30day_3k', '{"members": 3000, "duration": "30-day"}'),
        
        # Telegram Members (Lifetime)
        ('500 Members (Lifetime)', 'Telegram channel members lifetime', 2.50, 'Telegram', 500, 'members_lifetime', 'tg_life_500', '{"members": 500, "duration": "Lifetime"}'),
        ('1K Members (Lifetime)', 'Telegram channel members lifetime', 4.50, 'Telegram', 1000, 'members_lifetime', 'tg_life_1k', '{"members": 1000, "duration": "Lifetime"}'),
        
        # Telegram Views
        ('1K Views', 'Telegram post views', 0.10, 'Telegram', 1000, 'views', 'tg_view_1k', '{"views": 1000}'),
        ('5K Views', 'Telegram post views', 0.45, 'Telegram', 5000, 'views', 'tg_view_5k', '{"views": 5000}'),
        ('10K Views', 'Telegram post views', 0.85, 'Telegram', 10000, 'views', 'tg_view_10k', '{"views": 10000}'),
        
        # Telegram Reactions
        ('100 Positive Reactions', 'Telegram positive reactions (👍❤️🔥)', 0.15, 'Telegram', 100, 'reactions_positive', 'tg_pos_100', '{"reactions": "positive", "quantity": 100}'),
        ('500 Positive Reactions', 'Telegram positive reactions (👍❤️🔥)', 0.65, 'Telegram', 500, 'reactions_positive', 'tg_pos_500', '{"reactions": "positive", "quantity": 500}'),
        ('1K Positive Reactions', 'Telegram positive reactions (👍❤️🔥)', 1.20, 'Telegram', 1000, 'reactions_positive', 'tg_pos_1k', '{"reactions": "positive", "quantity": 1000}'),
        ('100 Negative Reactions', 'Telegram negative reactions (👎😱💩😢🤮)', 0.15, 'Telegram', 100, 'reactions_negative', 'tg_neg_100', '{"reactions": "negative", "quantity": 100}'),
        ('500 Negative Reactions', 'Telegram negative reactions (👎😱💩😢🤮)', 0.65, 'Telegram', 500, 'reactions_negative', 'tg_neg_500', '{"reactions": "negative", "quantity": 500}'),
        ('1K Negative Reactions', 'Telegram negative reactions (👎😱💩😢🤮)', 1.20, 'Telegram', 1000, 'reactions_negative', 'tg_neg_1k', '{"reactions": "negative", "quantity": 1000}'),
    ]
    
    cursor.executemany('''
        INSERT INTO services (name, description, price, category, quantity, service_type, key_name, package_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', services)
    
    print("✅ Services table created with multiple package options")
    print(f"📦 Added {len(services)} service packages")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("🎉 Database setup completed successfully!")
    print("\n📊 Database contains:")
    print("   • Services table with multiple package options")
    print("   • Orders table for tracking user orders")
    print("   • Users table with total_orders and total_spent columns")
    
    if not db_exists:
        print("\n💡 This is a new database. You may need to:")
        print("   • Add some users through your bot")
        print("   • Test the mini app functionality")

if __name__ == "__main__":
    setup_database()
