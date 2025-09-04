import telebot
from telebot import types
import logging
import sys
import sqlite3
import time

# ==================== CONFIGURATION ====================
# Replace with your bot's token
BOT_TOKEN = "7656178814:AAH2LMeSoMkOU95YANHCszAt1ZI4dxqdlIE"
STARS_ENABLED = True
DB_FILE = "bot_data.db"

# =====================================================

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Database Manager
class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0.0,
                registration_date TEXT
            )''')
            conn.commit()

    def get_user(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return {'user_id': row[0], 'balance': row[1], 'registration_date': row[2]}
            return None

    def add_user(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.execute(
                'INSERT OR IGNORE INTO users (user_id, registration_date) VALUES (?, ?)',
                (user_id, time.strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            return cursor.rowcount > 0

db = Database(DB_FILE)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def get_cached_user(user_id):
    user = db.get_user(user_id)
    if not user:
        db.add_user(user_id)
        user = db.get_user(user_id)
    return user

def create_payment_method_keyboard(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if STARS_ENABLED:
        keyboard.add(types.KeyboardButton("⭐ Pay with Stars"))
    keyboard.add(types.KeyboardButton("🔙 Back"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Handles the /start command and sends a welcome message with a payment button.
    """
    logger.info(f"Received /start command from user {message.chat.id}")
    db.add_user(message.chat.id)
    bot.send_message(message.chat.id, "Welcome! This is a simple bot to test Telegram Stars payments.")
    bot.send_message(message.chat.id, "Send /buy to receive an invoice for 10 Stars.")

@bot.message_handler(commands=['buy'])
def handle_buy_command(message):
    """
    Handles the /buy command and sends an invoice to the user.
    """
    chat_id = message.chat.id
    logger.info(f"Received /buy command from user {chat_id}. Creating invoice...")

    # Define the price for the invoice
    prices = [types.LabeledPrice(label="Test Product", amount=1)]  # 10 Stars

    try:
        # Send the invoice
        bot.send_invoice(
            chat_id=chat_id,
            title="Test Invoice",
            description="This is an invoice for a test product.",
            invoice_payload="test-payload",
            provider_token="",  # Must be empty for Telegram Stars
            currency="XTR",  # The currency for Telegram Stars
            prices=prices,
            start_parameter="test-start-parameter"
        )
        logger.info(f"Successfully sent invoice to user {chat_id}")

    except Exception as e:
        logger.error(f"Failed to send invoice to user {chat_id}: {e}")
        bot.send_message(chat_id, f"Sorry, there was an error creating the invoice: {e}")

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_query(query):
    """
    Handles the pre-checkout query from Telegram.
    """
    logger.info(f"Received pre-checkout query from user {query.from_user.id}")
    bot.answer_pre_checkout_query(query.id, ok=True)
    logger.info(f"Answered pre-checkout query for user {query.from_user.id}")

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    """
    Handles the successful payment message.
    """
    chat_id = message.chat.id
    logger.info(f"Received successful payment from user {chat_id}")
    bot.send_message(chat_id, "Payment successful! Thank you for your purchase.")

if __name__ == '__main__':
    logger.info("Bot is starting...")
    bot.polling(non_stop=True)