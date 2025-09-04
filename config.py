# Configuration file for JakLike User Web App

# Admin Telegram IDs (users with admin access)
ADMIN_IDS = [1]

# Database configuration
DB_FILE = "bot_data.db"

# SMM API Configuration (update these with your actual API details)
SMM_API_URL = "https://chhean-smm.net/api/v2"
SMM_API_KEY = "8bf8bc269ff40c0f472aff557505a485"

# App configuration
APP_NAME = "JakLike"
APP_VERSION = "1.0.0"
DEBUG_MODE = False  # Set to False for production
HOST = "0.0.0.0"
PORT = 10000  # Render uses port 10000

# Security settings
SECRET_KEY = None  # Will be auto-generated if None
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Balance sync settings
AUTO_SYNC_INTERVAL = 30  # seconds
BALANCE_UPDATE_ENABLED = True

# Features
ENABLE_ADMIN_CONTROLS = True
ENABLE_BALANCE_SYNC = True
ENABLE_TRANSACTION_HISTORY = True




