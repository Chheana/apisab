# Bot Integration Example - Add this to your main.py bot file

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def show_mini_app_button(update, context):
    """Show mini app button to users"""
    
    # Create keyboard with mini app button
    keyboard = [
        [InlineKeyboardButton(
            "🌐 Open JakLike Mini App", 
            web_app=WebAppInfo(url="https://your-app-name.onrender.com")
        )],
        [InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")],
        [InlineKeyboardButton("📦 My Orders", callback_data="my_orders")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🎯 **JakLike Mini App**\n\n"
        "Access your account from anywhere with our new web interface!\n\n"
        "✨ **Features:**\n"
        "• Check balance instantly\n"
        "• View order history\n"
        "• Manage your profile\n"
        "• Mobile-friendly design\n\n"
        "Click the button below to open:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_mini_app_in_menu(update, context):
    """Show mini app in main menu"""
    
    keyboard = [
        [InlineKeyboardButton("🌐 Mini App", callback_data="open_mini_app")],
        [InlineKeyboardButton("💰 Add Funds", callback_data="add_funds")],
        [InlineKeyboardButton("📦 Order Services", callback_data="order_services")],
        [InlineKeyboardButton("📊 My Account", callback_data="my_account")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🎯 **JakLike Services**\n\n"
        "Choose an option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def handle_mini_app_callback(update, context):
    """Handle mini app button clicks"""
    query = update.callback_query
    query.answer()
    
    if query.data == "open_mini_app":
        # Open mini app
        keyboard = [[InlineKeyboardButton(
            "🚀 Open Mini App", 
            web_app=WebAppInfo(url="https://your-app-name.onrender.com")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            "🌐 **JakLike Mini App**\n\n"
            "Click the button below to open your account dashboard:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == "check_balance":
        # Show balance info
        user_id = update.effective_user.id
        # Get balance from database and show it
        query.edit_message_text(f"💰 Your current balance: $X.XX")
    
    elif query.data == "my_orders":
        # Show orders info
        query.edit_message_text("📦 Your order history will be shown here")

# Add these handlers to your bot
def setup_mini_app_handlers(dispatcher):
    """Setup mini app related handlers"""
    
    # Command to show mini app
    dispatcher.add_handler(CommandHandler("miniapp", show_mini_app_button))
    
    # Command to show main menu with mini app
    dispatcher.add_handler(CommandHandler("menu", show_mini_app_in_menu))
    
    # Callback query handler for mini app buttons
    dispatcher.add_handler(CallbackQueryHandler(handle_mini_app_callback))

# Example usage in your main.py:
# from bot_integration_example import setup_mini_app_handlers
# setup_mini_app_handlers(dispatcher)

# Or add this command directly to your existing bot:
def add_mini_app_command(update, context):
    """Add /miniapp command to your bot"""
    show_mini_app_button(update, context)

# Add this to your existing command handlers:
# dispatcher.add_handler(CommandHandler("miniapp", add_mini_app_command))




