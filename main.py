import telebot
from telebot import types
import sqlite3
import threading
import time
import requests
import logging
import queue
import random
from concurrent.futures import ThreadPoolExecutor
import io
from datetime import datetime, timedelta
import sys

# ==================== WARNING: REPLACE WITH YOUR OWN DATA ====================
# You must replace these placeholder values with your actual bot token, admin IDs, etc.
# This code will not run correctly until you do.
# =============================================================================

# Telegram Stars Payment Configuration
STARS_ENABLED = True  # Set to True to enable Telegram Stars payments
# Note: Requires pyTelegramBotAPI 4.16.0+ for Stars support

# Language configuration
DEFAULT_LANGUAGE = "en"  # Default language
SUPPORTED_LANGUAGES = ["en", "km"]  # English and Khmer

# Translations dictionary
TRANSLATIONS = {
    "en": {
        # Language Selection
        "select_language": "🌍 Please select your language:",
        "language_english": "🇺🇸 English",
        "language_khmer": "🇰🇭 ខ្មែរ (Khmer)",
        "language_set": "✅ Language set to English!",
        
        # Main Menu
        "welcome": "🎉 Welcome to SMM Bot!\n\n💰 Current Balance: ${:.2f}\n\n📱 Choose an option below:",
        "main_menu_services": "🛍️ Services",
        "main_menu_add_funds": "💰 Add Funds",
        "main_menu_account_info": "👤 Account Info",
        "main_menu_help": "🛒 Tutorial",
        "main_menu_order_history": "📋 Order History",
        "main_menu_order_status": "🔍 Order Status",
        
        # Payment Methods
        "payment_methods_title": "💰 Add Funds to Your Account\n\n💵 Current Balance: ${:.2f}\n\n🔹 Choose your preferred payment method:",
        "payment_method_stars": "⭐ Pay with Stars",
        "payment_method_bakong": "💳 Pay with Bakong QR",
        "back_button": "🔙 Back",
        
        # Stars Payment
        "stars_title": "💵 Current Balance: ${:.2f}\n\n⭐ Choose Star Amount to Purchase:\n\n💡 Competitive Pricing (Better than Telegram!):\n✨ Special rates to save you money!\n\n👇 Select an amount below:",
        "stars_invoice_created": "✨ Payment Invoice Created!\n\n💰 Amount: {}⭐ = ${} USD\n🎯 Will be added to your balance\n\n👆 Tap the invoice above to pay!",
        "stars_payment_success": "⭐ Payment Successful!\n\n💰 Stars Paid: {}\n💵 USD Equivalent: ${:.2f}\n✅ Balance Added: ${:.2f}\n{}💰 New Balance: ${:.2f}\n\nThank you for using Telegram Stars! 🌟",
        "bonus_applied": "🎁 Bonus Added: ${:.2f}\n💰 Total Added: ${:.2f}\n",
        
        # Account Info
        "account_info": "👤 Account Information\n\n💰 Balance: ${:.2f} USD\n🆔 {}\n📦 Orders: {}",
        
        # Services
        "services_menu": "🛒 Choose a service category:",
        "tiktok_services": "🎥 TikTok Services",
        "telegram_services": "📱 Telegram Services",
        "facebook_services": "📘 Facebook Services",
        
        # Bakong Payment
        "bakong_amount_request": "💵 Current: ${:.2f}\n🟢 Enter amount (USD):",
        
        # Common
        "back_to_main": "🔙 Back to Main Menu",
        "back_button": "🔙 Back",
        "operation_canceled": "❌ Operation canceled.",
        "invalid_selection": "❌ Invalid selection. Please try again.",
        "error_occurred": "❌ An error occurred. Please try again.",
        "payment_disabled": "❌ Stars payments are currently disabled.",
        "contact_support": "Please contact support if this continues.",
        
        # Order History & Status
        "no_recent_orders": "📋 No recent orders.",
        "recent_orders_title": "📋 <b>Recent Orders</b>:\n",
        "no_orders_to_check": "🔍 No orders to check status for.",
        "detailed_order_status_title": "🔍 <b>Detailed Order Status (Last 10 Orders)</b>\n",
        "no_active_orders": "🔍 No active orders to check status for."
    },
    "km": {
        # Language Selection
        "select_language": "🌍 សូមជ្រើសរើសភាសារបស់អ្នក:",
        "language_english": "🇺🇸 English",
        "language_khmer": "🇰🇭 ខ្មែរ (Khmer)",
        "language_set": "✅ បានកំណត់ភាសាជាខ្មែរ!",
        
        # Main Menu
        "welcome": "🎉 សូមស្វាគមន៍មកកាន់ SMM Bot!\n\n💰 សមតុល្យបច្ចុប្បន្ន: ${:.2f}\n\n📱 សូមជ្រើសរើសជម្រើសខាងក្រោម:",
        "main_menu_services": "🛍️ សេវាកម្ម",
        "main_menu_add_funds": "💰 បញ្ចូលលុយ",
        "main_menu_account_info": "👤 ព័ត៌មានគណនី",
        "main_menu_help": "🛒 របៀបប្រើប្រាស់",
        "main_menu_order_history": "📋 ប្រវត្តិនៃការបញ្ជាទិញ",
        "main_menu_order_status": "🔍 ស្ថានភាពការបញ្ជាទិញ",
        
        # Payment Methods
        "payment_methods_title": "💰 បញ្ចូលលុយទៅក្នុងគណនីរបស់អ្នក\n\n💵 សមតុល្យបច្ចុប្បន្ន: ${:.2f}\n\n🔹 សូមជ្រើសរើសវិធីបង់ប្រាក់ដែលអ្នកចង់បាន:",
        "payment_method_stars": "⭐ បង់ប្រាក់ដោយ Stars",
        "payment_method_bakong": "💳 បង់ប្រាក់ដោយ Bakong QR",
        "back_button": "🔙 ត្រឡប់",
        
        # Stars Payment
        "stars_title": "💵 សមតុល្យបច្ចុប្បន្ន: ${:.2f}\n\n⭐ ជ្រើសរើសចំនួន Star ដែលត្រូវទិញ:\n\n💡 តម្លៃប្រកួតប្រជែង (ល្អជាង Telegram!):\n✨ អត្រាពិសេសដើម្បីសន្សំលុយរបស់អ្នក!\n\n👇 ជ្រើសរើសចំនួនខាងក្រោម:",
        "stars_invoice_created": "✨ វិក្កយបត្របង់ប្រាក់ត្រូវបានបង្កើត!\n\n💰 ចំនួន: {}⭐ = ${} USD\n🎯 នឹងត្រូវបានបន្ថែមទៅសមតុល្យរបស់អ្នក\n\n👆 ចុចលើវិក្កយបត្រខាងលើដើម្បីបង់ប្រាក់!",
        "stars_payment_success": "⭐ ការបង់ប្រាក់បានជោគជ័យ!\n\n💰 Stars បានបង់: {}\n💵 USD ស្មើនឹង: ${:.2f}\n✅ សមតុល្យបានបន្ថែម: ${:.2f}\n{}💰 សមតុល្យថ្មី: ${:.2f}\n\nអរគុណសម្រាប់ការប្រើប្រាស់ Telegram Stars! 🌟",
        "bonus_applied": "🎁 បូណុសបានបន្ថែម: ${:.2f}\n💰 សរុបបានបន្ថែម: ${:.2f}\n",
        
        # Account Info
        "account_info": "👤 ព័ត៌មានគណនី\n\n💰 សមតុល្យ: ${:.2f} USD\n🆔 {}\n📦 ការបញ្ជាទិញ: {}",
        
        # Services
        "services_menu": "🛒 ជ្រើសរើសប្រភេទសេវាកម្ម:",
        "tiktok_services": "🎥 សេវាកម្ម TikTok",
        "telegram_services": "📱 សេវាកម្ម Telegram",
        "facebook_services": "📘 សេវាកម្ម Facebook",
        
        # Bakong Payment
        "bakong_amount_request": "💵 សមតុល្យបច្ចុប្បន្ន: ${:.2f}\n\n តើអ្នកចង់បញ្ជូលប្រាក់ចំនួនប៉ុន្មាន $?\n\nឧទាហរណ៍បើសិនជាចង់ដាក់ 1$ ត្រូវសរសេរលេខ 1",
        
        # Common
        "back_to_main": "🔙 ត្រឡប់ទៅម៉ឺនុយដើម",
        "back_button": "🔙 ត្រឡប់",
        "operation_canceled": "❌ ប្រតិបត្តិការត្រូវបានបោះបង់។",
        "invalid_selection": "❌ ការជ្រើសរើសមិនត្រឹមត្រូវ។ សូមព្យាយាមម្តងទៀត។",
        "error_occurred": "❌ មានកំហុសកើតឡើង។ សូមព្យាយាមម្តងទៀត។",
        "payment_disabled": "❌ ការបង់ប្រាក់ Stars ត្រូវបានបិទបច្ចុប្បន្ន។",
        "contact_support": "សូមទាក់ទងផ្នែកគាំទ្រប្រសិនបើបន្ត។",
        
        # Order History & Status
        "no_recent_orders": "📋 មិនមានការបញ្ជាទិញថ្មីៗ។",
        "recent_orders_title": "📋 <b>ការបញ្ជាទិញថ្មីៗ</b>:\n",
        "no_orders_to_check": "🔍 មិនមានការបញ្ជាទិញសម្រាប់ពិនិត្យស្ថានភាព។",
        "detailed_order_status_title": "🔍 <b>ស្ថានភាពការបញ្ជាទិញលម្អិត (10 ចុងក្រោយ)</b>\n",
        "no_active_orders": "🔍 មិនមានការបញ្ជាទិញសកម្មសម្រាប់ពិនិត្យ។"
    }
}

# Initialize logging to show all logs in the terminal
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Bot Token and Admins
BOT_TOKEN = '7656178814:AAH2LMeSoMkOU95YANHCszAt1ZI4dxqdlIE'
ADMIN_IDS = [7672298857, 1630035459]

# SMM API Configuration
SMM_API_URL = "https://chhean-smm.net/api/v2"
SMM_API_KEY = "8bf8bc269ff40c0f472aff557505a485" # Replace with your SMM API key

# Telegram Group IDs
PAYMENT_GROUP_ID = -1002892538350
ORDER_GROUP_ID = -1002727074126

# Optimized Media Sending
# To get the file IDs, send your media files to the bot and use a temporary handler to print the file_id.
# Replace these placeholder strings with the actual file IDs you obtain.
VIDEO_FILE_ID = 'BAACAgUAAxkDAALgSGifdFVyWa2Mjkoj67NtlX76XJ0qAALmHgAC9wAB-VSaHFswtq3PmTYE'
WELCOME_PHOTO_ID = 'AgACAgUAAxkBAALmAAFooAABlS4e_LivqwI422nieOASODIAArnIMRvs5wFV5iv6BcH-6iIBAAMCAAN5AAM2BA'

# Database File
DB_FILE = "bot_data.db"

# =============================================================================
# Service IDs from your SMM panel
TIKTOK_LIKES_SERVICE_ID = "411"
TIKTOK_VIEWS_SERVICE_ID = "412"
TIKTOK_SAVES_SERVICE_ID = "472"
TIKTOK_SHARES_SERVICE_ID = "473"
TIKTOK_FOLLOWERS_SERVICE_ID = "497"  # ✅ Correct TikTok Followers service ID
FB_PAGE_FOLLOWERS_ID = "474"
FB_PROFILE_FOLLOWERS_ID = "474"
FB_VIDEO_VIEWS_ID = "475"
FB_REACTIONS_LIKE_ID = "476"
FB_REACTIONS_LOVE_ID = "477"
FB_REACTIONS_WOW_ID = "479"
FB_REACTIONS_CARE_ID = "478"
FB_REACTIONS_HAHA_ID = "615"
FB_REACTIONS_SAD_ID = "481"
FB_REACTIONS_ANGRY_ID = "482"
TG_MEMBER_7DAY_ID = "464"
TG_MEMBER_30DAY_ID = "465"
TG_MEMBER_LIFETIME_ID = "466"
TG_VIEW_SERVICE_ID = "467"
TG_MIX_POSITIVE_REACTIONS_ID = "462"
TG_MIX_NEGATIVE_REACTIONS_ID = "463"

# Telegram Stars transactions tracking
stars_transactions = {}

# User language preferences (in memory cache)
user_languages = {}

# Thread pool for background tasks - Optimized for maximum speed
executor = ThreadPoolExecutor(max_workers=1000, thread_name_prefix="SMM-Bot")
# In-memory cache - Optimized for speed
user_cache = {}
cache_lock = threading.Lock()
CACHE_TIMEOUT = 600  # 10 minutes - longer cache for better performance

# Pre-computed keyboard cache for instant responses
keyboard_cache = {}
keyboard_cache_lock = threading.Lock()

# Response time tracking
response_times = []
response_time_lock = threading.Lock()
# User states
user_states = {}
transactions = {}
# Display name cache
display_name_cache = {}
display_name_lock = threading.Lock()
# Message rate limiting
message_count = {}
message_lock = threading.Lock()

# Service Configurations
SERVICES = {
    "100 Likes + 1K Views - $0.10": {"likes": 100, "views": 1000, "price": 0.10, "key": "tiktok_100"},
    "250 Likes + 2K Views - $0.18": {"likes": 250, "views": 2000, "price": 0.18, "key": "tiktok_250"},
    "500 Likes + 5K Views - $0.29": {"likes": 500, "views": 5000, "price": 0.29, "key": "tiktok_500"},
    "1K Likes + 10K Views - $0.45": {"likes": 1000, "views": 10000, "price": 0.45, "key": "tiktok_1k"},
    "2K Likes + 13K Views - $0.85": {"likes": 2000, "views": 13000, "price": 0.85, "key": "tiktok_2k"},
    "3K Likes + 15K Views - $1.29": {"likes": 3000, "views": 15000, "price": 1.29, "key": "tiktok_3k"},
    "5K Likes + 30K Views - $1.99": {"likes": 5000, "views": 30000, "price": 1.99, "key": "tiktok_5k"},
    "10K Likes + 50K Views - $3.89": {"likes": 10000, "views": 50000, "price": 3.89, "key": "tiktok_10k"},
    "20K Likes + 90K Views - $6.49": {"likes": 20000, "views": 90000, "price": 6.49, "key": "tiktok_20k"},
    "30K Likes + 130K Views - $9.49": {"likes": 30000, "views": 130000, "price": 9.49, "key": "tiktok_30k"},
    "40K Likes + 160K Views - $12.49": {"likes": 40000, "views": 160000, "price": 12.49, "key": "tiktok_40k"},
    "50K Likes + 190K Views - $13.49": {"likes": 50000, "views": 190000, "price": 13.49, "key": "tiktok_50k"},
    "100K Likes + 230K Views - $19.99": {"likes": 100000, "views": 230000, "price": 19.99, "key": "tiktok_100k"},
}
TIKTOK_VIEW_SERVICES = {
    "10K Views - $0.10": {"views": 10000, "price": 0.10, "key": "view_10k"},
    "20K Views - $0.15": {"views": 20000, "price": 0.15, "key": "view_20k"},
    "30K Views - $0.20": {"views": 30000, "price": 0.20, "key": "view_30k"},
    "40K Views - $0.25": {"views": 40000, "price": 0.25, "key": "view_40k"},
    "50K Views - $0.30": {"views": 50000, "price": 0.30, "key": "view_50k"},
    "60K Views - $0.36": {"views": 60000, "price": 0.36, "key": "view_60k"},
    "70K Views - $0.40": {"views": 70000, "price": 0.40, "key": "view_70k"},
    "80K Views - $0.45": {"views": 80000, "price": 0.45, "key": "view_80k"},
    "90K Views - $0.50": {"views": 90000, "price": 0.50, "key": "view_90k"},
    "100K Views - $1": {"views": 100000, "price": 1, "key": "view_100k"},
}
TIKTOK_SAVE_SERVICES = {
    "100 Saves - $0.12": {"quantity": 100, "price": 0.12, "key": "save_100"},
    "500 Saves - $0.60": {"quantity": 500, "price": 0.60, "key": "save_500"},
    "1K Saves - $1.10": {"quantity": 1000, "price": 1.10, "key": "save_1k"},
}
TIKTOK_SHARE_SERVICES = {
    "100 Shares - $0.25": {"quantity": 100, "price": 0.25, "key": "share_100"},
    "500 Shares - $1.00": {"quantity": 500, "price": 1.00, "key": "share_500"},
    "1K Shares - $1.50": {"quantity": 1000, "price": 1.50, "key": "share_1k"},
}
TIKTOK_FOLLOWERS_SERVICES = {
    "100 Followers - $0.45": {"quantity": 100, "price": 0.45, "key": "followers_100"},
    "500 Followers - $1.50": {"quantity": 500, "price": 1.50, "key": "followers_500"},
    "1K Followers - $2.50": {"quantity": 1000, "price": 2.50, "key": "followers_1k"},
    "2K Followers - $4.50": {"quantity": 2000, "price": 4.50, "key": "followers_2k"},
    "5K Followers - $11.50": {"quantity": 5000, "price": 11.50, "key": "followers_5k"},
    "10K Followers - $20.00": {"quantity": 10000, "price": 20.00, "key": "followers_10k"},
}  # ✅ Using Service ID: 13 (HQ Profiles, Max 1M, Day 100K speed)
FB_PAGE_FOLLOWERS = {
    "500 Page Followers - $1.30": {"quantity": 500, "price": 1.30, "key": "fb_page_500"},
    "1K Page Followers - $2.00": {"quantity": 1000, "price": 2.00, "key": "fb_page_1k"},
    "5K Page Followers - $7.80": {"quantity": 5000, "price": 7.80, "key": "fb_page_5k"},
    "10K Page Followers - $13.00": {"quantity": 10000, "price": 13.00, "key": "fb_page_10k"},
}
FB_PROFILE_FOLLOWERS = {
    "500 Profile Followers - $1": {"quantity": 500, "price": 1, "key": "fb_prof_500"},
    "1K Profile Followers - $1.5": {"quantity": 1000, "price": 1.50, "key": "fb_prof_1k"},
    "5K Profile Followers - $7.50": {"quantity": 5000, "price": 7.50, "key": "fb_prof_5k"},
    "10K Profile Followers - $13.00": {"quantity": 10000, "price": 13.00, "key": "fb_prof_10k"},
}
FB_VIDEO_VIEWS = {
    "1K Video Views - $0.20": {"quantity": 1000, "price": 0.20, "key": "fb_view_1k"},
    "5K Video Views - $1.00": {"quantity": 5000, "price": 1.00, "key": "fb_view_5k"},
    "10K Video Views - $1.75": {"quantity": 10000, "price": 1.75, "key": "fb_view_10k"},
    "100K Video Views - $13.00": {"quantity": 100000, "price": 13.00, "key": "fb_view_100k"},
}
FB_REACTIONS = {
    "👍 Post Likes - 100 - $0.19": {"quantity": 100, "price": 0.19, "service_id": FB_REACTIONS_LIKE_ID, "key": "fb_like_100"},
    "👍 Post Likes - 500 - $0.85": {"quantity": 500, "price": 0.85, "service_id": FB_REACTIONS_LIKE_ID, "key": "fb_like_500"},
    "👍 Post Likes - 1K - $1.50": {"quantity": 1000, "price": 1.50, "service_id": FB_REACTIONS_LIKE_ID, "key": "fb_like_1k"},
    "💖 Post Love - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_LOVE_ID, "key": "fb_love_100"},
    "💖 Post Love - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_LOVE_ID, "key": "fb_love_500"},
    "💖 Post Love - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_LOVE_ID, "key": "fb_love_1k"},
    "😮 Post Wow - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_WOW_ID, "key": "fb_wow_100"},
    "😮 Post Wow - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_WOW_ID, "key": "fb_wow_500"},
    "😮 Post Wow - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_WOW_ID, "key": "fb_wow_1k"},
    "🥰 Post Care - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_CARE_ID, "key": "fb_care_100"},
    "🥰 Post Care - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_CARE_ID, "key": "fb_care_500"},
    "🥰 Post Care - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_CARE_ID, "key": "fb_care_1k"},
    "😂 Post Haha - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_HAHA_ID, "key": "fb_haha_100"},
    "😂 Post Haha - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_HAHA_ID, "key": "fb_haha_500"},
    "😂 Post Haha - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_HAHA_ID, "key": "fb_haha_1k"},
    "😭 Post Sad - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_SAD_ID, "key": "fb_sad_100"},
    "😭 Post Sad - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_SAD_ID, "key": "fb_sad_500"},
    "😭 Post Sad - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_SAD_ID, "key": "fb_sad_1k"},
    "😡 Post Angry - 100 - $0.25": {"quantity": 100, "price": 0.25, "service_id": FB_REACTIONS_ANGRY_ID, "key": "fb_angry_100"},
    "😡 Post Angry - 500 - $0.95": {"quantity": 500, "price": 0.95, "service_id": FB_REACTIONS_ANGRY_ID, "key": "fb_angry_500"},
    "😡 Post Angry - 1K - $1.75": {"quantity": 1000, "price": 1.75, "service_id": FB_REACTIONS_ANGRY_ID, "key": "fb_angry_1k"},
}
TELEGRAM_MEMBER_7DAY = {
    "500 Members (7-Day) - $0.70": {"members": 500, "price": 0.70, "duration": "7-day", "key": "tg_7day_500"},
    "1K Members (7-Day) - $1.40": {"members": 1000, "price": 1.40, "duration": "7-day", "key": "tg_7day_1k"},
    "3K Members (7-Day) - $3.20": {"members": 3000, "price": 3.20, "duration": "7-day", "key": "tg_7day_3k"},
}
TELEGRAM_MEMBER_30DAY = {
    "500 Members (30-Day) - $0.90": {"members": 500, "price": 0.90, "duration": "30-day", "key": "tg_30day_500"},
    "1K Members (30-Day) - $2.50": {"members": 1000, "price": 2.50, "duration": "30-day", "key": "tg_30day_1k"},
    "3K Members (30-Day) - $6.00": {"members": 3000, "price": 6.00, "duration": "30-day", "key": "tg_30day_3k"},
}
TELEGRAM_MEMBER_LIFETIME = {
    "500 Members (Lifetime) - $2.50": {"members": 500, "price": 2.50, "duration": "Lifetime", "key": "tg_life_500"},
    "1K Members (Lifetime) - $4.50": {"members": 1000, "price": 4.50, "duration": "Lifetime", "key": "tg_life_1k"},
    "3K Members (Lifetime) - $12.00": {"members": 3000, "price": 12.00, "duration": "Lifetime", "key": "tg_life_3k"},
}
TELEGRAM_VIEW_SERVICES = {
    "1K Views - $0.10": {"views": 1000, "price": 0.10, "key": "tg_view_1k"},
    "5K Views - $0.35": {"views": 5000, "price": 0.35, "key": "tg_view_5k"},
    "10K Views - $0.60": {"views": 10000, "price": 0.60, "key": "tg_view_10k"},
    "100K Views - $5.00": {"views": 100000, "price": 5.00, "key": "tg_view_100k"},
}
TELEGRAM_MIX_POSITIVE_REACTIONS = {
    "100 Positive Reactions (👍❤️🔥🎉😁) + Views - $0.30": {"quantity": 100, "price": 0.30, "key": "tg_pos_100"},
    "1K Positive Reactions (👍❤️🔥🎉😁) + Views - $1.50": {"quantity": 1000, "price": 1.50, "key": "tg_pos_1k"},
}
TELEGRAM_MIX_NEGATIVE_REACTIONS = {
    "100 Negative Reactions (👎😱💩😢🤮) + Views - $0.30": {"quantity": 100, "price": 0.30, "key": "tg_neg_100"},
    "1K Negative Reactions (👎😱💩😢🤮) + Views - $1.50": {"quantity": 1000, "price": 1.50, "key": "tg_neg_1k"},
}

# Thread pool for background tasks
executor = ThreadPoolExecutor(max_workers=500)
# In-memory cache
user_cache = {}
cache_lock = threading.Lock()
CACHE_TIMEOUT = 300 # 5 minutes
# User states
user_states = {}
transactions = {}
# Display name cache
display_name_cache = {}
display_name_lock = threading.Lock()
# Message rate limiting
message_count = {}
message_lock = threading.Lock()

# Database Manager
class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db_lock = threading.Lock()  # Add thread safety lock
        self.init_database()
    
    def get_connection(self):
        """Create a new connection for each thread to avoid SQLite threading issues"""
        conn = sqlite3.connect(self.db_file, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")  # Better for concurrent access
        conn.execute("PRAGMA busy_timeout=30000")  # 30 second timeout for locks
        return conn
    def init_database(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0.0,
                registration_date TEXT,
                total_orders INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0.0,
                last_activity TEXT,
                language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                package TEXT,
                url TEXT,
                price REAL,
                likes_order_id TEXT,
                views_order_id TEXT,
                status TEXT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )''')
            # Add balance history table
            conn.execute('''CREATE TABLE IF NOT EXISTS balance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                type TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )''')
            # Add bakong transactions table for duplicate prevention
            conn.execute('''CREATE TABLE IF NOT EXISTS bakong_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE,
                transaction_hash TEXT,
                user_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                message_text TEXT,
                status TEXT,
                total_users INTEGER,
                successful_sends INTEGER DEFAULT 0,
                failed_sends INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )''')
            # Add bonus rules table
            conn.execute('''CREATE TABLE IF NOT EXISTS bonus_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                min_amount REAL NOT NULL,
                max_amount REAL NOT NULL,
                bonus_percentage REAL NOT NULL,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (created_by) REFERENCES users (user_id)
            )''')
            # Add Telegram Stars transactions table
            conn.execute('''CREATE TABLE IF NOT EXISTS stars_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                transaction_type TEXT NOT NULL,
                usd_amount REAL NOT NULL,
                stars_amount INTEGER NOT NULL,
                telegram_charge_id TEXT UNIQUE,
                invoice_payload TEXT,
                service_name TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )''')
            cursor = conn.execute("PRAGMA table_info(orders)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'package' not in columns:
                conn.execute("ALTER TABLE orders ADD COLUMN package TEXT")
                logger.info("✅ Added missing column: package")
            if 'error' not in columns:
                conn.execute("ALTER TABLE orders ADD COLUMN error TEXT")
                logger.info("✅ Added missing column: error")
            conn.commit()
    def add_user(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.execute(
                'INSERT OR IGNORE INTO users (user_id, registration_date) VALUES (?, ?)',
                (user_id, time.strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            return cursor.rowcount > 0
    def get_user(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'user_id': row[0], 'balance': row[1], 'registration_date': row[2],
                    'total_orders': row[3], 'total_spent': row[4], 'last_activity': row[5],
                    'language': row[6] if len(row) > 6 else 'en'
                }
            return None
    def update_user_balance(self, user_id, balance):
        with self.get_connection() as conn:
            conn.execute(
                '''INSERT OR REPLACE INTO users
                (user_id, balance, registration_date, total_orders, total_spent, last_activity, created_at, updated_at)
                VALUES (?, ?, COALESCE((SELECT registration_date FROM users WHERE user_id = ?), ?),
                             COALESCE((SELECT total_orders FROM users WHERE user_id = ?), 0),
                             COALESCE((SELECT total_spent FROM users WHERE user_id = ?), 0),
                             ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)''',
                (user_id, balance, user_id, time.strftime('%Y-%m-%d %H:%M:%S'), user_id, user_id,
                 time.strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
    
    def update_user_language(self, user_id, language):
        """Update user's language preference"""
        with self.get_connection() as conn:
            conn.execute(
                '''INSERT OR REPLACE INTO users
                (user_id, balance, registration_date, total_orders, total_spent, last_activity, language, created_at, updated_at)
                VALUES (?, COALESCE((SELECT balance FROM users WHERE user_id = ?), 0),
                           COALESCE((SELECT registration_date FROM users WHERE user_id = ?), ?),
                           COALESCE((SELECT total_orders FROM users WHERE user_id = ?), 0),
                           COALESCE((SELECT total_spent FROM users WHERE user_id = ?), 0),
                           ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)''',
                (user_id, user_id, user_id, time.strftime('%Y-%m-%d %H:%M:%S'), user_id, user_id,
                 time.strftime('%Y-%m-%d %H:%M:%S'), language)
            )
            conn.commit()
    
    def add_order(self, user_id, order_data):
        with self.get_connection() as conn:
            conn.execute('''INSERT INTO orders
                (user_id, package, url, price, likes_order_id, views_order_id, status, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id,
                 order_data.get('package'),
                 order_data.get('url'),
                 order_data.get('price'),
                 order_data.get('likes_order_id'),
                 order_data.get('views_order_id'),
                 order_data.get('status'),
                 order_data.get('error'))
            )
            conn.commit()
    def get_user_orders(self, user_id, limit=5):
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ?''',
                                  (user_id, limit))
            return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    
    def get_orders_by_date_range(self, start_date, end_date, status_filter=None):
        """Get all orders within a date range, optionally filtered by status"""
        with self.get_connection() as conn:
            if status_filter:
                cursor = conn.execute('''SELECT * FROM orders 
                                       WHERE date(created_at) BETWEEN ? AND ? 
                                       AND (status = ? OR status IS NULL)
                                       ORDER BY created_at DESC''',
                                    (start_date, end_date, status_filter))
            else:
                cursor = conn.execute('''SELECT * FROM orders 
                                       WHERE date(created_at) BETWEEN ? AND ? 
                                       ORDER BY created_at DESC''',
                                    (start_date, end_date))
            return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    
    def check_bakong_transaction_exists(self, transaction_id):
        """Check if a Bakong transaction ID already exists"""
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT id FROM bakong_transactions WHERE transaction_id = ?', (transaction_id,))
            return cursor.fetchone() is not None
    
    def add_bakong_transaction(self, transaction_id, transaction_hash, user_id, amount):
        """Add a new Bakong transaction record"""
        with self.get_connection() as conn:
            try:
                conn.execute('''INSERT INTO bakong_transactions 
                              (transaction_id, transaction_hash, user_id, amount) 
                              VALUES (?, ?, ?, ?)''',
                            (transaction_id, transaction_hash, user_id, amount))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Transaction ID already exists
                return False
    def get_all_user_ids(self):
        conn = self.get_connection()
        try:
            cursor = conn.execute('SELECT user_id FROM users')
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
    def add_broadcast(self, admin_id, message_text):
        conn = self.get_connection()
        try:
            cursor = conn.execute('''INSERT INTO broadcasts
                (admin_id, message_text, status, total_users, created_at)
                VALUES (?, ?, ?, ?, ?)''',
                (admin_id, message_text, 'pending', 0, time.strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    def update_broadcast_stats(self, broadcast_id, successful, failed):
        conn = self.get_connection()
        try:
            conn.execute('''UPDATE broadcasts SET successful_sends = ?, failed_sends = ?, status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?''',
                           (successful, failed, broadcast_id))
            conn.commit()
        finally:
            conn.close()
    def get_bot_stats(self):
        with self.get_connection() as conn:
            total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
            total_balance = conn.execute('SELECT SUM(balance) FROM users').fetchone()[0] or 0.0
            users_with_balance = conn.execute('SELECT COUNT(*) FROM users WHERE balance > 0').fetchone()[0]
            orders_today = conn.execute("SELECT COUNT(*) FROM orders WHERE DATE(created_at) = DATE('now')").fetchone()[0]
            return {
                'total_users': total_users,
                'total_balance': total_balance,
                'users_with_balance': users_with_balance,
                'orders_today': orders_today
            }
    def log_balance_change(self, user_id, amount, type, description):
        """Log a balance change to the history table"""
        with self.get_connection() as conn:
            conn.execute('''INSERT INTO balance_history
                (user_id, amount, type, description)
                VALUES (?, ?, ?, ?)''',
                (user_id, amount, type, description)
            )
            conn.commit()
    def get_balance_history(self, user_id, limit=10):
        """Get balance history for a user"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM balance_history
                WHERE user_id = ? ORDER BY created_at DESC LIMIT ?''',
                (user_id, limit))
            return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    def get_daily_topup_stats(self):
        """
        Calculates the total top-up amount from "deposit" type transactions
        for the current day in Cambodia time (UTC+7).
        """
        try:
            with self.get_connection() as conn:
                # Get the current date in Cambodia's timezone (UTC+7)
                now_cambodia = datetime.utcnow() + timedelta(hours=7)
                today_str = now_cambodia.strftime('%Y-%m-%d')
                
                cursor = conn.execute('''
                    SELECT SUM(amount) FROM balance_history
                    WHERE type = 'deposit' AND CAST(created_at AS TEXT) LIKE ?
                ''', (today_str + '%',))
                total_topup = cursor.fetchone()[0] or 0.0
                return total_topup
        except Exception as e:
            logger.error(f"Error getting daily topup stats: {e}")
            return 0.0

    def add_bonus_rule(self, min_amount, max_amount, bonus_percentage, created_by):
        """Add a new bonus rule"""
        with self.get_connection() as conn:
            cursor = conn.execute('''INSERT INTO bonus_rules
                (min_amount, max_amount, bonus_percentage, created_by)
                VALUES (?, ?, ?, ?)''',
                (min_amount, max_amount, bonus_percentage, created_by)
            )
            conn.commit()
            return cursor.lastrowid

    def get_active_bonus_rules(self):
        """Get all active bonus rules"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM bonus_rules
                WHERE is_active = 1 ORDER BY min_amount ASC''')
            return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    def delete_bonus_rule(self, rule_id):
        """Delete a bonus rule"""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM bonus_rules WHERE id = ?', (rule_id,))
            conn.commit()

    def deactivate_all_bonus_rules(self, created_by=None):
        """Deactivate all bonus rules"""
        with self.get_connection() as conn:
            conn.execute('UPDATE bonus_rules SET is_active = 0')
            conn.commit()

    def get_applicable_bonus(self, amount):
        """Get the applicable bonus for a given top-up amount"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM bonus_rules
                WHERE is_active = 1 AND ? >= min_amount AND ? <= max_amount
                ORDER BY bonus_percentage DESC LIMIT 1''',
                (amount, amount))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def add_stars_transaction(self, user_id, transaction_type, usd_amount, stars_amount, 
                             invoice_payload, service_name=None):
        """Add a new Stars transaction record"""
        with self.get_connection() as conn:
            cursor = conn.execute('''INSERT INTO stars_transactions
                (user_id, transaction_type, usd_amount, stars_amount, invoice_payload, service_name, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (user_id, transaction_type, usd_amount, stars_amount, invoice_payload, service_name, 'pending')
            )
            conn.commit()
            return cursor.lastrowid

    def complete_stars_transaction(self, user_id, invoice_payload, telegram_charge_id):
        """Mark a Stars transaction as completed"""
        with self.get_connection() as conn:
            conn.execute('''UPDATE stars_transactions 
                SET status = 'completed', telegram_charge_id = ?, completed_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND invoice_payload = ? AND status = 'pending' ''',
                (telegram_charge_id, user_id, invoice_payload)
            )
            conn.commit()

    def get_stars_transaction(self, user_id, invoice_payload):
        """Get a Stars transaction by user and payload"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM stars_transactions 
                WHERE user_id = ? AND invoice_payload = ? AND status = 'pending' 
                ORDER BY created_at DESC LIMIT 1''',
                (user_id, invoice_payload)
            )
            result = cursor.fetchone()
            if result:
                return dict(zip([column[0] for column in cursor.description], result))
            return None

    def get_user_stars_history(self, user_id, limit=10):
        """Get user's Stars transaction history"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM stars_transactions 
                WHERE user_id = ? ORDER BY created_at DESC LIMIT ?''',
                (user_id, limit)
            )
            return [dict(zip([column[0] for column in cursor.description], row)) 
                   for row in cursor.fetchall()]

    def get_stars_stats(self, days=30):
        """Get Stars payment statistics"""
        with self.get_connection() as conn:
            cursor = conn.execute('''SELECT 
                COUNT(*) as total_transactions,
                COALESCE(SUM(usd_amount), 0) as total_usd,
                COALESCE(SUM(stars_amount), 0) as total_stars,
                COALESCE(AVG(usd_amount), 0) as avg_usd
                FROM stars_transactions 
                WHERE status = 'completed' 
                AND created_at >= datetime('now', '-{} days')'''.format(days)
            )
            result = cursor.fetchone()
            if result:
                stats = dict(zip([column[0] for column in cursor.description], result))
                # Ensure all values are numbers, not None
                return {
                    "total_transactions": stats.get("total_transactions", 0) or 0,
                    "total_usd": float(stats.get("total_usd", 0) or 0),
                    "total_stars": int(stats.get("total_stars", 0) or 0),
                    "avg_usd": float(stats.get("avg_usd", 0) or 0)
                }
            return {"total_transactions": 0, "total_usd": 0.0, "total_stars": 0, "avg_usd": 0.0}

db = Database(DB_FILE)
# Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Helper Functions
def get_user_language(user_id):
    """Get user's preferred language"""
    if user_id in user_languages:
        return user_languages[user_id]
    
    # Try to get from database
    try:
        user = db.get_user(user_id)
        if user and 'language' in user:
            lang = user['language'] or DEFAULT_LANGUAGE
            user_languages[user_id] = lang
            return lang
    except Exception as e:
        logger.error(f"Error getting user language: {e}")
    
    # Default language
    user_languages[user_id] = DEFAULT_LANGUAGE
    return DEFAULT_LANGUAGE

def set_user_language(user_id, language):
    """Set user's preferred language"""
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    user_languages[user_id] = language
    
    # Update database
    try:
        db.update_user_language(user_id, language)
    except Exception as e:
        logger.error(f"Error setting user language: {e}")

def get_text(user_id, key, *args, **kwargs):
    """Get translated text for user"""
    language = get_user_language(user_id)
    
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        text = TRANSLATIONS[language][key]
    elif key in TRANSLATIONS[DEFAULT_LANGUAGE]:
        text = TRANSLATIONS[DEFAULT_LANGUAGE][key]
    else:
        return f"Missing translation: {key}"
    
    # Format text with arguments
    try:
        if args or kwargs:
            return text.format(*args, **kwargs)
        return text
    except Exception as e:
        logger.error(f"Error formatting text '{key}': {e}")
        return text

def get_cached_user(user_id):
    with cache_lock:
        if user_id in user_cache:
            user, timestamp = user_cache[user_id]
            if time.time() - timestamp < CACHE_TIMEOUT:
                return user
    try:
        user = db.get_user(user_id)
        if user:
            with cache_lock:
                user_cache[user_id] = (user, time.time())
            return user
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
    return {'user_id': user_id, 'balance': 0.0}
def update_cached_user_balance(user_id, balance):
    db.update_user_balance(user_id, balance)
    with cache_lock:
        user_cache[user_id] = ({
            'user_id': user_id,
            'balance': balance,
            'registration_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }, time.time())
def add_user_funds(user_id, amount, description="User deposit", apply_bonus=True):
    """Add funds to user and log the transaction"""
    total_amount = amount
    bonus_amount = 0

    # Check for applicable bonus if this is a user deposit
    if apply_bonus and "deposit" in description.lower():
        bonus_rule = db.get_applicable_bonus(amount)
        if bonus_rule:
            bonus_amount = amount * (bonus_rule['bonus_percentage'] / 100)
            total_amount = amount + bonus_amount

            # Log the original deposit
            db.log_balance_change(user_id, amount, "deposit", description)
            # Log the bonus separately
            db.log_balance_change(user_id, bonus_amount, "bonus",
                f"Bonus {bonus_rule['bonus_percentage']}% for ${amount:.2f} deposit")
        else:
            # Log the transaction normally
            db.log_balance_change(user_id, amount, "deposit", description)
    else:
        # Log the transaction normally
        db.log_balance_change(user_id, amount, "deposit", description)

    # Update balance
    user = get_cached_user(user_id)
    new_balance = user['balance'] + total_amount
    update_cached_user_balance(user_id, new_balance)

    return new_balance, bonus_amount
def deduct_user_funds(user_id, amount, description="Service purchase"):
    """Deduct funds from user and log the transaction"""
    # Log the transaction
    db.log_balance_change(user_id, -amount, "spending", description)
    # Update balance
    user = get_cached_user(user_id)
    new_balance = user['balance'] - amount
    update_cached_user_balance(user_id, new_balance)
    return new_balance
def refund_user_funds(user_id, amount, description="Order refund"):
    """Refund funds to user and log the transaction"""
    # Log the transaction
    db.log_balance_change(user_id, amount, "refund", description)
    # Update balance
    user = get_cached_user(user_id)
    new_balance = user['balance'] + amount
    update_cached_user_balance(user_id, new_balance)
    return new_balance
def adjust_user_funds(user_id, amount, description="Admin adjustment"):
    """Adjust user funds (positive for add, negative for deduct) and log the transaction"""
    # Determine transaction type
    transaction_type = "deposit" if amount > 0 else "withdrawal"
    # Log the transaction
    db.log_balance_change(user_id, amount, transaction_type, description)
    # Update balance
    user = get_cached_user(user_id)
    new_balance = user['balance'] + amount
    update_cached_user_balance(user_id, new_balance)
    return new_balance
def refund_user(user_id, amount, reason="Order canceled"):
    """Refund amount to user and notify them"""
    try:
        # Use the dedicated refund function that logs the history
        new_balance = refund_user_funds(user_id, amount, reason)
        bot.send_message(
            user_id,
            f"""🔄 Refund issued: ${amount:.2f}
💬 Reason: {reason}
💰 New balance: ${new_balance:.2f}"""
        )
        # Log to payment group
        send_with_retry(
            PAYMENT_GROUP_ID,
            f"""🔄 <b>Refund Issued</b>
👤 {get_user_display_name(user_id)}
🆔 {user_id}
💵 ${amount:.2f}
📝 {reason}""",
            parse_mode='HTML'
        )
        logger.info(f"✅ Refunded ${amount:.2f} to user {user_id} - {reason}")
    except Exception as e:
        logger.error(f"❌ Failed to refund user {user_id}: {e}")
def get_user_display_name(user_id):
    with display_name_lock:
        if user_id in display_name_cache:
            name, ts = display_name_cache[user_id]
            if time.time() - ts < 3600:
                return name
    try:
        user_info = bot.get_chat(user_id)
        if user_info.username:
            name = f"@{user_info.username}"
        elif user_info.first_name and user_info.last_name:
            name = f"{user_info.first_name} {user_info.last_name}"
        elif user_info.first_name:
            name = user_info.first_name
        else:
            name = f"User {user_id}"
        with display_name_lock:
            display_name_cache[user_id] = (name, time.time())
        return name
    except Exception as e:
        logger.error(f"Error getting display name for {user_id}: {e}")
        name = f"User {user_id}"
        with display_name_lock:
            display_name_cache[user_id] = (name, time.time())
        return name
def is_admin(user_id):
    return user_id in ADMIN_IDS
def check_rate_limit(user_id, limit=10, window=60):
    now = time.time()
    with message_lock:
        if user_id not in message_count:
            message_count[user_id] = []
        message_count[user_id] = [t for t in message_count[user_id] if now - t < window]
        if len(message_count[user_id]) >= limit:
            return False
        message_count[user_id].append(now)
        return True
def send_with_retry(chat_id, text, retries=3, parse_mode=None):
    for i in range(retries):
        try:
            bot.send_message(chat_id, text, parse_mode=parse_mode)
            return True
        except Exception as e:
            logger.warning(f"Failed to send message to {chat_id} (attempt {i+1}): {e}")
            time.sleep(2)
    return False

# Keyboards
def create_main_menu_keyboard(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    if user_id:
        # Use translated text
        keyboard.add(
            types.KeyboardButton(get_text(user_id, "main_menu_account_info")),
            types.KeyboardButton(get_text(user_id, "main_menu_add_funds"))
        )
        keyboard.add(
            types.KeyboardButton(get_text(user_id, "main_menu_services")),
            types.KeyboardButton("🌐 Mini App")
        )
        keyboard.add(
            types.KeyboardButton(get_text(user_id, "main_menu_order_history")),
            types.KeyboardButton(get_text(user_id, "main_menu_order_status"))
        )
        keyboard.add(
            types.KeyboardButton(get_text(user_id, "main_menu_help"))
        )
    else:
        # Fallback to bilingual buttons
        keyboard.add(
            types.KeyboardButton("👤 Account/អាខោន"),
            types.KeyboardButton("💰 Add Funds/ដាក់លុយ")
        )
        keyboard.add(
            types.KeyboardButton("🛍️ Services"),
            types.KeyboardButton("🌐 Mini App")
        )
        keyboard.add(
            types.KeyboardButton("📋 Order History/ប្រវត្តិនៃការបញ្ជាទិញ"),
            types.KeyboardButton("🔍 Order Status/ស្ថានភាពការបញ្ជាទិញ")
        )
        keyboard.add(
            types.KeyboardButton("🛒 Tutorial/របៀបប្រើប្រាស់")
        )
    return keyboard
def create_services_menu_keyboard(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if user_id:
        keyboard.add(
            types.KeyboardButton(get_text(user_id, "tiktok_services")),
            types.KeyboardButton(get_text(user_id, "telegram_services")),
            types.KeyboardButton(get_text(user_id, "facebook_services")),
            types.KeyboardButton(get_text(user_id, "back_to_main"))
        )
    else:
        # Fallback to bilingual
        keyboard.add(
            types.KeyboardButton("🎥 TikTok Services/សេវាកម្ម TikTok"),
            types.KeyboardButton("📱 Telegram Services/សេវាកម្ម Telegram"),
            types.KeyboardButton("📘 Facebook Services/សេវាកម្ម Facebook"),
            types.KeyboardButton("🔙 Back/ត្រឡប់")
        )
    return keyboard
def create_facebook_services_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("👥 Facebook Page Followers"),
        types.KeyboardButton("👤 Facebook Profile Followers"),
        types.KeyboardButton("👀 Facebook Video Views"),
        types.KeyboardButton("❤️ Facebook Reactions"),
        types.KeyboardButton("🔙 Back")
    )
    return keyboard
def create_tiktok_services_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("👥 TikTok Followers"),
        types.KeyboardButton("❤️ TikTok Likes & Views"),
        types.KeyboardButton("👀 TikTok Views Only"),
        types.KeyboardButton("💾 TikTok Saves"),
        types.KeyboardButton("📤 TikTok Shares"),
        types.KeyboardButton("🔙 Back")
    )
    return keyboard
def create_tiktok_views_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for name in TIKTOK_VIEW_SERVICES:
        keyboard.add(types.KeyboardButton(name))
    keyboard.add(types.KeyboardButton("🔙 Back"))
    return keyboard
def create_telegram_services_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("👥 Telegram Members"),
        types.KeyboardButton("👀 Telegram Views"),
        types.KeyboardButton("😊 Mix Positive Reactions"),
        types.KeyboardButton("😡 Mix Negative Reactions"),
        types.KeyboardButton("🔙 Back")
    )
    return keyboard
def create_telegram_member_duration_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("⏳ 7-Day Members"),
        types.KeyboardButton("📆 30-Day Members"),
        types.KeyboardButton("♾️ Lifetime Members"),
        types.KeyboardButton("🔙 Back")
    )
    return keyboard
def create_telegram_member_services_keyboard(service_dict):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in service_dict:
        keyboard.add(types.KeyboardButton(name))
    keyboard.add(types.KeyboardButton("🔙 Back"))
    return keyboard
def create_telegram_view_services_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TELEGRAM_VIEW_SERVICES:
        keyboard.add(types.KeyboardButton(name))
    keyboard.add(types.KeyboardButton("🔙 Back"))
    return keyboard
def create_back_keyboard(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id:
        back_text = get_text(user_id, "back_to_main")
    else:
        # Fallback to bilingual
        back_text = "🔙 Back/ត្រឡប់"
    keyboard.add(types.KeyboardButton(back_text))
    return keyboard
def create_order_confirmation_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("✅ Confirm Order"), types.KeyboardButton("❌ Cancel Order"))
    return keyboard
def create_admin_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("👥 User Mgmt"),
        types.KeyboardButton("💸 Add Funds")
    )
    keyboard.add(
        types.KeyboardButton("💸 Remove Funds"),
        types.KeyboardButton("📊 Bot Stats")
    )
    keyboard.add(
        types.KeyboardButton("🎁 Bonus Mgmt"),
        types.KeyboardButton("📤 Broadcast")
    )
    keyboard.add(
        types.KeyboardButton("👥 All Users"),
        types.KeyboardButton("📜 History")
    )
    keyboard.add(
        types.KeyboardButton("💸 Topup Stats"), # NEW BUTTON ADDED HERE
        types.KeyboardButton("⭐ Stars Stats")
    )
    keyboard.add(
        types.KeyboardButton("🎥 TikTok Bulk Retry")
    )
    keyboard.add(
        types.KeyboardButton("🔙 Back to User")
    )
    return keyboard

def create_bulk_retry_keyboard():
    """Create keyboard for bulk retry time period selection"""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("📅 Today"),
        types.KeyboardButton("📅 Yesterday")
    )
    keyboard.add(
        types.KeyboardButton("📅 This Week"),
        types.KeyboardButton("📅 Last Week")
    )
    keyboard.add(
        types.KeyboardButton("📅 This Month"),
        types.KeyboardButton("📅 Custom Date")
    )
    keyboard.add(
        types.KeyboardButton("🔙 Back to Admin")
    )
    return keyboard

def create_account_info_keyboard(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id:
        back_text = get_text(user_id, "back_button")
    else:
        back_text = "🔙 Back/ត្រឡប់"
    keyboard.add(types.KeyboardButton(back_text))
    return keyboard
# === ALL NAVIGATION HANDLERS MUST COME BEFORE GENERAL HANDLERS ===
# This is critical for button functionality
# Main navigation handlers
@bot.message_handler(func=lambda message: message.text in ["🔙 Back", "🔙 ត្រឡប់ទៅម៉ឺនុយដើម", "🔙 ត្រឡប់", "🔙 Back/ត្រឡប់"])
def go_back(message):
    user_id = message.chat.id
    state = user_states.get(user_id)
    
    # Clear any transaction data
    if user_id in transactions:
        try:
            if "message_id" in transactions[user_id]:
                bot.delete_message(user_id, transactions[user_id]["message_id"])
        except Exception as e:
            logger.debug(f"Could not delete message: {e}")
        transactions.pop(user_id, None)
    
    # Handle different states
    if state in ["awaiting_amount", "add_funds"]:
        user_states[user_id] = "main_menu"
        bot.reply_to(message, "Back to main menu.", reply_markup=create_main_menu_keyboard(user_id))
    elif state == "stars_amount_selection":
        # Back from Stars amount selection to payment methods
        user_states[user_id] = "payment_methods"
        show_payment_methods(message)
    elif state in ["awaiting_telegram_url", "confirm_order", "waiting_for_payment", "awaiting_order_id_for_status"]:
        user_states[user_id] = "main_menu"
        bot.reply_to(message, "Operation canceled.", reply_markup=create_main_menu_keyboard(user_id))
    elif state == "services_menu":
        user_states[user_id] = "main_menu"
        bot.reply_to(message, "Back to main menu.", reply_markup=create_main_menu_keyboard(user_id))
    elif state in ["tiktok_services", "awaiting_tiktok_package", "tiktok_views", "tiktok_followers", "tiktok_saves", "tiktok_shares"]:
        user_states[user_id] = "services_menu"
        bot.reply_to(message, "🛒 Choose a service category:", reply_markup=create_services_menu_keyboard(user_id))
    elif state in ["facebook_services", "fb_page_followers", "fb_profile_followers", "fb_video_views", "fb_reactions"]:
        user_states[user_id] = "services_menu"
        bot.reply_to(message, "📘 Facebook Services", reply_markup=create_facebook_services_keyboard())
    elif state in ["telegram_services", "telegram_member_duration", "tg_7day", "tg_30day", "tg_lifetime",
                  "telegram_views", "tg_pos_reactions", "tg_neg_reactions"]:
        user_states[user_id] = "services_menu"
        bot.reply_to(message, "🛒 Choose a service category:", reply_markup=create_services_menu_keyboard(user_id))
    elif state in ["admin_menu", "awaiting_user_id_for_funds", "awaiting_fund_amount",
                  "awaiting_user_id_for_removal", "awaiting_removal_amount", "awaiting_broadcast", "awaiting_user_info",
                  "bonus_menu", "awaiting_bonus_min", "awaiting_bonus_max", "awaiting_bonus_percentage",
                  "awaiting_bonus_deletion"]:
        if is_admin(user_id):
            user_states[user_id] = "admin_menu"
            bot.reply_to(message, "🔐 Admin Panel", reply_markup=create_admin_menu_keyboard())
        else:
            user_states[user_id] = "main_menu"
            bot.reply_to(message, "Back to main menu.", reply_markup=create_main_menu_keyboard(user_id))
    else:
        user_states[user_id] = "main_menu"
        bot.reply_to(message, "Back to main menu.", reply_markup=create_main_menu_keyboard(user_id))

# Service category handlers
@bot.message_handler(func=lambda message: message.text in ["🛍️ Services", "🛍️ សេវាកម្ម"])
def show_services_menu(message):
    user_id = message.chat.id
    user_states[user_id] = "services_menu"
    services_text = get_text(user_id, "services_menu")
    bot.reply_to(message, services_text, reply_markup=create_services_menu_keyboard(user_id))
@bot.message_handler(func=lambda message: message.text in ["🎥 TikTok Services", "🎥 សេវាកម្ម TikTok"])
def show_tiktok_services(message):
    user_id = message.chat.id
    user_states[user_id] = "tiktok_services"
    services_text = get_text(user_id, "tiktok_services")
    bot.reply_to(message, services_text, reply_markup=create_tiktok_services_keyboard())
@bot.message_handler(func=lambda message: message.text in ["📱 Telegram Services", "📱 សេវាកម្ម Telegram"])
def show_telegram_services(message):
    user_id = message.chat.id
    user_states[user_id] = "telegram_services"
    services_text = get_text(user_id, "telegram_services")
    bot.reply_to(message, services_text, reply_markup=create_telegram_services_keyboard())
@bot.message_handler(func=lambda message: message.text in ["📘 Facebook Services", "📘 សេវាកម្ម Facebook"])
def show_facebook_services(message):
    user_id = message.chat.id
    user_states[user_id] = "facebook_services"
    services_text = get_text(user_id, "facebook_services")
    bot.reply_to(message, services_text, reply_markup=create_facebook_services_keyboard())
# TikTok sub-category handlers
@bot.message_handler(func=lambda message: message.text == "❤️ TikTok Likes & Views")
def show_tiktok_likes_views(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in SERVICES:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "❤️ TikTok Likes & Views", reply_markup=kb)
    user_states[user_id] = "awaiting_tiktok_package"
@bot.message_handler(func=lambda message: message.text == "👀 TikTok Views Only")
def show_tiktok_views_only(message):
    user_id = message.chat.id
    bot.reply_to(message, "👀 TikTok Views Only", reply_markup=create_tiktok_views_keyboard())
    user_states[user_id] = "tiktok_views"
@bot.message_handler(func=lambda message: message.text == "👥 TikTok Followers")
def show_tiktok_followers(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TIKTOK_FOLLOWERS_SERVICES:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "👥 TikTok Followers", reply_markup=kb)
    user_states[user_id] = "tiktok_followers"
@bot.message_handler(func=lambda message: message.text == "💾 TikTok Saves")
def show_tiktok_saves(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TIKTOK_SAVE_SERVICES:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "💾 TikTok Saves", reply_markup=kb)
    user_states[user_id] = "tiktok_saves"
@bot.message_handler(func=lambda message: message.text == "📤 TikTok Shares")
def show_tiktok_shares(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TIKTOK_SHARE_SERVICES:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "📤 TikTok Shares", reply_markup=kb)
    user_states[user_id] = "tiktok_shares"
# Facebook sub-category handlers
@bot.message_handler(func=lambda message: message.text == "👥 Facebook Page Followers")
def show_fb_page_followers(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in FB_PAGE_FOLLOWERS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "👥 Facebook Page Followers", reply_markup=kb)
    user_states[user_id] = "fb_page_followers"
@bot.message_handler(func=lambda message: message.text == "👤 Facebook Profile Followers")
def show_fb_profile_followers(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in FB_PROFILE_FOLLOWERS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "👤 Facebook Profile Followers", reply_markup=kb)
    user_states[user_id] = "fb_profile_followers"
@bot.message_handler(func=lambda message: message.text == "👀 Facebook Video Views")
def show_fb_video_views(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in FB_VIDEO_VIEWS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "👀 Facebook Video Views", reply_markup=kb)
    user_states[user_id] = "fb_video_views"
@bot.message_handler(func=lambda message: message.text == "❤️ Facebook Reactions")
def show_fb_reactions(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in FB_REACTIONS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "❤️ Facebook Reactions", reply_markup=kb)
    user_states[user_id] = "fb_reactions"
# Telegram sub-category handlers
@bot.message_handler(func=lambda message: message.text == "👥 Telegram Members")
def show_telegram_member_duration(message):
    user_id = message.chat.id
    bot.reply_to(message, "📅 Choose member duration:", reply_markup=create_telegram_member_duration_keyboard())
    user_states[user_id] = "telegram_member_duration"
@bot.message_handler(func=lambda message: message.text == "👀 Telegram Views")
def show_telegram_views(message):
    user_id = message.chat.id
    bot.reply_to(message, "👀 Telegram Views", reply_markup=create_telegram_view_services_keyboard())
    user_states[user_id] = "telegram_views"
@bot.message_handler(func=lambda message: message.text == "😊 Mix Positive Reactions")
def show_telegram_positive_reactions(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TELEGRAM_MIX_POSITIVE_REACTIONS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "😊 Mix Positive Reactions", reply_markup=kb)
    user_states[user_id] = "tg_pos_reactions"
@bot.message_handler(func=lambda message: message.text == "😡 Mix Negative Reactions")
def show_telegram_negative_reactions(message):
    user_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for name in TELEGRAM_MIX_NEGATIVE_REACTIONS:
        kb.add(types.KeyboardButton(name))
    kb.add(types.KeyboardButton("🔙 Back"))
    bot.reply_to(message, "😡 Mix Negative Reactions", reply_markup=kb)
    user_states[user_id] = "tg_neg_reactions"
@bot.message_handler(func=lambda message: message.text == "⏳ 7-Day Members")
def show_telegram_7day_members(message):
    user_id = message.chat.id
    kb = create_telegram_member_services_keyboard(TELEGRAM_MEMBER_7DAY)
    bot.reply_to(message, "⏳ 7-Day Members", reply_markup=kb)
    user_states[user_id] = "tg_7day"
@bot.message_handler(func=lambda message: message.text == "📆 30-Day Members")
def show_telegram_30day_members(message):
    user_id = message.chat.id
    kb = create_telegram_member_services_keyboard(TELEGRAM_MEMBER_30DAY)
    bot.reply_to(message, "📆 30-Day Members", reply_markup=kb)
    user_states[user_id] = "tg_30day"
@bot.message_handler(func=lambda message: message.text == "♾️ Lifetime Members")
def show_telegram_lifetime_members(message):
    user_id = message.chat.id
    kb = create_telegram_member_services_keyboard(TELEGRAM_MEMBER_LIFETIME)
    bot.reply_to(message, "♾️ Lifetime Members", reply_markup=kb)
    user_states[user_id] = "tg_lifetime"
# Order action handlers
@bot.message_handler(func=lambda message: message.text == "❌ Cancel Order")
def cancel_order(message):
    user_id = message.chat.id
    user_states[user_id] = "main_menu"
    if user_id in transactions:
        transactions.pop(user_id, None)
    bot.reply_to(message, "❌ Order canceled.", reply_markup=create_main_menu_keyboard())
@bot.message_handler(func=lambda message: message.text == "✅ Confirm Order")
def confirm_order(message):
    user_id = message.chat.id
    if not transactions.get(user_id, {}).get("package_name"):
        bot.reply_to(message, "❌ No service selected.", reply_markup=create_main_menu_keyboard())
        return
    bot.reply_to(message, "🔗 Send the post URL:", reply_markup=create_back_keyboard())
    user_states[user_id] = "awaiting_telegram_url"
# Bot Commands - Must come after navigation handlers but before general handlers
@bot.message_handler(commands=['start'])
def start(message):
    if not check_rate_limit(message.chat.id):
        bot.reply_to(message, "Too many requests. Please wait.")
        return
    user_id = message.chat.id
    db.add_user(user_id)
    
    # Always show language selection for /start command
    user_states[user_id] = "language_selection"
    bot.send_message(
        user_id,
        "🌍 Please select your language:\n"
        "សូមជ្រើសរើសភាសារបស់អ្នក:",
        reply_markup=create_language_selection_keyboard()
    )

def show_main_menu(message):
    """Show the main menu with proper language"""
    user_id = message.chat.id
    user_states[user_id] = "main_menu"
    user = get_cached_user(user_id)
    
    # Get welcome message in user's language
    if is_admin(user_id):
        welcome_text = get_text(user_id, "welcome", user['balance']) + "\n\n👋 Admin! Use /admin for admin panel."
    else:
        welcome_text = (
            get_text(user_id, "welcome", user['balance']) + "\n\n"
            "របៀបប្រើប្រាស់ : https://t.me/tinhliketiktok/2 \n"
            "Admin: @jakliketiktok"
        )
    
    # Send photo with caption, with a fallback to text
    try:
        if WELCOME_PHOTO_ID and WELCOME_PHOTO_ID != 'YOUR_WELCOME_PHOTO_FILE_ID_HERE':
            bot.send_photo(
                user_id,
                WELCOME_PHOTO_ID,
                caption=welcome_text,
                reply_markup=create_main_menu_keyboard(user_id),
                parse_mode='HTML'
            )
        else:
            bot.send_message(user_id, welcome_text, reply_markup=create_main_menu_keyboard(user_id), parse_mode='HTML')
    except Exception as e:
        logger.error(f"Failed to send welcome message to user {user_id}: {e}")
        bot.send_message(user_id, welcome_text, reply_markup=create_main_menu_keyboard(user_id), parse_mode='HTML')
    
    # Clear any old transactions
    if user_id in transactions:
        transactions.pop(user_id, None)

# Language selection handlers
@bot.message_handler(func=lambda message: message.text in ["🇺🇸 English", "🇰🇭 ខ្មែរ (Khmer)"])
def handle_language_selection(message):
    user_id = message.chat.id
    
    if message.text == "🇺🇸 English":
        language = "en"
    elif message.text == "🇰🇭 ខ្មែរ (Khmer)":
        language = "km"
    else:
        return
    
    # Set user language
    set_user_language(user_id, language)
    
    # Send confirmation and show main menu
    confirmation = get_text(user_id, "language_set")
    bot.send_message(user_id, confirmation)
    
    # Show main menu
    show_main_menu(message)

@bot.message_handler(commands=['language'])
def change_language(message):
    """Allow users to change their language preference"""
    user_id = message.chat.id
    # Clear any cached language preference to force selection
    if user_id in user_languages:
        user_languages.pop(user_id, None)
    
    user_states[user_id] = "language_selection"
    bot.send_message(
        user_id,
        "🌍 Please select your language:\n"
        "សូមជ្រើសរើសភាសារបស់អ្នក:",
        reply_markup=create_language_selection_keyboard()
    )

@bot.message_handler(commands=['clearcache'])
def clear_cache_debug(message):
    """Debug command to clear user cache"""
    user_id = message.chat.id
    
    # Clear all caches for this user
    if user_id in user_languages:
        user_languages.pop(user_id, None)
    if user_id in user_cache:
        user_cache.pop(user_id, None)
    
    bot.send_message(user_id, "🔄 Cache cleared! Now try /start to see language selection.")
    logger.info(f"Cache cleared for user {user_id}")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.reply_to(message, "❌ You are not authorized.")
        return
    user_states[user_id] = "admin_menu"
    bot.reply_to(message, "🔐 Admin Panel", reply_markup=create_admin_menu_keyboard())
# Admin Handlers
@bot.message_handler(func=lambda message: message.text == "📊 Bot Stats" and is_admin(message.from_user.id))
def send_bot_stats(message):
    user_id = message.from_user.id
    stats = db.get_bot_stats()
    text = (
        "📊 <b>Bot Statistics</b>\n"
        f"👥 Total Users: {stats['total_users']}\n"
        f"💰 Total Balance: ${stats['total_balance']:.2f}\n"
        f"💵 Users with Balance: {stats['users_with_balance']}\n"
        f"📦 Orders Today: {stats['orders_today']}"
    )
    bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
# Debug handler to catch any topup stats clicks
@bot.message_handler(func=lambda message: message.text == "💸 Topup Stats")
def debug_topup_stats_click(message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} clicked Topup Stats button")
    if not is_admin(user_id):
        logger.warning(f"User {user_id} is not admin - ADMIN_IDS: {ADMIN_IDS}")
        bot.reply_to(message, "❌ You are not authorized.", reply_markup=create_main_menu_keyboard())
        return
    # If admin, proceed with the actual handler
    send_topup_stats_handler(message)

# NEW: Handler for Topup Stats
def send_topup_stats_handler(message):
    try:
        user_id = message.from_user.id
        logger.info(f"Admin {user_id} requested topup stats")
        
        total_topup = db.get_daily_topup_stats()
        now_cambodia = datetime.utcnow() + timedelta(hours=7)
        today_str = now_cambodia.strftime('%Y-%m-%d')
        
        logger.info(f"Daily topup stats: ${total_topup:.2f} for {today_str}")

        text = (
            "📊 <b>Daily Top-up Statistics</b>\n"
            f"📅 Date: {today_str}\n"
            f"💸 Total Top-up: <b>${total_topup:.2f}</b>"
        )
        bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
        logger.info(f"Sent topup stats response to admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error in send_topup_stats: {e}")
        bot.reply_to(message, f"❌ Error retrieving topup statistics: {str(e)}", reply_markup=create_admin_menu_keyboard())
@bot.message_handler(func=lambda message: message.text == "💸 Add Funds" and is_admin(message.from_user.id))
def request_user_id_for_funds(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_user_id_for_funds"
    bot.reply_to(message, "🆔 Send the user ID:", reply_markup=create_back_keyboard())
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_user_id_for_funds")
def request_amount_to_add(message):
    user_id = message.from_user.id
    try:
        target_id = int(message.text.strip())
        user = get_cached_user(target_id)
        if not user or user['user_id'] != target_id:
            bot.reply_to(message, "❌ User not found.")
            user_states[user_id] = "admin_menu"
            return
        transactions[user_id] = {"target_user": target_id}
        user_states[user_id] = "awaiting_fund_amount"
        bot.reply_to(message, "💰 Enter amount to add:")
    except ValueError:
        bot.reply_to(message, "❌ Invalid ID.")
        user_states[user_id] = "admin_menu"
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_fund_amount")
def add_funds_to_user(message):
    admin_id = message.from_user.id
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            bot.reply_to(message, "❌ Amount must be positive.")
            return
        target_id = transactions[admin_id]["target_user"]
        new_balance = adjust_user_funds(target_id, amount, f"Admin added: {admin_id}")
        bot.send_message(target_id, f"✅ ${amount:.2f} has been added to your account by admin!\n💰 New balance: ${new_balance:.2f}")
        user_name = get_user_display_name(target_id)
        admin_name = get_user_display_name(admin_id)
        send_with_retry(
            PAYMENT_GROUP_ID,
            f"📥 <b>New Deposit (Admin Added)</b>\n"
            f"👤 {user_name}\n"
            f"🆔 {target_id}\n"
            f"💵 ${amount:.2f}\n"
            f"🛠️ Admin: {admin_name}",
            parse_mode='HTML'
        )
        bot.reply_to(message, f"✅ Added ${amount:.2f} to user {target_id}.", reply_markup=create_admin_menu_keyboard())
        user_states[admin_id] = "admin_menu"
        transactions.pop(admin_id, None)
    except Exception as e:
        logger.error(f"Error in add_funds_to_user: {e}")
        bot.reply_to(message, "❌ Invalid amount or error occurred.")
        user_states[admin_id] = "admin_menu"
        transactions.pop(admin_id, None)
@bot.message_handler(func=lambda message: message.text == "💸 Remove Funds" and is_admin(message.from_user.id))
def request_user_id_to_remove_funds(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_user_id_for_removal"
    bot.reply_to(message, "🆔 Send the user ID to remove funds from:", reply_markup=create_back_keyboard())
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_user_id_for_removal")
def request_amount_to_remove(message):
    user_id = message.from_user.id
    try:
        target_id = int(message.text.strip())
        user = get_cached_user(target_id)
        if not user or user['user_id'] != target_id:
            bot.reply_to(message, "❌ User not found.")
            user_states[user_id] = "admin_menu"
            return
        transactions[user_id] = {"target_user": target_id}
        user_states[user_id] = "awaiting_removal_amount"
        bot.reply_to(message, f"💰 Enter amount to remove from user {target_id}'s balance (Current balance: ${user['balance']:.2f}):")
    except ValueError:
        bot.reply_to(message, "❌ Invalid ID. Please enter a number.")
        user_states[user_id] = "admin_menu"
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_removal_amount")
def remove_funds_from_user(message):
    admin_id = message.from_user.id
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            bot.reply_to(message, "❌ Amount must be a positive number.")
            return
        target_id = transactions[admin_id]["target_user"]
        user = get_cached_user(target_id)
        if user['balance'] < amount:
            bot.reply_to(message, "❌ Insufficient user balance to remove.")
            user_states[admin_id] = "admin_menu"
            transactions.pop(admin_id, None)
            return
        new_balance = adjust_user_funds(target_id, -amount, f"Admin removed: {admin_id}")
        bot.send_message(target_id, f"⚠️ ${amount:.2f} has been removed from your account by an admin.\n💰 New balance: ${new_balance:.2f}")
        user_name = get_user_display_name(target_id)
        admin_name = get_user_display_name(admin_id)
        send_with_retry(
            PAYMENT_GROUP_ID,
            f"⛔️ <b>Funds Removed (Admin)</b>\n"
            f"👤 {user_name}\n"
            f"🆔 {target_id}\n"
            f"💵 ${amount:.2f}\n"
            f"🛠️ Admin: {admin_name}",
            parse_mode='HTML'
        )
        bot.reply_to(message, f"✅ Removed ${amount:.2f} from user {target_id}.", reply_markup=create_admin_menu_keyboard())
        user_states[admin_id] = "admin_menu"
        transactions.pop(admin_id, None)
    except Exception as e:
        logger.error(f"Error in remove_funds_from_user: {e}")
        bot.reply_to(message, "❌ Invalid amount or an error occurred.")
        user_states[admin_id] = "admin_menu"
        transactions.pop(admin_id, None)
@bot.message_handler(func=lambda message: message.text == "📤 Broadcast" and is_admin(message.from_user.id))
def request_broadcast_message(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_broadcast"
    bot.reply_to(message, "📢 Send message to all users:", reply_markup=create_back_keyboard())
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_broadcast", content_types=['text', 'photo', 'video'])
def send_broadcast(message):
    admin_id = message.from_user.id
    try:
        # Get user IDs with error handling
        user_ids = db.get_all_user_ids()
        if not user_ids:
            bot.reply_to(message, "❌ No users found in database", reply_markup=create_admin_menu_keyboard())
            user_states[admin_id] = "admin_menu"
            return
        
        sent = failed = 0
        total_users = len(user_ids)
        
        # Send initial status message
        status_msg = bot.reply_to(message, f"📤 Starting broadcast to {total_users} users...")
        
        for i, uid in enumerate(user_ids, 1):
            try:
                if message.content_type == 'text':
                    bot.send_message(uid, "📢 <b>Admin Broadcast</b>\n" + message.text, parse_mode='HTML')
                elif message.content_type == 'photo':
                    bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "", parse_mode='HTML')
                elif message.content_type == 'video':
                    bot.send_video(uid, message.video.file_id, caption=message.caption or "", parse_mode='HTML')
                sent += 1
                
                # Update status every 100 users
                if i % 100 == 0:
                    try:
                        bot.edit_message_text(
                            f"📤 Broadcasting... {i}/{total_users}\n✅ Sent: {sent} | ❌ Failed: {failed}",
                            admin_id, status_msg.message_id
                        )
                    except:
                        pass  # Ignore edit errors
                        
            except Exception as e:
                logger.error(f"Failed to send broadcast to {uid}: {e}")
                failed += 1
        
        # Final status
        final_msg = f"🎉 Broadcast Complete!\n📊 Total: {total_users}\n✅ Sent: {sent} | ❌ Failed: {failed}"
        try:
            bot.edit_message_text(final_msg, admin_id, status_msg.message_id)
        except:
            bot.send_message(admin_id, final_msg)
            
    except Exception as e:
        logger.error(f"Critical error in broadcast: {e}")
        bot.reply_to(message, f"❌ Broadcast failed: {str(e)}", reply_markup=create_admin_menu_keyboard())
    
    user_states[admin_id] = "admin_menu"
@bot.message_handler(func=lambda message: message.text == "👥 All Users" and is_admin(message.from_user.id))
def send_all_users(message):
    user_id = message.from_user.id
    user_ids = db.get_all_user_ids()
    text = f"👥 <b>All Users ({len(user_ids)})</b>:\n" + "\n".join([f"🆔 {uid}" for uid in user_ids[:50]])
    bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
@bot.message_handler(func=lambda message: message.text == "👥 User Mgmt" and is_admin(message.from_user.id))
def request_user_info(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_user_info"
    bot.reply_to(message, "🆔 Enter user ID:")
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_user_info")
def show_user_info(message):
    admin_id = message.from_user.id
    try:
        uid = int(message.text.strip())
        user = get_cached_user(uid)
        if not user or user['user_id'] != uid:
            bot.reply_to(message, "❌ Not found.")
        else:
            text = f"👤 User: {uid}\n💰 Balance: ${user['balance']:.2f}\n📅 Joined: {user['registration_date']}"
            bot.reply_to(message, text)
        user_states[admin_id] = "admin_menu"
    except (ValueError, KeyError):
        bot.reply_to(message, "❌ Invalid ID.")
    except Exception as e:
        logger.error(f"Error in show_user_info: {e}")
        bot.reply_to(message, "❌ An error occurred.")
    finally:
        user_states[admin_id] = "admin_menu"
# Bonus Management Handlers
@bot.message_handler(func=lambda message: message.text == "🎁 Bonus Mgmt" and is_admin(message.from_user.id))
def bonus_management_menu(message):
    user_id = message.from_user.id
    user_states[user_id] = "bonus_menu"

    # Get current bonus rules
    bonus_rules = db.get_active_bonus_rules()

    text = "🎁 <b>Bonus Management</b>\n\n"

    if bonus_rules:
        text += "📋 <b>Current Active Bonuses:</b>\n"
        for rule in bonus_rules:
            text += f"💰 ${rule['min_amount']:.2f} - ${rule['max_amount']:.2f} = {rule['bonus_percentage']}% bonus\n"
        text += "\n"
    else:
        text += "❌ No active bonus rules\n\n"

    text += "Choose an action:"

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("➕ Add Bonus"),
        types.KeyboardButton("🗑️ Remove Bonus")
    )
    keyboard.add(
        types.KeyboardButton("🚫 Cancel All Bonuses")
    )
    keyboard.add(types.KeyboardButton("🔙 Back"))

    bot.reply_to(message, text, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(commands=['bonus'])
def bonus_command(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    # Call the bonus management menu
    bonus_management_menu(message)

@bot.message_handler(commands=['cancelbonus'])
def cancel_bonus_command(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    # Get current bonus rules
    bonus_rules = db.get_active_bonus_rules()

    if not bonus_rules:
        bot.reply_to(message, "❌ No active bonus rules to cancel.", reply_markup=create_admin_menu_keyboard())
        return

    text = "🗑️ <b>Cancel Bonus Rules</b>\n\n"
    text += "📋 <b>Current Active Bonuses:</b>\n"

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for i, rule in enumerate(bonus_rules, 1):
        text += f"{i}. ${rule['min_amount']:.2f} - ${rule['max_amount']:.2f} = {rule['bonus_percentage']}% bonus\n"
        keyboard.add(types.KeyboardButton(f"Cancel Bonus {i}"))

    text += "\nSelect a bonus to cancel or cancel all:"

    keyboard.add(
        types.KeyboardButton("🚫 Cancel All Bonuses"),
        types.KeyboardButton("🔙 Back")
    )

    user_states[user_id] = "awaiting_bonus_deletion"
    transactions[user_id] = {"bonus_rules": bonus_rules}

    bot.reply_to(message, text, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "➕ Add Bonus" and is_admin(message.from_user.id))
def add_bonus_start(message):
    user_id = message.from_user.id
    user_states[user_id] = "awaiting_bonus_min"
    bot.reply_to(message, "💰 Enter minimum top-up amount (minimum 1):", reply_markup=create_back_keyboard())

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_bonus_min")
def process_bonus_min(message):
    user_id = message.from_user.id
    try:
        min_amount = float(message.text.strip())
        if min_amount < 1:
            bot.reply_to(message, "❌ Minimum amount must be at least $1. Please try again:")
            return

        transactions[user_id] = {"min_amount": min_amount}
        user_states[user_id] = "awaiting_bonus_max"
        bot.reply_to(message, f"💰 Enter maximum top-up amount (must be greater than ${min_amount:.2f}):")
    except ValueError:
        bot.reply_to(message, "❌ Invalid amount. Please enter a number:")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_bonus_max")
def process_bonus_max(message):
    user_id = message.from_user.id
    try:
        max_amount = float(message.text.strip())
        min_amount = transactions[user_id]["min_amount"]

        if max_amount <= min_amount:
            bot.reply_to(message, f"❌ Maximum amount must be greater than ${min_amount:.2f}. Please try again:")
            return

        transactions[user_id]["max_amount"] = max_amount
        user_states[user_id] = "awaiting_bonus_percentage"
        bot.reply_to(message, "📊 Enter bonus percentage (e.g., 10 for 10%):")
    except ValueError:
        bot.reply_to(message, "❌ Invalid amount. Please enter a number:")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_bonus_percentage")
def process_bonus_percentage(message):
    user_id = message.from_user.id
    try:
        percentage = float(message.text.strip())
        if percentage <= 0 or percentage > 100:
            bot.reply_to(message, "❌ Percentage must be between 0.1 and 100. Please try again:")
            return

        min_amount = transactions[user_id]["min_amount"]
        max_amount = transactions[user_id]["max_amount"]

        # Add the bonus rule to database
        rule_id = db.add_bonus_rule(min_amount, max_amount, percentage, user_id)

        text = f"✅ <b>Bonus Rule Created!</b>\n\n"
        text += f"💰 Range: ${min_amount:.2f} - ${max_amount:.2f}\n"
        text += f"🎁 Bonus: {percentage}% \n\n"
        text += f"Users who top up between ${min_amount:.2f} and ${max_amount:.2f} will receive {percentage}% bonus!"

        bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())

        user_states[user_id] = "admin_menu"
        transactions.pop(user_id, None)

        logger.info(f"Admin {user_id} created bonus rule: ${min_amount:.2f}-${max_amount:.2f} = {percentage}%")

    except ValueError:
        bot.reply_to(message, "❌ Invalid percentage. Please enter a number:")

@bot.message_handler(func=lambda message: message.text == "🗑️ Remove Bonus" and is_admin(message.from_user.id))
def remove_bonus_start(message):
    # Call the cancel bonus command functionality
    cancel_bonus_command(message)

@bot.message_handler(func=lambda message: message.text == "🚫 Cancel All Bonuses" and is_admin(message.from_user.id))
def cancel_all_bonuses(message):
    user_id = message.from_user.id

    # Get current bonus rules count
    bonus_rules = db.get_active_bonus_rules()

    if not bonus_rules:
        bot.reply_to(message, "❌ No active bonus rules to cancel.", reply_markup=create_admin_menu_keyboard())
        return

    # Deactivate all bonus rules
    db.deactivate_all_bonus_rules()

    text = f"✅ <b>All Bonus Rules Cancelled!</b>\n\n"
    text += f"🗑️ Cancelled {len(bonus_rules)} bonus rule(s)\n"
    text += "All existing bonus rules have been deactivated."

    bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
    user_states[user_id] = "admin_menu"

    logger.info(f"Admin {user_id} cancelled all bonus rules ({len(bonus_rules)} rules)")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_bonus_deletion")
def process_bonus_deletion(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text == "🚫 Cancel All Bonuses":
        cancel_all_bonuses(message)
        return

    if text.startswith("Cancel Bonus "):
        try:
            bonus_index = int(text.split("Cancel Bonus ")[1]) - 1
            bonus_rules = transactions[user_id]["bonus_rules"]

            if 0 <= bonus_index < len(bonus_rules):
                rule = bonus_rules[bonus_index]
                db.delete_bonus_rule(rule['id'])

                text = f"✅ <b>Bonus Rule Deleted!</b>\n\n"
                text += f"🗑️ Removed: ${rule['min_amount']:.2f} - ${rule['max_amount']:.2f} = {rule['bonus_percentage']}% bonus"

                bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
                user_states[user_id] = "admin_menu"
                transactions.pop(user_id, None)

                logger.info(f"Admin {user_id} deleted bonus rule: ${rule['min_amount']:.2f}-${rule['max_amount']:.2f} = {rule['bonus_percentage']}%")
            else:
                bot.reply_to(message, "❌ Invalid selection. Please try again.")
        except (ValueError, IndexError):
            bot.reply_to(message, "❌ Invalid selection. Please try again.")
    else:
        bot.reply_to(message, "❌ Invalid selection. Please choose from the options.")

@bot.message_handler(func=lambda message: message.text == "🔙 Back to User")
def back_to_user_mode(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        user_states[user_id] = "main_menu"
        bot.reply_to(message, "👋 Back to user mode.", reply_markup=create_main_menu_keyboard(user_id))

@bot.message_handler(func=lambda message: message.text == "🔙 Back to Admin" and is_admin(message.from_user.id))
def back_to_admin(message):
    user_id = message.from_user.id
    user_states[user_id] = "admin_menu"
    bot.reply_to(message, "🔐 Back to admin panel.", reply_markup=create_admin_menu_keyboard())
# User Handlers
@bot.message_handler(func=lambda message: message.text in ["👤 Account/អាខោន", "👤 Account Info", "👤 ព័ត៌មានគណនី"])
def show_account_info(message):
    user_id = message.chat.id
    user = get_cached_user(user_id)
    balance = user.get('balance', 0.0)
    username = get_user_display_name(user_id)
    # Show both username and user ID for clarity
    display_id = f"{username} (ID: {user_id})"
    text = get_text(user_id, "account_info", balance, display_id, user.get('total_orders', 0))
    bot.reply_to(message, text, reply_markup=create_account_info_keyboard(user_id))
def create_payment_method_keyboard(user_id=None):
    """Create keyboard for payment method selection"""
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    if user_id:
        if STARS_ENABLED:
            keyboard.add(types.KeyboardButton(get_text(user_id, "payment_method_stars")))
        keyboard.add(types.KeyboardButton(get_text(user_id, "payment_method_bakong")))
        keyboard.add(types.KeyboardButton(get_text(user_id, "back_button")))
    else:
        # Fallback to English
        if STARS_ENABLED:
            keyboard.add(types.KeyboardButton("⭐ Pay with Stars"))
        keyboard.add(types.KeyboardButton("💳 Pay with Bakong QR"))
        keyboard.add(types.KeyboardButton("🔙 Back"))
    return keyboard

def create_language_selection_keyboard():
    """Create keyboard for language selection"""
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("🇺🇸 English"),
        types.KeyboardButton("🇰🇭 ខ្មែរ (Khmer)")
    )
    return keyboard

def create_stars_amount_keyboard():
    """Create keyboard with predefined Star amounts"""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # Row 1: Small amounts
    keyboard.add(
        types.KeyboardButton("2⭐ = $0.019"),
        types.KeyboardButton("10⭐ = $0.11")
    )
    
    # Row 2: Medium amounts  
    keyboard.add(
        types.KeyboardButton("50⭐ = $0.55"),
        types.KeyboardButton("100⭐ = $1.10")
    )
    
    # Row 3: Large amounts
    keyboard.add(
        types.KeyboardButton("300⭐ = $3.6"),
        types.KeyboardButton("1000⭐ = $12")
    )
    
    # Row 4: Very large amounts
    keyboard.add(
        types.KeyboardButton("5000⭐ = $60"),
        types.KeyboardButton("10000⭐ = $130")
    )
    
    # Row 5: Back button
    keyboard.add(types.KeyboardButton("🔙 Back"))
    
    return keyboard

@bot.message_handler(func=lambda message: message.text in ["💰 Add Funds/ដាក់លុយ", "💰 Add Funds", "💰 បញ្ចូលលុយ"])
def show_payment_methods(message):
    user_id = message.chat.id
    user = get_cached_user(user_id)
    
    payment_options_text = get_text(user_id, "payment_methods_title", user['balance'])
    
    if STARS_ENABLED:
        payment_options_text += (
            f"⭐ <b>Telegram Stars</b>\n"
            f"• Instant payment processing\n"
            f"• No external apps needed\n"
            f"• Fair tiered pricing (better rates for small amounts)\n"
            f"• Example: $1 = ~65 Stars, $5 = ~225 Stars\n"
            f"• Secure in-app payment\n\n"
        )
    
    payment_options_text += (
        f"💳 <b>Bakong QR Code</b>\n"
        f"• Traditional bank transfer\n"
        f"• Requires Bakong app\n"
        f"• Manual verification\n"
        f"• 10-minute timeout\n"
    )
    
    bot.reply_to(
        message,
        payment_options_text,
        parse_mode='HTML',
        reply_markup=create_payment_method_keyboard(user_id)
    )

@bot.message_handler(func=lambda message: message.text in ["💳 Pay with Bakong QR", "💳 បង់ប្រាក់ដោយ Bakong QR"])
def request_fund_amount(message):
    user_id = message.chat.id
    user = get_cached_user(user_id)
    user_states[user_id] = "awaiting_amount"
    bot.reply_to(
        message,
        get_text(user_id, "bakong_amount_request", user['balance']),
        reply_markup=create_back_keyboard()
    )
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_amount")
def generate_qr(message):
    user_id = message.chat.id
    try:
        amount = message.text.strip()
        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            bot.reply_to(message, "❌ Invalid amount! Please enter a positive number.")
            return
        amount = f"{float(amount):.2f}"
        api_url = f"https://api.kunchhunlichhean.org/khqr/create?amount={amount}&bakongid=chhunlichhean_kun@wing&merchantname=JAKLIKEBOT"
        response = requests.get(api_url)
        if response.status_code in [200, 201]:
            try:
                data = response.json()
            except ValueError:
                bot.reply_to(message, "❌ Failed to parse QR response.")
                return
            qr_url = data.get('qr')
            md5 = data.get('md5')
            if not qr_url or not md5:
                bot.reply_to(message, "❌ Failed to generate QR code.")
                return
            sent_msg = bot.send_photo(
                user_id,
                qr_url,
                caption=f"📸 Scan to pay\n💵 Amount: ${amount}\n⏳ Valid for 30 minutes",
                reply_markup=create_back_keyboard()
            )
            transactions[user_id] = {
                "md5": md5,
                "message_id": sent_msg.message_id,
                "amount": float(amount),
                "timestamp": time.time()
            }
            user_states[user_id] = "waiting_for_payment"
            executor.submit(auto_check_transaction, user_id, md5, float(amount))
            executor.submit(delete_qr_after_timeout, user_id)
        else:
            bot.reply_to(message, f"❌ API Error: {response.status_code}")
    except Exception as e:
        logger.error(f"QR generation error: {e}")
        bot.reply_to(message, "❌ An error occurred.")
def auto_check_transaction(user_id, md5, amount):
    url = f"https://api.kunchhunlichhean.org/check_by_md5?md5={md5}&bakongid=chhunlichhean_kun@wing"
    logger.info(f"Starting transaction check for user {user_id}, MD5: {md5}, required amount: ${amount:.2f}")
    for i in range(180): # 180 × 10 seconds = 1800 seconds = 30 minutes
        if user_id not in transactions:
            logger.info(f"Transaction canceled or already processed for user {user_id}")
            return
        try:
            r = requests.get(url, timeout=10)
            logger.debug(f"Check #{i+1} - Status: {r.status_code}")
            if r.status_code != 200:
                logger.warning(f"Received HTTP {r.status_code}, retrying...")
                time.sleep(10)
                continue
            # Safely parse JSON
            try:
                data = r.json()
            except ValueError:
                logger.warning("Invalid JSON response")
                time.sleep(10)
                continue
            if not data:
                logger.warning("Empty or null JSON response")
                time.sleep(10)
                continue
            # Check responseCode
            response_code = data.get("responseCode")
            if response_code != 0:
                error_msg = data.get("description", "Unknown error")
                logger.warning(f"Payment not successful. responseCode={response_code}, error={error_msg}")
                time.sleep(10)
                continue
            # Extract amount and other fields
            data_part = data.get("data")
            if not data_part:
                logger.warning("Missing 'data' field in API response")
                time.sleep(10)
                continue
            
            # Log the full API response to see available fields
            logger.info(f"Bakong API response data: {data_part}")
            
            amount_str = data_part.get("amount")
            # Extract additional fields for bank-style notification using correct API field names
            account_id = data_part.get("fromAccountId", "unknown@abaa")
            transaction_hash = data_part.get("hash", "unknown")
            transaction_id = data_part.get("externalRef", "unknown")
            
            if not amount_str:
                logger.warning("Missing 'amount' in 'data'")
                time.sleep(10)
                continue
            try:
                api_amount = float(amount_str)
            except (TypeError, ValueError):
                logger.warning(f"Invalid amount value: {amount_str}")
                time.sleep(10)
                continue
            # ✅ Success: Sufficient payment
            if api_amount >= amount:
                # ⚠️ DUPLICATE TRANSACTION PREVENTION
                if db.check_bakong_transaction_exists(transaction_id):
                    logger.warning(f"🚫 DUPLICATE TRANSACTION DETECTED! Transaction ID: {transaction_id} already processed for user {user_id}")
                    # Send warning to admin group
                    duplicate_warning = (
                        f"🚫 <b>DUPLICATE BAKONG TRANSACTION BLOCKED!</b>\n\n"
                        f"👤 User: {get_user_display_name(user_id)} (ID: {user_id})\n"
                        f"💰 Amount: ${api_amount:.2f}\n"
                        f"🆔 Transaction ID: {transaction_id}\n"
                        f"🔗 Hash: {transaction_hash[:8]}\n\n"
                        f"⚠️ This transaction was already processed previously.\n"
                        f"💡 No funds were added to prevent double crediting."
                    )
                    send_with_retry(PAYMENT_GROUP_ID, duplicate_warning, parse_mode='HTML')
                    
                    # Clean up transaction tracking and exit
                    if user_id in transactions:
                        del transactions[user_id]
                    return
                
                # Record the transaction to prevent future duplicates
                if not db.add_bakong_transaction(transaction_id, transaction_hash, user_id, api_amount):
                    logger.error(f"Failed to record Bakong transaction {transaction_id} - possible race condition")
                    return
                
                # Use the new add_user_funds function with bonus calculation
                new_balance, bonus_amount = add_user_funds(user_id, amount, "User deposit", apply_bonus=True)

                # Generate deposit ID
                deposit_id = f"JAKLIKE_{random.randint(1000000, 9999999)}"
                # Get current time in Cambodia (UTC+7)
                cambodia_time = datetime.utcnow() + timedelta(hours=7)
                formatted_time = cambodia_time.strftime("%Y-%m-%d %H:%M:%S")

                # Prepare bank-style notification text
                user_name = get_user_display_name(user_id)
                # Extract first 8 characters of hash for Bakong Hash
                short_hash = transaction_hash[:8] if len(transaction_hash) >= 8 else transaction_hash
                
                deposit_notification = (
                    f"You received {amount:.2f} USD from {account_id} on {cambodia_time.strftime('%d %b, %Y %H:%M:%S')} "
                    f"by Transaction ID: {transaction_id}, Bakong Hash: {short_hash}. Remark: User: {user_name} (ID: {user_id})"
                )

                # Add bonus info if applicable
                if bonus_amount > 0:
                    deposit_notification += f"\n🎁 Bonus Applied: ${bonus_amount:.2f}"
                    deposit_notification += f"\n💰 Total Added: ${amount + bonus_amount:.2f}"
                send_with_retry(PAYMENT_GROUP_ID, deposit_notification)

                # Send user notification - First message
                user_message = (
                    f"Automated Deposit System ⚙️\n"
                    f"User ID: {user_id}\n"
                    f"Currency: USD 💵\n"
                    f"Balance Added: ${amount:.2f} ✅\n"
                )

                if bonus_amount > 0:
                    user_message += f"🎁 Bonus Added: ${bonus_amount:.2f} ✅\n"
                    user_message += f"💰 Total Added: ${amount + bonus_amount:.2f}\n"

                user_message += f"Payment: Bakong Pay [ Auto ]"

                bot.send_message(user_id, user_message)

                # Send user notification - Second message
                thank_you_message = f"Thank you for your payment of ${amount:.2f}."
                if bonus_amount > 0:
                    thank_you_message += f" You received a ${bonus_amount:.2f} bonus!"
                thank_you_message += " We appreciate your support!"

                bot.send_message(user_id, thank_you_message)
                # Clean up
                if "message_id" in transactions[user_id]:
                    try:
                        bot.delete_message(user_id, transactions[user_id]["message_id"])
                    except Exception as e:
                        logger.warning(f"Failed to delete QR message: {e}")
                transactions.pop(user_id, None)
                logger.info(f"✅ Payment successful for user {user_id}")
                return
            else:
                logger.warning(f"Underpayment: expected ${amount:.2f}, got ${api_amount:.2f}")
                bot.send_message(
                    user_id,
                    f"⚠️ Payment received (${api_amount:.2f}) is less than required (${amount:.2f}).\n"
                    "Please make a full payment."
                )
                transactions.pop(user_id, None)
                return
        except requests.exceptions.Timeout:
            logger.warning("Request to payment API timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
        time.sleep(10)
    # Timeout reached
    if user_id in transactions:
        try:
            bot.send_message(
                user_id,
                "⏳ QR code expired after 30 minutes. Please try again.",
                reply_markup=create_main_menu_keyboard()
            )
            if "message_id" in transactions[user_id]:
                bot.delete_message(user_id, transactions[user_id]["message_id"])
        except Exception as e:
            logger.error(f"Error sending timeout message: {e}")
        finally:
            transactions.pop(user_id, None)
def delete_qr_after_timeout(user_id):
    time.sleep(1800) # 1800 seconds = 30 minutes
    if user_id in transactions and "message_id" in transactions[user_id]:
        try:
            bot.delete_message(user_id, transactions[user_id]["message_id"])
            bot.send_message(user_id, "⏳ QR code expired after 30 minutes. Please use '💰 Add Funds' to generate a new one.", reply_markup=create_main_menu_keyboard())
        except Exception as e:
            logger.error(f"Error in QR timeout handler: {e}")
        finally:
            transactions.pop(user_id, None)

# ==================== TELEGRAM STARS PAYMENT HANDLERS ====================

def convert_usd_to_stars(usd_amount):
    """
    Convert USD amount to Telegram Stars using OFFICIAL Telegram pricing
    Based on actual Telegram Star prices: competitive but fair rates
    
    Official Telegram rates:
    2★ = $0.019 (105.26★/$)  |  10★ = $0.11 (90.91★/$)
    50★ = $0.55 (90.91★/$)   |  100★ = $1.10 (90.91★/$)  
    300★ = $3.60 (83.33★/$)  |  1000★ = $12 (83.33★/$)
    5000★ = $60 (83.33★/$)   |  10000★ = $130 (76.92★/$)
    """
    # Use competitive rates that are fair to users (slightly better than Telegram)
    if usd_amount <= 0.02:
        # Micro payments: match Telegram's best rate
        return max(1, int(usd_amount * 100))
    elif usd_amount <= 1.10:
        # Small amounts: competitive rate  
        return int(usd_amount * 85)  # Better than Telegram's 90.91
    elif usd_amount <= 12.0:
        # Medium amounts: good rate
        return int(usd_amount * 80)  # Better than Telegram's 83.33
    else:
        # Large amounts: bulk pricing
        return int(usd_amount * 75)  # Better than Telegram's 76.92

def convert_stars_to_usd(stars_amount):
    """
    Convert Telegram Stars to USD using the same competitive rates
    This is the reverse calculation for processing payments
    """
    if stars_amount <= 2:
        return round(stars_amount / 100, 2)
    elif stars_amount <= 94:  # 1.10 * 85
        return round(stars_amount / 85, 2)
    elif stars_amount <= 960:  # 12 * 80
        return round(stars_amount / 80, 2)
    else:
        return round(stars_amount / 75, 2)

def check_stars_support():
    """Check if the bot API supports Stars payments"""
    try:
        import telebot
        # Check if send_invoice supports XTR currency
        # Stars support was added in pyTelegramBotAPI 4.16.0+
        version = telebot.__version__
        # Handle version strings like "4.28.0"
        version_parts = version.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        
        logger.info(f"pyTelegramBotAPI version: {version} (major: {major}, minor: {minor})")
        
        # Version 4.28.0 definitely supports Stars
        if major > 4 or (major == 4 and minor >= 16):
            logger.info("Stars payments supported by library version")
            return True
        else:
            logger.warning(f"Stars not supported by version {version}")
            return False
    except Exception as e:
        logger.error(f"Error checking library version: {e}")
        return False

@bot.message_handler(func=lambda message: message.text in ["⭐ Pay with Stars", "⭐ បង់ប្រាក់ដោយ Stars"])
def request_stars_amount(message):
    """Handle Stars payment initiation - show amount selection"""
    if not STARS_ENABLED:
        bot.reply_to(message, "❌ Stars payments are currently disabled.", reply_markup=create_main_menu_keyboard())
        return
    
    # Check if library supports Stars
    supports_stars = check_stars_support()
    logger.info(f"Stars support check result: {supports_stars}")
    
    # Temporarily bypass version check since user has 4.28.0
    # if not supports_stars:
    #     bot.reply_to(
    #         message, 
    #         "❌ Stars payments require pyTelegramBotAPI 4.16.0+\n"
    #         "Please upgrade: pip install --upgrade pyTelegramBotAPI\n"
    #         "For now, please use Bakong QR payment instead.", 
    #         reply_markup=create_main_menu_keyboard()
    #     )
    #     return
        
    user_id = message.chat.id
    user = get_cached_user(user_id)
    user_states[user_id] = "stars_amount_selection"
    
    bot.reply_to(
        message,
        get_text(user_id, "stars_title", user['balance']),
        parse_mode='HTML',
        reply_markup=create_stars_amount_keyboard()
    )

# Handle Star amount selections
@bot.message_handler(func=lambda message: message.text.startswith("2⭐ = $") or 
                                          message.text.startswith("10⭐ = $") or
                                          message.text.startswith("50⭐ = $") or
                                          message.text.startswith("100⭐ = $") or
                                          message.text.startswith("300⭐ = $") or
                                          message.text.startswith("1000⭐ = $") or
                                          message.text.startswith("5000⭐ = $") or
                                          message.text.startswith("10000⭐ = $"))
def handle_stars_amount_selection(message):
    """Handle when user selects a predefined Star amount"""
    user_id = message.chat.id
    
    # Parse the selected amount
    text = message.text
    try:
        # Extract stars and USD from text like "2⭐ = $0.019"
        stars_part = text.split("⭐")[0]
        usd_part = text.split("$")[1]
        
        stars_amount = int(stars_part)
        usd_amount = float(usd_part)
        
        # Create the invoice directly
        create_stars_invoice_from_amount(message, usd_amount, stars_amount)
        
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing Stars amount selection: {e}")
        bot.reply_to(message, "❌ Invalid selection. Please try again.", 
                    reply_markup=create_stars_amount_keyboard())

def create_stars_invoice_from_amount(message, usd_amount, stars_amount):
    """Create Stars invoice from predefined amounts"""
    user_id = message.chat.id
    logger.info(f"Attempting to create Stars invoice for user {user_id} with usd_amount: {usd_amount} and stars_amount: {stars_amount}")
    
    try:
        # Create unique invoice payload
        invoice_payload = f"stars_deposit_{user_id}_{int(time.time())}"
        logger.info(f"Generated invoice_payload: {invoice_payload}")
        
        # Log the transaction to database
        db.add_stars_transaction(
            user_id=user_id,
            transaction_type="deposit",
            usd_amount=usd_amount,
            stars_amount=stars_amount,
            invoice_payload=invoice_payload,
            service_name="Account Top-up"
        )
        logger.info(f"Logged stars transaction to database")
        
        # Also store in memory for compatibility (backup method)
        stars_transactions[user_id] = {
            "transaction_type": "deposit",
            "usd_amount": usd_amount,
            "stars_amount": stars_amount,
            "payload": invoice_payload,  # Use 'payload' for consistency
            "timestamp": time.time(),   # Add timestamp
            "service_name": "Account Top-up"
        }
        logger.info(f"Stored stars transaction in memory")
        
        # Create the invoice
        logger.info(f"Creating Stars invoice: User {user_id}, ${usd_amount} USD, {stars_amount} Stars")
        
        bot.send_invoice(
            chat_id=user_id,
            title=f"⭐ {stars_amount} Telegram Stars",
            description=f"Add ${usd_amount} USD to your account balance\nCompetitive rates - better than official Telegram pricing!",
            invoice_payload=invoice_payload,
            provider_token="",  # Empty for Stars
            currency="XTR",  # Telegram Stars currency
            prices=[types.LabeledPrice(label=f"{stars_amount} Stars", amount=stars_amount)],
            start_parameter="stars_payment"
        )
        
        logger.info(f"✅ Stars invoice sent successfully for user {user_id}")
        
        # Send confirmation message
        bot.send_message(
            user_id,
            f"✨ <b>Payment Invoice Created!</b>\n\n" 
            f"💰 Amount: {stars_amount}⭐ = ${usd_amount} USD\n"
            f"🎯 Will be added to your balance\n\n"
            f"👆 <b>Tap the invoice above to pay!</b>",
            parse_mode='HTML',
            reply_markup=create_main_menu_keyboard(user_id)
        )
        
    except Exception as e:
        logger.error(f"Error creating Stars invoice: {e}")
        bot.reply_to(
            message, 
            "❌ Payment error occurred. Please try Bakong QR payment or contact support.",
            reply_markup=create_main_menu_keyboard()
        )



@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_stars_amount")
def create_stars_invoice(message):
    """Create Telegram Stars invoice"""
    user_id = message.chat.id
    try:
        amount_str = message.text.strip()
        if not amount_str.replace('.', '', 1).isdigit() or float(amount_str) <= 0:
            bot.reply_to(message, "❌ Invalid amount! Please enter a positive number.")
            return
            
        usd_amount = float(amount_str)
        stars_amount = convert_usd_to_stars(usd_amount)
        
        # Minimum amount check
        if stars_amount < 1:
            bot.reply_to(message, "❌ Minimum amount is $0.01 (1 Star).")
            return
            
        # Create invoice payload
        invoice_payload = f"balance_topup_{user_id}_{int(time.time())}"
        
        # Store transaction data
        stars_transactions[user_id] = {
            "type": "balance_topup",
            "usd_amount": usd_amount,
            "stars_amount": stars_amount,
            "payload": invoice_payload,
            "timestamp": time.time()
        }
        
        # Log to database
        db.add_stars_transaction(
            user_id, "balance_topup", usd_amount, stars_amount, invoice_payload
        )
        
        # Create and send invoice
        try:
            # Validate parameters
            logger.info(f"Creating Stars invoice - User: {user_id}, USD: ${usd_amount}, Stars: {stars_amount}")
            
            bot.send_invoice(
                chat_id=user_id,
                title="💰 Add Funds",
                description=f"Add ${usd_amount:.2f} to your account balance",
                invoice_payload=invoice_payload,  # Correct parameter name for pyTelegramBotAPI
                provider_token="",  # Empty for Stars payments
                currency="XTR",  # Telegram Stars currency
                prices=[types.LabeledPrice(label="Balance Top-up", amount=stars_amount)],
                start_parameter="stars_payment",
                need_shipping_address=False,
                need_phone_number=False,
                need_email=False,
                is_flexible=False
            )
            
            user_states[user_id] = "main_menu"
            bot.send_message(
                user_id, 
                f"⭐ Invoice created for {stars_amount} Stars (${usd_amount:.2f})\n"
                "Tap the Pay button above to complete your payment!",
                reply_markup=create_main_menu_keyboard()
            )
            
        except Exception as e:
            logger.error(f"Failed to create Stars invoice for user {user_id}, amount ${usd_amount}: {e}")
            logger.error(f"Invoice payload: {invoice_payload}")
            logger.error(f"Stars amount: {stars_amount}")
            
            # Show detailed error for debugging
            error_str = str(e).lower()
            if "currency" in error_str or "xtr" in error_str or "method" in error_str:
                bot.reply_to(
                    message, 
                    "❌ Stars payments are not available yet.\n"
                    "Please use 💳 Bakong QR payment instead.\n\n"
                    "📱 Tap '💰 Add Funds' → '💳 Pay with Bakong QR'",
                    reply_markup=create_main_menu_keyboard()
                )
            else:
                # Show detailed error for debugging
                bot.reply_to(message, f"❌ Payment error: {str(e)[:200]}\nPlease try Bakong QR payment or contact support.")
            user_states[user_id] = "main_menu"
            
    except Exception as e:
        logger.error(f"Stars invoice creation error: {e}")
        bot.reply_to(message, "❌ An error occurred.")
        user_states[user_id] = "main_menu"

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(query):
    """
    Handle pre-checkout queries for Stars payments.
    This function must be very fast to avoid timeouts from Telegram.
    """
    logger.info(f"Received pre-checkout query: {query}")
    try:
        logger.info(f"Received pre-checkout query from user {query.from_user.id}, payload: {query.invoice_payload}")
        
        # Check if the transaction exists in the database
        transaction = db.get_stars_transaction(query.from_user.id, query.invoice_payload)
        
        if transaction:
            # Immediately approve the query.
            bot.answer_pre_checkout_query(query.id, ok=True)
            logger.info(f"Pre-checkout query approved for user {query.from_user.id}")
        else:
            # If transaction not found, reject the query
            logger.warning(f"Pre-checkout query rejected for user {query.from_user.id}: Transaction not found for payload {query.invoice_payload}")
            bot.answer_pre_checkout_query(query.id, ok=False, error_message="Transaction expired or invalid. Please try again.")
            
    except Exception as e:
        logger.exception(f"Critical error in pre-checkout query for user {query.from_user.id}: {e}")
        # Even if there's an error, we must try to respond to Telegram.
        try:
            bot.answer_pre_checkout_query(query.id, ok=False, error_message="An internal error occurred. Please contact support.")
        except Exception as inner_e:
            logger.error(f"Failed to even send a negative pre-checkout answer: {inner_e}")

@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    """Handle successful Stars payments"""
    logger.info(f"Received successful payment message: {message}")
    try:
        payment = message.successful_payment
        user_id = message.chat.id
        payload = payment.invoice_payload
        stars_paid = payment.total_amount
        telegram_payment_charge_id = payment.telegram_payment_charge_id
        
        logger.info(f"Successful payment from user {user_id}: {stars_paid} Stars, charge ID: {telegram_payment_charge_id}")
        
        # Get transaction details from the database
        transaction = db.get_stars_transaction(user_id, payload)
        logger.info(f"Retrieved transaction from database: {transaction}")
        
        if not transaction:
            logger.error(f"No transaction record for successful payment from user {user_id}, payload: {payload}")
            bot.send_message(user_id, "❌ Payment received but transaction record not found. Please contact support.")
            return
            
        # Check if the transaction is already completed
        if transaction['status'] == 'completed':
            logger.warning(f"Received duplicate successful payment notification for user {user_id}, payload: {payload}")
            return

        expected_stars = transaction["stars_amount"]
        usd_amount = transaction["usd_amount"]
        
        # Verify payment amount
        if stars_paid != expected_stars:
            logger.warning(f"Payment amount mismatch: expected {expected_stars}, got {stars_paid}")
            bot.send_message(user_id, f"⚠️ Payment amount mismatch. Expected {expected_stars} Stars, received {stars_paid} Stars. Please contact support.")
            # Optionally, you could refund here if the amount is wrong
            return
            
        # Process the payment based on transaction type
        if transaction["transaction_type"] == "deposit":
            # Add funds to user balance
            new_balance, bonus_amount = add_user_funds(
                user_id, usd_amount, f"Stars Payment: {stars_paid} Stars", apply_bonus=True
            )
            logger.info(f"Added funds to user {user_id}. New balance: {new_balance}, bonus amount: {bonus_amount}")
            
            # Complete the database transaction
            db.complete_stars_transaction(user_id, payload, telegram_payment_charge_id)
            logger.info(f"Completed stars transaction in database for user {user_id}, payload: {payload}")
                
            # Send notification to payment group (bank-style format)
            user_name = get_user_display_name(user_id)
            cambodia_time = datetime.utcnow() + timedelta(hours=7)
            short_charge_id = telegram_payment_charge_id[:8]
            
            payment_notification = (
                f"⭐ You received {usd_amount:.2f} USD from Telegram@Stars on {cambodia_time.strftime('%d %b, %Y %H:%M:%S')}" 
                f"by Transaction ID: {telegram_payment_charge_id}, Stars Hash: {short_charge_id}. Remark: User: {user_name} (ID: {user_id})"
            )
            if bonus_amount > 0:
                payment_notification += f"\n🎁 Bonus Applied: ${bonus_amount:.2f}"
                payment_notification += f"\n💰 Total Added: ${usd_amount + bonus_amount:.2f}"
            
            send_with_retry(PAYMENT_GROUP_ID, payment_notification, parse_mode='HTML')
            logger.info(f"Sent payment notification to group for user {user_id}")
            
            # Send confirmation to user
            total_added = usd_amount + bonus_amount
            final_balance = new_balance # add_user_funds already returns the updated balance

            user_message = get_text(
                user_id, 
                "stars_payment_success",
                stars_paid,
                usd_amount,
                usd_amount, # Balance added
                get_text(user_id, "bonus_applied", bonus_amount, total_added) if bonus_amount > 0 else "",
                final_balance
            )
            
            bot.send_message(user_id, user_message, parse_mode='HTML')
            logger.info(f"Sent successful payment confirmation to user {user_id}")
            
        elif transaction["transaction_type"] == "service":
            # Handle direct service payments (for future use)
            service_name = transaction.get("service_name", "Unknown Service")
            bot.send_message(user_id, f"⭐ Payment successful for {service_name}!")
            # You would typically trigger the service delivery here
            db.complete_stars_transaction(user_id, payload, telegram_payment_charge_id)

        # Clean up in-memory transaction record if it exists (for safety)
        stars_transactions.pop(user_id, None)
        logger.info(f"✅ Stars payment processed successfully for user {user_id}")
        
    except Exception as e:
        logger.exception(f"Error processing successful payment for user {message.chat.id}: {e}")
        bot.send_message(message.chat.id, "❌ A critical error occurred while processing your payment. Please contact support with your payment details.")




def create_stars_service_invoice(user_id, service_name, service_price, service_description):
    """Create a direct payment invoice for a service using Stars"""
    if not STARS_ENABLED:
        return False
        
    try:
        stars_amount = convert_usd_to_stars(service_price)
        invoice_payload = f"service_{user_id}_{int(time.time())}"
        
        # Store transaction data
        stars_transactions[user_id] = {
            "type": "direct_service",
            "service_name": service_name,
            "usd_amount": service_price,
            "stars_amount": stars_amount,
            "payload": invoice_payload,
            "timestamp": time.time()
        }
        
        # Log to database
        db.add_stars_transaction(
            user_id, "direct_service", service_price, stars_amount, 
            invoice_payload, service_name
        )
        
        bot.send_invoice(
            chat_id=user_id,
            title=f"🛒 {service_name}",
            description=f"{service_description}\nExchange rate: 1 USD = 2 Stars",
            invoice_payload=invoice_payload,  # Correct parameter name for pyTelegramBotAPI
            provider_token="",  # Empty for Stars payments
            currency="XTR",  # Telegram Stars currency
            prices=[types.LabeledPrice(label=service_name, amount=stars_amount)],
            need_shipping_address=False,
            need_phone_number=False,
            need_email=False,
            is_flexible=False
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create service Stars invoice: {e}")
        return False

@bot.message_handler(commands=['paysupport'])
def handle_payment_support(message):
    """Handle payment support requests for Stars"""
    support_message = (
        "💰 <b>Payment Support</b>\n\n"
        "🌟 <b>Telegram Stars Payments:</b>\n"
        "• Instant processing\n"
        "• No external payment providers\n"
        "• Secure in-app payments\n"
        "• Exchange rate: 1 USD = 2 Stars\n\n"
        "🔄 <b>Refunds:</b>\n"
        "Stars payments can be refunded if there are technical issues.\n"
        "Contact support with your payment charge ID.\n\n"
        "📞 <b>Support Contact:</b>\n"
        "For any payment issues, contact our support team."
    )
    bot.send_message(message.chat.id, support_message, parse_mode='HTML')

def refund_stars_payment(telegram_payment_charge_id, reason="Technical issue"):
    """Refund a Stars payment (admin function)"""
    try:
        result = bot.refund_star_payment(
            telegram_payment_charge_id=telegram_payment_charge_id
        )
        logger.info(f"Refund initiated for charge {telegram_payment_charge_id}: {result}")
        return True
    except Exception as e:
        logger.error(f"Failed to refund Stars payment {telegram_payment_charge_id}: {e}")
        return False

# Debug handler to catch any stars stats clicks
@bot.message_handler(func=lambda message: message.text == "⭐ Stars Stats")
def debug_stars_stats_click(message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} clicked Stars Stats button")
    if not is_admin(user_id):
        logger.warning(f"User {user_id} is not admin - ADMIN_IDS: {ADMIN_IDS}")
        bot.reply_to(message, "❌ You are not authorized.", reply_markup=create_main_menu_keyboard())
        return
    # If admin, proceed with the actual handler
    send_stars_stats_handler(message)

def send_stars_stats_handler(message):
    """Send Stars payment statistics to admin"""
    try:
        user_id = message.from_user.id
        logger.info(f"Admin {user_id} requested stars stats")
        
        # Get 30-day stats
        stats_30d = db.get_stars_stats(30)
        # Get 7-day stats
        stats_7d = db.get_stars_stats(7)
        # Get today's stats
        stats_today = db.get_stars_stats(1)
        
        logger.info(f"Stars stats retrieved - Today: {stats_today}, 7d: {stats_7d}, 30d: {stats_30d}")
        
        stats_text = (
            "⭐ <b>Telegram Stars Payment Statistics</b>\n\n"
            
            f"📅 <b>Today:</b>\n"
            f"💰 Transactions: {stats_today['total_transactions']}\n"
            f"💵 Total USD: ${stats_today['total_usd']:.2f}\n"
            f"⭐ Total Stars: {stats_today['total_stars']}\n"
            f"📊 Avg per transaction: ${stats_today['avg_usd']:.2f}\n\n"
            
            f"📅 <b>Last 7 Days:</b>\n"
            f"💰 Transactions: {stats_7d['total_transactions']}\n"
            f"💵 Total USD: ${stats_7d['total_usd']:.2f}\n"
            f"⭐ Total Stars: {stats_7d['total_stars']}\n"
            f"📊 Avg per transaction: ${stats_7d['avg_usd']:.2f}\n\n"
            
            f"📅 <b>Last 30 Days:</b>\n"
            f"💰 Transactions: {stats_30d['total_transactions']}\n"
            f"💵 Total USD: ${stats_30d['total_usd']:.2f}\n"
            f"⭐ Total Stars: {stats_30d['total_stars']}\n"
            f"📊 Avg per transaction: ${stats_30d['avg_usd']:.2f}\n\n"
            
            f"💱 <b>Exchange Rate:</b> 1 USD = 2 Stars\n"
            f"🌟 <b>Status:</b> {'Enabled' if STARS_ENABLED else 'Disabled'}"
        )
        
        bot.reply_to(message, stats_text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
        logger.info(f"Sent stars stats response to admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error getting Stars stats: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        bot.reply_to(message, f"❌ Error retrieving Stars statistics: {str(e)}", reply_markup=create_admin_menu_keyboard())

# ==================== BULK RETRY HANDLERS ====================

@bot.message_handler(func=lambda message: message.text == "🎥 TikTok Bulk Retry" and is_admin(message.from_user.id))
def show_bulk_retry_menu(message):
    """Show bulk retry time period selection menu"""
    user_id = message.from_user.id
    user_states[user_id] = "bulk_retry_menu"
    
    text = (
        "🎥 <b>TikTok Bulk Retry Orders</b>\n\n"
        "📅 Select time period for TikTok orders to retry:\n"
        "💡 This will resend TikTok orders to your SMM provider\n"
        "🎯 Useful when TikTok detects and removes engagement\n\n"
        "✅ <b>Supports:</b> tiktok.com & vt.tiktok.com URLs\n"
        "🛡️ <b>Safe:</b> Only processes TikTok orders\n\n"
        "🔄 <b>Retry Logic:</b>\n"
        "👀 Views: Random 1K-10K (regardless of original)\n"
        "❤️ Likes: Exact original amount\n\n"
        "✅ <b>Includes ONLY:</b>\n"
        "• TikTok Likes & Views (combo packages)\n"
        "• TikTok Views Only\n\n"
        "❌ <b>Excludes:</b> Followers, Saves, Shares\n\n"
        "⚠️ <b>Warning:</b> This will create new orders for existing URLs"
    )
    
    bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_bulk_retry_keyboard())

@bot.message_handler(func=lambda message: message.text.startswith("📅") and user_states.get(message.from_user.id) == "bulk_retry_menu")
def handle_bulk_retry_period(message):
    """Handle time period selection for bulk retry"""
    user_id = message.from_user.id
    period_text = message.text
    
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    
    if period_text == "📅 Today":
        start_date = end_date = today
        period_name = "Today"
    elif period_text == "📅 Yesterday":
        start_date = end_date = today - timedelta(days=1)
        period_name = "Yesterday"
    elif period_text == "📅 This Week":
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)
        end_date = today
        period_name = "This Week"
    elif period_text == "📅 Last Week":
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday + 7)
        end_date = today - timedelta(days=days_since_monday + 1)
        period_name = "Last Week"
    elif period_text == "📅 This Month":
        start_date = today.replace(day=1)
        end_date = today
        period_name = "This Month"
    elif period_text == "📅 Custom Date":
        user_states[user_id] = "awaiting_custom_date"
        bot.reply_to(message, "📅 Enter date in format YYYY-MM-DD (e.g., 2024-01-15):", reply_markup=create_admin_menu_keyboard())
        return
    else:
        bot.reply_to(message, "❌ Invalid selection", reply_markup=create_bulk_retry_keyboard())
        return
    
    # Get orders for the selected period
    all_orders = db.get_orders_by_date_range(str(start_date), str(end_date))
    
    # Filter for TikTok Likes & Views orders only (by URL and package type)
    orders = []
    for order in all_orders:
        url = order.get('url', '').lower()
        package = order.get('package', '')
        
        # Check if it's a TikTok URL
        if url and ('tiktok.com' in url or 'vt.tiktok.com' in url):
            # Only include TikTok Likes & Views combo OR TikTok Views Only
            if package in SERVICES or package in TIKTOK_VIEW_SERVICES:
                orders.append(order)
    
    if not orders:
        bot.reply_to(message, f"📅 No TikTok orders found for {period_name}", reply_markup=create_admin_menu_keyboard())
        user_states[user_id] = "admin_menu"
        return
    
    # Store retry data for confirmation
    user_states[user_id] = "confirming_bulk_retry"
    retry_data[user_id] = {
        'orders': orders,
        'period_name': period_name,
        'start_date': str(start_date),
        'end_date': str(end_date)
    }
    
    # Show confirmation
    confirmation_text = (
        f"🎥 <b>TikTok Bulk Retry Confirmation</b>\n\n"
        f"📅 <b>Period:</b> {period_name}\n"
        f"📊 <b>TikTok Orders Found:</b> {len(orders)}\n"
        f"🗓️ <b>Date Range:</b> {start_date} to {end_date}\n\n"
        f"🎯 <b>Filtered for TikTok only</b>\n"
        f"✅ Supports: tiktok.com & vt.tiktok.com\n\n"
        f"⚠️ <b>This will:</b>\n"
        f"• Resend {len(orders)} TikTok orders to SMM provider\n"
        f"• Create new order IDs for tracking\n"
        f"• Use original URLs and packages\n\n"
        f"✅ Type 'CONFIRM' to proceed\n"
        f"❌ Type 'CANCEL' to abort"
    )
    
    bot.reply_to(message, confirmation_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "awaiting_custom_date")
def handle_custom_date(message):
    """Handle custom date input for bulk retry"""
    user_id = message.from_user.id
    date_text = message.text.strip()
    
    try:
        from datetime import datetime
        custom_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        
        # Get orders for the custom date
        all_orders = db.get_orders_by_date_range(str(custom_date), str(custom_date))
        
        # Filter for TikTok Likes & Views orders only (by URL and package type)
        orders = []
        for order in all_orders:
            url = order.get('url', '').lower()
            package = order.get('package', '')
            
            # Check if it's a TikTok URL
            if url and ('tiktok.com' in url or 'vt.tiktok.com' in url):
                # Only include TikTok Likes & Views combo OR TikTok Views Only
                if package in SERVICES or package in TIKTOK_VIEW_SERVICES:
                    orders.append(order)
        
        if not orders:
            bot.reply_to(message, f"📅 No TikTok orders found for {custom_date}", reply_markup=create_admin_menu_keyboard())
            user_states[user_id] = "admin_menu"
            return
        
        # Store retry data for confirmation
        user_states[user_id] = "confirming_bulk_retry"
        retry_data[user_id] = {
            'orders': orders,
            'period_name': f"Custom Date ({custom_date})",
            'start_date': str(custom_date),
            'end_date': str(custom_date)
        }
        
        # Show confirmation
        confirmation_text = (
            f"🎥 <b>TikTok Bulk Retry Confirmation</b>\n\n"
            f"📅 <b>Date:</b> {custom_date}\n"
            f"📊 <b>TikTok Orders Found:</b> {len(orders)}\n\n"
            f"🎯 <b>Filtered for TikTok only</b>\n"
            f"✅ Supports: tiktok.com & vt.tiktok.com\n\n"
            f"⚠️ <b>This will:</b>\n"
            f"• Resend {len(orders)} TikTok orders to SMM provider\n"
            f"• Create new order IDs for tracking\n"
            f"• Use original URLs and packages\n\n"
            f"✅ Type 'CONFIRM' to proceed\n"
            f"❌ Type 'CANCEL' to abort"
        )
        
        bot.reply_to(message, confirmation_text, parse_mode='HTML')
        
    except ValueError:
        bot.reply_to(message, "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2024-01-15):")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "confirming_bulk_retry")
def handle_bulk_retry_confirmation(message):
    """Handle bulk retry confirmation"""
    user_id = message.from_user.id
    response = message.text.strip().upper()
    
    if response == "CONFIRM":
        # Get stored retry data
        retry_info = retry_data.get(user_id, {})
        orders = retry_info.get('orders', [])
        period_name = retry_info.get('period_name', 'Unknown')
        
        if not orders:
            bot.reply_to(message, "❌ No retry data found", reply_markup=create_admin_menu_keyboard())
            user_states[user_id] = "admin_menu"
            return
        
        # Start bulk retry process
        user_states[user_id] = "admin_menu"
        
        progress_text = (
            f"🎥 <b>Starting TikTok Bulk Retry...</b>\n\n"
            f"📅 Period: {period_name}\n"
            f"📊 TikTok Orders: {len(orders)}\n"
            f"⏳ Processing in background...\n\n"
            f"📱 You'll receive updates as orders are processed"
        )
        
        bot.reply_to(message, progress_text, parse_mode='HTML', reply_markup=create_admin_menu_keyboard())
        
        # Process bulk retry in background
        executor.submit(process_bulk_retry, user_id, orders, period_name)
        
        # Clear retry data
        if user_id in retry_data:
            del retry_data[user_id]
            
    elif response == "CANCEL":
        user_states[user_id] = "admin_menu"
        bot.reply_to(message, "❌ Bulk retry canceled", reply_markup=create_admin_menu_keyboard())
        
        # Clear retry data
        if user_id in retry_data:
            del retry_data[user_id]
    else:
        bot.reply_to(message, "❌ Please type 'CONFIRM' or 'CANCEL'")

def process_bulk_retry(admin_user_id, orders, period_name):
    """Process bulk retry orders in background"""
    try:
        successful_retries = 0
        failed_retries = 0
        total_orders = len(orders)
        
        # Send initial status
        bot.send_message(admin_user_id, f"🎥 Processing {total_orders} TikTok orders for {period_name}...")
        
        for i, order in enumerate(orders, 1):
            try:
                package = order['package']
                url = order['url']
                user_id = order['user_id']
                
                if not url or not package:
                    failed_retries += 1
                    continue
                
                # Find the service configuration (only for TikTok Likes & Views services)
                service = None
                for service_dict in [SERVICES, TIKTOK_VIEW_SERVICES]:
                    if package in service_dict:
                        service = service_dict[package]
                        break
                
                if not service:
                    failed_retries += 1
                    continue
                
                # Retry the order based on package type
                retry_success = retry_single_order(package, url, service, user_id)
                
                if retry_success:
                    successful_retries += 1
                else:
                    failed_retries += 1
                
                # Send progress update every 10 orders
                if i % 10 == 0 or i == total_orders:
                    progress_text = (
                        f"🎥 <b>TikTok Bulk Retry Progress</b>\n\n"
                        f"📊 Processed: {i}/{total_orders}\n"
                        f"✅ Successful: {successful_retries}\n"
                        f"❌ Failed: {failed_retries}\n"
                        f"📈 Progress: {(i/total_orders)*100:.1f}%"
                    )
                    bot.send_message(admin_user_id, progress_text, parse_mode='HTML')
                
                # Small delay to avoid overwhelming the API
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error retrying order {order.get('id', 'unknown')}: {e}")
                failed_retries += 1
        
        # Send final summary
        summary_text = (
            f"🎉 <b>TikTok Bulk Retry Complete!</b>\n\n"
            f"📅 <b>Period:</b> {period_name}\n"
            f"📊 <b>TikTok Orders:</b> {total_orders}\n"
            f"✅ <b>Successful:</b> {successful_retries}\n"
            f"❌ <b>Failed:</b> {failed_retries}\n"
            f"📈 <b>Success Rate:</b> {(successful_retries/total_orders)*100:.1f}%\n\n"
            f"🔍 Check individual order statuses for details"
        )
        
        bot.send_message(admin_user_id, summary_text, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in bulk retry process: {e}")
        bot.send_message(admin_user_id, f"❌ Bulk retry process encountered an error: {str(e)}")

def retry_single_order(package, url, service, user_id):
    """Retry a single order and return success status - ONLY for TikTok Likes & Views services"""
    try:
        # Handle only TikTok Likes & Views services
        if package in SERVICES:
            # TikTok combo service (likes + views)
            # For LIKES: Use exact original amount
            payload_likes = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_LIKES_SERVICE_ID,
                "link": url,
                "quantity": service['likes']  # Exact original amount
            }
            likes_order_id = make_smm_request_with_retry(payload_likes, f"Retry ❤️ Likes ({service['likes']})")
            
            # For VIEWS: Use random amount between 1K-10K
            random_views = random.randint(1000, 10000)
            payload_views = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_VIEWS_SERVICE_ID,
                "link": url,
                "quantity": random_views  # Random 1K-10K views
            }
            views_order_id = make_smm_request_with_retry(payload_views, f"Retry 👀 Views ({random_views})")
            
            # Save the retry order
            db.add_order(user_id, {
                'package': f"RETRY: {package} (L:{service['likes']}, V:{random_views})",
                'url': url,
                'price': 0,  # No charge for retries
                'likes_order_id': likes_order_id,
                'views_order_id': views_order_id,
                'status': "Completed" if likes_order_id != "Failed" or views_order_id != "Failed" else "Failed",
                'error': None
            })
            
            return likes_order_id != "Failed" or views_order_id != "Failed"
            
        elif package in TIKTOK_VIEW_SERVICES:
            # TikTok Views Only service
            # For Views Only: Use random amount between 1K-10K
            random_views = random.randint(1000, 10000)
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_VIEWS_SERVICE_ID,
                "link": url,
                "quantity": random_views  # Random 1K-10K views
            }
            
            order_id = make_smm_request_with_retry(payload, f"Retry TikTok Views ({random_views})")
            
            # Save the retry order
            db.add_order(user_id, {
                'package': f"RETRY: {package} (V:{random_views})",
                'url': url,
                'price': 0,  # No charge for retries
                'likes_order_id': None,
                'views_order_id': order_id,
                'status': "Completed" if order_id != "Failed" else "Failed",
                'error': None
            })
            
            return order_id != "Failed"
        
        # If it's not a supported service type, return False
        return False
        
    except Exception as e:
        logger.error(f"Error retrying single order: {e}")
        return False

# Global dictionary to store retry data temporarily
retry_data = {}

# ==================== END BULK RETRY HANDLERS ====================

# ==================== END TELEGRAM STARS HANDLERS ====================

# Service Selection Handler - Must come after all navigation handlers
@bot.message_handler(func=lambda message: any(message.text in d for d in [
    SERVICES, TIKTOK_VIEW_SERVICES, TIKTOK_SAVE_SERVICES, TIKTOK_SHARE_SERVICES, TIKTOK_FOLLOWERS_SERVICES,
    FB_PAGE_FOLLOWERS, FB_PROFILE_FOLLOWERS, FB_VIDEO_VIEWS, FB_REACTIONS,
    TELEGRAM_MEMBER_7DAY, TELEGRAM_MEMBER_30DAY, TELEGRAM_MEMBER_LIFETIME,
    TELEGRAM_VIEW_SERVICES,
    TELEGRAM_MIX_POSITIVE_REACTIONS, TELEGRAM_MIX_NEGATIVE_REACTIONS
]) and message.text not in [
    # Navigation buttons to exclude
    "🔙 Back", "🔙 Back to Main Menu", "🔙 Back to Services Menu",
    "🔙 Back to TikTok Services", "🔙 Back to Telegram Services",
    "🔙 Back to Facebook Services", "🔙 Back to Duration Selection",
    "❌ Cancel Order", "✅ Confirm Order",
    # Sub-category buttons to exclude
    "❤️ TikTok Likes & Views",
    "👀 TikTok Views Only", "👥 TikTok Followers", "💾 TikTok Saves", "📤 TikTok Shares",
    "👥 Facebook Page Followers", "👤 Facebook Profile Followers",
    "👀 Facebook Video Views", "❤️ Facebook Reactions",
    "👥 Telegram Members", "👀 Telegram Views",
    "😊 Mix Positive Reactions", "😡 Mix Negative Reactions",
    "⏳ 7-Day Members", "📆 30-Day Members", "♾️ Lifetime Members"
])
def handle_service_selection(message):
    service_name = message.text
    user_id = message.chat.id
    user = get_cached_user(user_id)
    balance = user['balance']
    service = None
    # Search in all service dicts
    for service_dict in [
        SERVICES, TIKTOK_VIEW_SERVICES, TIKTOK_SAVE_SERVICES, TIKTOK_SHARE_SERVICES, TIKTOK_FOLLOWERS_SERVICES,
        FB_PAGE_FOLLOWERS, FB_PROFILE_FOLLOWERS, FB_VIDEO_VIEWS, FB_REACTIONS,
        TELEGRAM_MEMBER_7DAY, TELEGRAM_MEMBER_30DAY, TELEGRAM_MEMBER_LIFETIME,
        TELEGRAM_VIEW_SERVICES,
        TELEGRAM_MIX_POSITIVE_REACTIONS, TELEGRAM_MIX_NEGATIVE_REACTIONS
    ]:
        if service_name in service_dict:
            service = service_dict[service_name]
            break
    if not service:
        bot.reply_to(message, "❌ Invalid service.", reply_markup=create_main_menu_keyboard())
        return
    price = service['price']
    if balance < price:
        text = f"❌ Insufficient balance.\n💰 Need ${price - balance:.2f} more."
        kb = create_back_keyboard()
        user_states[user_id] = "add_funds"
    else:
        text = f"✅ Ready to order!\n📦 {service_name}\n💰 ${price:.2f}\n💵 Balance: ${balance:.2f}"
        kb = create_order_confirmation_keyboard()
        user_states[user_id] = "confirm_order"
    transactions[user_id] = {"package_name": service_name, "price": price}
    bot.reply_to(message, text, reply_markup=kb)
def place_smm_order(user_id):
    try:
        t = transactions.get(user_id, {})
        pkg = t.get("package_name")
        url = t.get("url")
        if not pkg or not url:
            logger.error(f"Missing package or URL for user {user_id}")
            return
        service = None
        service_type = None
        # Search in all service dicts to identify service type
        for d in [
            SERVICES, TIKTOK_VIEW_SERVICES, TIKTOK_SAVE_SERVICES, TIKTOK_SHARE_SERVICES, TIKTOK_FOLLOWERS_SERVICES,
            FB_PAGE_FOLLOWERS, FB_PROFILE_FOLLOWERS, FB_VIDEO_VIEWS, FB_REACTIONS,
            TELEGRAM_MEMBER_7DAY, TELEGRAM_MEMBER_30DAY, TELEGRAM_MEMBER_LIFETIME,
            TELEGRAM_VIEW_SERVICES,
            TELEGRAM_MIX_POSITIVE_REACTIONS, TELEGRAM_MIX_NEGATIVE_REACTIONS
        ]:
            if pkg in d:
                service = d[pkg]
                service_type = d
                break
        if not service:
            logger.error(f"Unknown package: {pkg}")
            bot.send_message(user_id, "❌ Service not found.\n\n🔧 This might be a configuration issue.\n📞 Please contact support: @jakliketiktok")
            return
        # Process based on service type
        order_id = None
        success_messages = []
        error_messages = []
        # 1. TIKTOK COMBO SERVICES (LIKES & VIEWS)
        if pkg in SERVICES:
            payload_likes = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_LIKES_SERVICE_ID,
                "link": url,
                "quantity": service['likes']
            }
            likes_order_id = make_smm_request_with_retry(payload_likes, "❤️ Likes")
            if likes_order_id != "Failed":
                success_messages.append(f"❤️ Likes: #{likes_order_id}")
            else:
                error_messages.append("❤️ Likes: Failed after 3 retries")
            payload_views = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_VIEWS_SERVICE_ID,
                "link": url,
                "quantity": service['views']
            }
            views_order_id = make_smm_request_with_retry(payload_views, "👀 Views")
            if views_order_id != "Failed":
                success_messages.append(f"👀 Views: #{views_order_id}")
            else:
                error_messages.append("👀 Views: Failed after 3 retries")
            status = "Completed" if likes_order_id != "Failed" or views_order_id != "Failed" else "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': likes_order_id,
                'views_order_id': views_order_id,
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if pkg in SERVICES:  # Only for TikTok Combo services
                if likes_order_id != "Failed":
                    order_id_text += f"Order ID: {likes_order_id}"
                if views_order_id != "Failed":
                    if order_id_text:
                        order_id_text += "\n"
                    order_id_text += f"Views order ID: {views_order_id}"
            else:  # For ALL other services (single order ID)
                if 'order_id' in locals() and order_id != "Failed":
                    order_id_text = f"Order ID: {order_id}"
                elif 'likes_order_id' in locals() and likes_order_id != "Failed":
                    order_id_text = f"Order ID: {likes_order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if likes_order_id != "Failed":
                user_order_info += f"❤️ Like Order ID : <code>{likes_order_id}</code>\n"
            if views_order_id != "Failed":
                user_order_info += f"👀 Views Order ID : <code>{views_order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
            
            # Start status checking
            if likes_order_id != "Failed":
                executor.submit(check_order_status, user_id, likes_order_id, "❤️ Likes", url, pkg)
            if views_order_id != "Failed":
                executor.submit(check_order_status, user_id, views_order_id, "👀 Views", url, pkg)
        # 2. TIKTOK VIEWS ONLY
        elif pkg in TIKTOK_VIEW_SERVICES:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_VIEWS_SERVICE_ID,
                "link": url,
                "quantity": service['views']
            }
            order_id = make_smm_request_with_retry(payload, "👀 Views")
            if order_id != "Failed":
                success_messages.append(f"👀 Views: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👀 Views", url, pkg)
            else:
                error_messages.append("👀 Views: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'views_order_id': order_id,
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👀 Views Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 3. TIKTOK SAVES
        elif pkg in TIKTOK_SAVE_SERVICES:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_SAVES_SERVICE_ID,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "💾 Saves")
            if order_id != "Failed":
                success_messages.append(f"💾 Saves: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "💾 Saves", url, pkg)
            else:
                error_messages.append("💾 Saves: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for saves
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"💾 Saves Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 4. TIKTOK SHARES
        elif pkg in TIKTOK_SHARE_SERVICES:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_SHARES_SERVICE_ID,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "📤 Shares")
            if order_id != "Failed":
                success_messages.append(f"📤 Shares: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "📤 Shares", url, pkg)
            else:
                error_messages.append("📤 Shares: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for shares
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"📤 Shares Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 5. TIKTOK FOLLOWERS
        elif pkg in TIKTOK_FOLLOWERS_SERVICES:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TIKTOK_FOLLOWERS_SERVICE_ID,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "👥 TikTok Followers")
            if order_id != "Failed":
                success_messages.append(f"👥 TikTok Followers: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👥 TikTok Followers", url, pkg)
            else:
                error_messages.append("👥 TikTok Followers: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for followers
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")

            # Unified order notification - Shows order ID
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')

            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👥 Followers Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 6. FACEBOOK SERVICES
        elif pkg in FB_PAGE_FOLLOWERS or pkg in FB_PROFILE_FOLLOWERS:
            service_id = FB_PAGE_FOLLOWERS_ID  # Same for both page and profile followers
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": service_id,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "👥 Facebook Followers")
            if order_id != "Failed":
                success_messages.append(f"👥 Facebook Followers: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👥 Facebook Followers", url, pkg)
            else:
                error_messages.append("👥 Facebook Followers: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for followers
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👥 Followers Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 6. FACEBOOK VIDEO VIEWS
        elif pkg in FB_VIDEO_VIEWS:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": FB_VIDEO_VIEWS_ID,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "👀 Facebook Video Views")
            if order_id != "Failed":
                success_messages.append(f"👀 Facebook Video Views: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👀 Facebook Video Views", url, pkg)
            else:
                error_messages.append("👀 Facebook Video Views: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for views
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👀 Views Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 7. FACEBOOK REACTIONS
        elif pkg in FB_REACTIONS:
            service_id = service.get('service_id', FB_REACTIONS_LIKE_ID)
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": service_id,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "❤️ Facebook Reactions")
            if order_id != "Failed":
                success_messages.append(f"❤️ Facebook Reactions: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "❤️ Facebook Reactions", url, pkg)
            else:
                error_messages.append("❤️ Facebook Reactions: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for reactions
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"❤️ Reactions Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 8. TELEGRAM MEMBERS
        elif pkg in TELEGRAM_MEMBER_7DAY or pkg in TELEGRAM_MEMBER_30DAY or pkg in TELEGRAM_MEMBER_LIFETIME:
            # Determine service ID based on duration
            if pkg in TELEGRAM_MEMBER_7DAY:
                service_id = TG_MEMBER_7DAY_ID
            elif pkg in TELEGRAM_MEMBER_30DAY:
                service_id = TG_MEMBER_30DAY_ID
            else:
                service_id = TG_MEMBER_LIFETIME_ID
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": service_id,
                "link": url,
                "quantity": service['members']
            }
            order_id = make_smm_request_with_retry(payload, "👥 Telegram Members")
            if order_id != "Failed":
                success_messages.append(f"👥 Telegram Members: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👥 Telegram Members", url, pkg)
            else:
                error_messages.append("👥 Telegram Members: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for members
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👥 Members Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 9. TELEGRAM VIEWS
        elif pkg in TELEGRAM_VIEW_SERVICES:
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": TG_VIEW_SERVICE_ID,
                "link": url,
                "quantity": service['views']
            }
            order_id = make_smm_request_with_retry(payload, "👀 Telegram Views")
            if order_id != "Failed":
                success_messages.append(f"👀 Telegram Views: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "👀 Telegram Views", url, pkg)
            else:
                error_messages.append("👀 Telegram Views: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for views
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_text = ""
            if 'order_id' in locals() and order_id != "Failed":
                order_id_text = f"Order ID: {order_id}"

            user_name = get_user_display_name(user_id)
            success_text = "Success ✅" if success_messages else "Processing..."

            # THIS IS THE GROUP NOTIFICATION - Updated to requested format
            order_notification = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"{order_id_text}\n"
                f"🔗 Post: {url}\n"
                f"🆔 User ID: {user_id}\n"
                f"👤 Username: {user_name}\n"
                f"📦 Product: {pkg}\n"
                f"💸 Price: ${service['price']:.2f}\n"
                f"📊 Status: {success_text}"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Updated with correct format
            user_order_info = (
                f"❇️ <b>New Order Successfully</b>\n"
                f"🛒 : {pkg}\n"
                f"🔗 : {url}\n"
            )
            if order_id != "Failed":
                user_order_info += f"👀 Views Order ID : <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 : ${service['price']:.2f}\n"
                f"⏰ : សូមរងចាំ 1-15នាទី\n\n"
                f"ℹ️ Your order is now processing. Most orders complete within 1-15 minutes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
        # 10. TELEGRAM MIX REACTIONS
        elif pkg in TELEGRAM_MIX_POSITIVE_REACTIONS or pkg in TELEGRAM_MIX_NEGATIVE_REACTIONS:
            service_id = TG_MIX_POSITIVE_REACTIONS_ID if pkg in TELEGRAM_MIX_POSITIVE_REACTIONS else TG_MIX_NEGATIVE_REACTIONS_ID
            payload = {
                "key": SMM_API_KEY,
                "action": "add",
                "service": service_id,
                "link": url,
                "quantity": service['quantity']
            }
            order_id = make_smm_request_with_retry(payload, "😊 Telegram Reactions")
            if order_id != "Failed":
                success_messages.append(f"😊 Telegram Reactions: #{order_id}")
                status = "Processing"
                # Start status checking
                executor.submit(check_order_status, user_id, order_id, "😊 Telegram Reactions", url, pkg)
            else:
                error_messages.append("😊 Telegram Reactions: Failed after 3 retries")
                status = "Failed"
            # Save order details
            db.add_order(user_id, {
                'package': pkg,
                'url': url,
                'price': service['price'],
                'likes_order_id': order_id,  # Using likes_order_id for reactions
                'status': status,
                'error': "\n".join(error_messages) if error_messages else None
            })
            # Delete the processing message if it exists
            if user_id in transactions and "processing_message_id" in transactions[user_id]:
                try:
                    bot.delete_message(user_id, transactions[user_id]["processing_message_id"])
                except Exception as e:
                    logger.warning(f"Could not delete processing message: {e}")
            
            # Unified order notification - Shows Views order ID ONLY for combo services
            order_id_display = order_id if 'order_id' in locals() and order_id != "Failed" else "Processing..."

            user_name = get_user_display_name(user_id)
            success_text = "Completed ✅" if success_messages else "Processing ⏳"

            # THIS IS THE GROUP NOTIFICATION - Beautiful admin format
            order_notification = (
                f"🎯 <b>NEW ORDER PLACED</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 <b>Customer:</b> {user_name} (<code>{user_id}</code>)\n"
                f"📦 <b>Service:</b> {pkg}\n"
                f"💰 <b>Amount:</b> ${service['price']:.2f}\n"
                f"🌐 <b>Target:</b> <a href='{url}'>View Post</a>\n"
                f"🆔 <b>Order ID:</b> <code>{order_id_display}</code>\n"
                f"📊 <b>Status:</b> {success_text}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            )

            send_with_retry(ORDER_GROUP_ID, order_notification, parse_mode='HTML')
            
            # THIS IS THE USER MESSAGE - Clean & friendly format
            user_order_info = (
                f"🎉 <b>Order Placed Successfully!</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Service:</b> {pkg}\n"
                f"🔗 <b>Target Link:</b> <a href='{url}'>Your Post</a>\n"
            )
            if order_id != "Failed":
                user_order_info += f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n"
            user_order_info += (
                f"💰 <b>Cost:</b> ${service['price']:.2f}\n"
                f"⏱️ <b>Processing Time:</b> 1-15 minutes\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🚀 <b>Your order is now in progress!</b>\n"
                f"💫 Most orders complete within 1-15 minutes.\n"
                f"📱 You'll receive updates as your order processes."
            )
            bot.send_message(user_id, user_order_info, parse_mode='HTML')
    except Exception as e:
        logger.exception(f"Order error for {user_id}: {e}")
        db.add_order(user_id, {
            'package': pkg,
            'url': url,
            'price': service.get('price', 0),
            'status': 'Failed',
            'error': str(e)
        })
        bot.send_message(user_id, "❌ An error occurred. Contact admin.")
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_telegram_url")
def process_service_url(message):
    user_id = message.chat.id
    url = message.text.strip()
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Invalid URL.", reply_markup=create_main_menu_keyboard())
        return
    pkg = transactions.get(user_id, {}).get("package_name")
    service = None
    for d in [
        SERVICES, TIKTOK_VIEW_SERVICES, TIKTOK_SAVE_SERVICES, TIKTOK_SHARE_SERVICES, TIKTOK_FOLLOWERS_SERVICES,
        FB_PAGE_FOLLOWERS, FB_PROFILE_FOLLOWERS, FB_VIDEO_VIEWS, FB_REACTIONS,
        TELEGRAM_MEMBER_7DAY, TELEGRAM_MEMBER_30DAY, TELEGRAM_MEMBER_LIFETIME,
        TELEGRAM_VIEW_SERVICES,
        TELEGRAM_MIX_POSITIVE_REACTIONS, TELEGRAM_MIX_NEGATIVE_REACTIONS
    ]:
        if pkg in d:
            service = d[pkg]
            break
    if not service:
        bot.reply_to(message, "❌ Service not found.")
        return
    user = get_cached_user(user_id)
    if user['balance'] < service['price']:
        bot.reply_to(message, "❌ Insufficient balance.")
        return
    # Use the dedicated function that logs the history
    new_balance = deduct_user_funds(user_id, service['price'], f"Order: {pkg}")
    transactions[user_id]["url"] = url
    user_states[user_id] = "main_menu"
    
    # Send processing message FIRST
    processing_msg = (
        "⚡ <b>Processing Your Order...</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>Connecting to service providers</b>\n"
        "⏳ <b>Estimated time:</b> 30-60 seconds\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 <b>Please wait while we process your request!</b>\n"
        "💫 Your order will be ready shortly..."
    )
    sent_msg = bot.send_message(user_id, processing_msg, parse_mode='HTML')
    
    # Store the message ID for later deletion
    if user_id not in transactions:
        transactions[user_id] = {}
    transactions[user_id]["processing_message_id"] = sent_msg.message_id
    
    # Then schedule the actual order placement
    executor.submit(place_smm_order, user_id)
def check_order_status(user_id, order_id, service_name, url, package_name=None):
    max_checks = 60
    for _ in range(max_checks):
        time.sleep(30)
        try:
            r = requests.post(SMM_API_URL, data={
                "key": SMM_API_KEY,
                "action": "status",
                "order": order_id
            }, timeout=10)
            if r.status_code == 200:
                data = r.json()
                status = data.get("status")

                # The API might send an "error" field for certain cancellations.
                if "error" in data:
                    error_message = data["error"]
                    # Log the error. We do not refund here because the SMM panel
                    # likely hasn't refunded us for a user-side issue.
                    bot.send_message(user_id, f"❌ An error occurred with your order #{order_id}: {error_message}", parse_mode='HTML')
                    break

                # The main refund logic is here.
                # Check for "Canceled" or "Refunded" status.
                if status in ["Canceled", "Refunded"]:
                    # Check the reason for cancellation if provided by the API.
                    # This helps to avoid refunding for user-side errors (e.g., wrong link).
                    cancellation_reason = data.get("reason", "").lower()
                    
                    # You MUST customize this list of reasons based on your SMM panel's documentation.
                    # These are examples of reasons that usually do NOT trigger a refund from the panel.
                    no_refund_reasons = ["wrong link", "private", "not found", "link is not public"]

                    if any(reason in cancellation_reason for reason in no_refund_reasons):
                        # The SMM panel won't refund you, so you should not refund the user.
                        bot.send_message(user_id, f"❌ {service_name} order #{order_id} was canceled due to a user-side issue (e.g., wrong link, private account). No refund has been issued.", parse_mode='HTML')
                        logger.info(f"Order {order_id} ({service_name}) canceled - No refund (user error)")
                    else:
                        # For other cancellation reasons, assume the SMM panel has refunded you
                        # and pass the refund on to the user.
                        # Get the service details to refund the correct amount
                        service = None
                        for d in [
                            SERVICES, TIKTOK_VIEW_SERVICES, TIKTOK_SAVE_SERVICES, TIKTOK_SHARE_SERVICES, TIKTOK_FOLLOWERS_SERVICES,
                            FB_PAGE_FOLLOWERS, FB_PROFILE_FOLLOWERS, FB_VIDEO_VIEWS, FB_REACTIONS,
                            TELEGRAM_MEMBER_7DAY, TELEGRAM_MEMBER_30DAY, TELEGRAM_MEMBER_LIFETIME,
                            TELEGRAM_VIEW_SERVICES,
                            TELEGRAM_MIX_POSITIVE_REACTIONS, TELEGRAM_MIX_NEGATIVE_REACTIONS
                        ]:
                            for name, s in d.items():
                                if name == package_name:
                                    service = s
                                    break
                            if service:
                                break
                        
                        if service:
                            refund_user(user_id, service['price'], f"{service_name} order canceled by API.")
                        else:
                            refund_user(user_id, 0.0, f"{service_name} order canceled. Contact admin for manual refund.")
                    break
                elif status == "Completed":
                    bot.send_message(user_id, f"🎉 {service_name} order completed!\n🔗 {url}", parse_mode='HTML')
                    break
        except Exception as e:
            logger.error(f"Error checking status for order {order_id}: {e}")
    else:
        bot.send_message(user_id, f"🕒 {service_name} is still processing. Please check later.", parse_mode='HTML')
def make_smm_request_with_retry(payload, label, max_retries=3):
    for i in range(max_retries):
        try:
            logger.info(f"Attempt {i+1}/{max_retries} for {label}: {payload}")
            r = requests.post(SMM_API_URL, data=payload, timeout=15)
            if r.status_code == 200:
                data = r.json()
                order_id = data.get("order")
                if order_id:
                    logger.info(f"✅ Success: {label} → Order ID: {order_id}")
                    return order_id
                else:
                    error = data.get("error", "Unknown error")
                    logger.warning(f"❌ API Error (attempt {i+1}): {error}")
            else:
                logger.warning(f"❌ HTTP {r.status_code} (attempt {i+1})")
        except Exception as e:
            logger.error(f"❌ Request failed (attempt {i+1}): {e}")
        if i < max_retries - 1:
            time.sleep(3)
    logger.error(f"❌ Failed after {max_retries} attempts: {label}")
    return "Failed"
@bot.message_handler(func=lambda message: message.text in ["📋 Order History/ប្រវត្តិនៃការបញ្ជាទិញ", "📋 Order History", "📋 ប្រវត្តិនៃការបញ្ជាទិញ"])
def show_order_history(message):
    user_id = message.chat.id
    orders = db.get_user_orders(user_id, 5)
    if not orders:
        text = get_text(user_id, "no_recent_orders", default="📋 No recent orders.")
    else:
        text = get_text(user_id, "recent_orders_title", default="📋 <b>Recent Orders</b>:\n")
        for i, o in enumerate(orders, 1):
            line = f"<b>#{i}</b> 💰 ${o['price']:.2f}\n📦 {o['package']}\n🔗 {o['url']}"
            if o.get('likes_order_id'):
                line += f"\n❤️ Likes ID: <code>#{o['likes_order_id']}</code>"
            if o.get('views_order_id'):
                line += f"\n👀 Views ID: <code>#{o['views_order_id']}</code>"
            if o.get('status'):
                line += f"\n📊 Status: {o['status']}"
            if i < len(orders):
                line += "\n\n"
            text += line
    bot.reply_to(message, text, parse_mode='HTML', reply_markup=create_main_menu_keyboard(user_id))
# Order Status Feature - Shows detailed status for all orders without requiring order ID input
@bot.message_handler(func=lambda message: message.text in ["🔍 Order Status/ស្ថានភាពការបញ្ជាទិញ", "🔍 Order Status", "🔍 ស្ថានភាពការបញ្ជាទិញ"])
def show_all_order_statuses(message):
    user_id = message.chat.id
    orders = db.get_user_orders(user_id, 10)  # Get most recent 10 orders
    if not orders:
        no_orders_text = get_text(user_id, "no_orders_to_check", default="🔍 No orders to check status for.")
        bot.reply_to(message, no_orders_text, reply_markup=create_main_menu_keyboard(user_id))
        return
    response = get_text(user_id, "detailed_order_status_title", default="🔍 <b>Detailed Order Status (Last 10 Orders)</b>\n")
    order_count = 0
    for order in orders:
        package = order['package']
        url = order['url']
        price = order['price']
        # Check likes order status if exists
        likes_order_id = order.get('likes_order_id')
        if likes_order_id and likes_order_id != "Failed":
            try:
                r = requests.post(SMM_API_URL, data={
                    "key": SMM_API_KEY,
                    "action": "status",
                    "order": likes_order_id
                }, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if "error" in data:
                        error_msg = data["error"]
                        response += f"❤️ <b>Likes Order</b>\n"
                        response += f"📦 Package: {package}\n"
                        response += f"🔗 URL: {url}\n"
                        response += f"🆔 Order ID: <code>{likes_order_id}</code>\n"
                        response += f"❌ API Error: {error_msg}\n"
                        order_count += 1
                    else:
                        status = data.get("status", "Unknown")
                        remains = data.get("remains", "N/A")
                        start_count = data.get("start_count", "N/A")
                        response += f"❤️ <b>Likes Order</b>\n"
                        response += f"📦 Package: {package}\n"
                        response += f"🔗 URL: {url}\n"
                        response += f"🆔 Order ID: <code>{likes_order_id}</code>\n"
                        response += f"📊 Status: <b>{status}</b>\n"
                        response += f"📈 Start Count: {start_count}\n"
                        response += f"🔄 Remains: {remains}\n"
                        order_count += 1
            except Exception as e:
                logger.error(f"Error checking likes order status for {likes_order_id}: {e}")
                response += f"❤️ <b>Likes Order</b>\n"
                response += f"📦 Package: {package}\n"
                response += f"🔗 URL: {url}\n"
                response += f"🆔 Order ID: <code>{likes_order_id}</code>\n"
                response += f"❌ Connection Error\n"
                order_count += 1
        # Check views order status if exists
        views_order_id = order.get('views_order_id')
        if views_order_id and views_order_id != "Failed":
            try:
                r = requests.post(SMM_API_URL, data={
                    "key": SMM_API_KEY,
                    "action": "status",
                    "order": views_order_id
                }, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if "error" in data:
                        error_msg = data["error"]
                        response += f"👀 <b>Views Order</b>\n"
                        response += f"📦 Package: {package}\n"
                        response += f"🔗 URL: {url}\n"
                        response += f"🆔 Order ID: <code>{views_order_id}</code>\n"
                        response += f"❌ API Error: {error_msg}\n"
                        order_count += 1
                    else:
                        status = data.get("status", "Unknown")
                        remains = data.get("remains", "N/A")
                        start_count = data.get("start_count", "N/A")
                        response += f"👀 <b>Views Order</b>\n"
                        response += f"📦 Package: {package}\n"
                        response += f"🔗 URL: {url}\n"
                        response += f"🆔 Order ID: <code>{views_order_id}</code>\n"
                        response += f"📊 Status: <b>{status}</b>\n"
                        response += f"📈 Start Count: {start_count}\n"
                        response += f"🔄 Remains: {remains}\n"
                        order_count += 1
            except Exception as e:
                logger.error(f"Error checking views order status for {views_order_id}: {e}")
                response += f"👀 <b>Views Order</b>\n"
                response += f"📦 Package: {package}\n"
                response += f"🔗 URL: {url}\n"
                response += f"🆔 Order ID: <code>{views_order_id}</code>\n"
                response += f"❌ Connection Error\n"
                order_count += 1
    if order_count == 0:
        no_active_orders_text = get_text(user_id, "no_active_orders", default="🔍 No active orders to check status for.")
        bot.reply_to(message, no_active_orders_text, reply_markup=create_main_menu_keyboard(user_id))
    else:
        bot.reply_to(message, response, parse_mode='HTML', reply_markup=create_main_menu_keyboard(user_id))
# Optimized "How to buy" handler - Uses file ID for instant delivery
@bot.message_handler(func=lambda message: message.text in ["🛒 Tutorial/របៀបប្រើប្រាស់", "🛒 Tutorial", "🛒 របៀបប្រើប្រាស់"])
def send_how_to_buy_video(message):
    user_id = message.chat.id
    try:
        if not VIDEO_FILE_ID or VIDEO_FILE_ID == 'YOUR_VIDEO_FILE_ID_HERE':
            bot.reply_to(message, "❌ The video file ID has not been configured by the administrator.")
            logger.error("Video file ID not set. Please obtain the video file ID and update the VIDEO_FILE_ID variable.")
            return
        bot.send_video(
            user_id,
            VIDEO_FILE_ID,
            caption="💎 How to buy in BOT!",
            reply_markup=create_main_menu_keyboard(user_id)
        )
        logger.info(f"Sent video using File ID to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send video using File ID: {e}")
        bot.reply_to(message, "❌ Video not found or an error occurred. Contact admin.")

@bot.message_handler(func=lambda message: message.text == "🌐 Mini App")
def handle_mini_app_button(message):
    """Handle mini app button from main menu"""
    user_id = message.chat.id
    
    # Create keyboard with mini app button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "🌐 Open JakLike Mini App", 
            web_app=types.WebAppInfo(url="https://chheanforwarder123.onrender.com/auto-login")
        )
    )
    
    bot.reply_to(message,
        "🎯 **JakLike Mini App**\n\n"
        "Access your account from anywhere with our new web interface!\n\n"
        "✨ **Features:**\n"
        "• Check balance instantly\n"
        "• View order history\n"
        "• Manage your profile\n"
        "• Mobile-friendly design\n\n"
        "Click the button below to open:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
# Mini App Integration
@bot.message_handler(commands=['miniapp'])
def show_mini_app(message):
    """Show mini app button to users"""
    user_id = message.chat.id
    
    # Create keyboard with mini app button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "🌐 Open JakLike Mini App", 
            web_app=types.WebAppInfo(url="https://chheanforwarder123.onrender.com/auto-login")
        )
    )
    
    bot.reply_to(message,
        "🎯 **JakLike Mini App**\n\n"
        "Access your account from anywhere with our new web interface!\n\n"
        "✨ **Features:**\n"
        "• Check balance instantly\n"
        "• View order history\n"
        "• Manage your profile\n"
        "• Mobile-friendly design\n\n"
        "Click the button below to open:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['webapp'])
def show_webapp_menu(message):
    """Show web app menu with mini app option"""
    user_id = message.chat.id
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("🌐 Mini App", callback_data="open_mini_app"),
        types.InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")
    )
    keyboard.add(
        types.InlineKeyboardButton("📦 My Orders", callback_data="my_orders"),
        types.InlineKeyboardButton("👤 My Profile", callback_data="my_profile")
    )
    
    bot.reply_to(message,
        "🎯 **JakLike Web Interface**\n\n"
        "Choose an option:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "open_mini_app")
def handle_mini_app_callback(call):
    """Handle mini app button clicks"""
    user_id = call.from_user.id
    
    # Open mini app
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "🚀 Open Mini App", 
            web_app=types.WebAppInfo(url="https://chheanforwarder123.onrender.com/auto-login")
        )
    )
    
    bot.edit_message_text(
        "🌐 **JakLike Mini App**\n\n"
        "Click the button below to open your account dashboard:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_balance")
def handle_check_balance_callback(call):
    """Handle check balance callback"""
    user_id = call.from_user.id
    user = get_cached_user(user_id)
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        f"💰 **Your Balance**\n\n"
        f"💵 Current Balance: ${user['balance']:.2f}\n"
        f"📊 Total Orders: {user.get('total_orders', 0)}\n"
        f"💸 Total Spent: ${user.get('total_spent', 0):.2f}",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "my_orders")
def handle_my_orders_callback(call):
    """Handle my orders callback"""
    user_id = call.from_user.id
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "📦 **Your Orders**\n\n"
        "To view your detailed order history, please use the Mini App or send /order_history command.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "my_profile")
def handle_my_profile_callback(call):
    """Handle my profile callback"""
    user_id = call.from_user.id
    user = get_cached_user(user_id)
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        f"👤 **Your Profile**\n\n"
        f"🆔 User ID: {user_id}\n"
        f"💰 Balance: ${user['balance']:.2f}\n"
        f"📅 Member Since: {user.get('registration_date', 'Unknown')}\n"
        f"🌍 Language: {user.get('language', 'English')}\n"
        f"📊 Total Orders: {user.get('total_orders', 0)}\n"
        f"💸 Total Spent: ${user.get('total_spent', 0):.2f}",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

# Start polling
if __name__ == "__main__":
    logger.info("Bot is starting...")
    print("🚀 Starting High-Performance SMM Bot...")
    print(f"⚡ ThreadPool Workers: {executor._max_workers}")
    print(f"💾 Cache Timeout: {CACHE_TIMEOUT}s")
    print("🔥 Bot is ready for instant responses!")
    print("🌐 Mini App URL: https://chheanforwarder123.onrender.com/auto-login")
    
    # Ultra-fast polling configuration
    bot.infinity_polling(
        timeout=10,           # Faster timeout for quicker responses
        long_polling_timeout=20,  # Optimized long polling
        skip_pending=True,    # Skip old messages for faster startup
        interval=0.1          # Minimal interval between polling
    )