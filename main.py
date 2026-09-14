import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters
import nest_asyncio

nest_asyncio.apply()

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "8938226896:AAE6VV3zj01TBicAloOdifyjEl405M7kB-g"

# കൃത്യമായ വിലകളും വ്യത്യസ്തമായ ഡിസ്ക്രിപ്ഷനുകളും അടങ്ങിയ പ്രൊഡക്റ്റ് ലിസ്റ്റ്
PRODUCTS = {
    "project_0": {
        "title": "🔥 The Ultimate E-commerce ChatGPT Prompt Vault",
        "description": "110+ proven prompts for Shopify store owners to scale your store and boost sales instantly! (Full Version).",
        "price": 850,  # നിങ്ങൾ ആവശ്യപ്പെട്ടതുപോലെ 850 Stars
        "is_free": False,
        "file_path": "ecommerce-ai-prompt-vault.pdf"
    },
    "project_1": {
        "title": "💡 Advanced E-commerce Growth Prompts (Project 1)",
        "description": "Advanced AI copywriting & marketing strategies designed specifically for high-growth online stores.",
        "price": 500,  # പുതിയതും മികച്ചതുമായ സ്റ്റാർ വാല്യൂ
        "is_free": False,
        "file_path": "ecommerce-ai-prompt-vault.pdf"
    },
    "notion_system": {
        "title": "📊 Notion Business System",
        "description": "Centralized Notion workspace templates and operational dashboards.",
        "price": 600,
        "is_free": False,
        "file_path": "notion-links.txt"
    },
    "shopify_playbook": {
        "title": "🚀 Shopify Scale Playbook",
        "description": "Complete 5-Module E-Commerce Growth System.",
        "price": 1000,
        "is_free": False,
        "file_path": "THE SHOPIFY SCALE PLAYBOOK.pdf"
    }
}

# Simple Flask app for UptimeRobot to ping
app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# 5 ഓപ്ഷനുകൾ അടങ്ങിയ മെയിൻ മെനു കീബോർഡ്
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁 Free AI Prompts Samples", callback_data="select_free_entry")],
        [InlineKeyboardButton(f"⭐ {PRODUCTS['project_0']['title']} - {PRODUCTS['project_0']['price']} Stars", callback_data="select_project_0")],
        [InlineKeyboardButton(f"⭐ {PRODUCTS['project_1']['title']} - {PRODUCTS['project_1']['price']} Stars", callback_data="select_project_1")],
        [InlineKeyboardButton(f"⭐ {PRODUCTS['notion_system']['title']} - {PRODUCTS['notion_system']['price']} Stars", callback_data="select_notion_system")],
        [InlineKeyboardButton(f"⭐ {PRODUCTS['shopify_playbook']['title']} - {PRODUCTS['shopify_playbook']['price']} Stars", callback_data="select_shopify_playbook")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Hello {user_name}!\n\n"
        "Welcome to **Qyro Scale Hub** 🚀\n"
        "Please choose an option from the menu below:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id

    # ഫ്രീ സാമ്പിൾ എൻട്രി ക്ലിക്ക് ചെയ്യുമ്പോൾ
    if data == "select_free_entry":
        free_text = (
            "🎁 **Free AI Prompts Samples**\n"
            "*(From The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners)*\n\n"
            "**1. Product Description Prompt:**\n"
            "`Act as an expert copywriter. Write a high-converting product description for [Product Name] focusing on benefits and emotional triggers.`\n\n"
            "**2. Instagram/TikTok Ad Hook Prompt:**\n"
            "`Generate 5 viral hook lines for a Shopify store selling [Product Niche] that stops users from scrolling instantly.`\n\n"
            "💡 *Want to unlock the full vaults? Choose your package from the menu below!* 🔥"
        )
        
        # ഫ്രീ മെനുവിനുള്ളിലും അതേ 5 ഓപ്ഷനുകൾ കൃത്യമായി വരുന്നു
        free_keyboard = [
            [InlineKeyboardButton("🎁 Free AI Prompts Samples", callback_data="select_free_entry")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['project_0']['title']} - {PRODUCTS['project_0']['price']} Stars", callback_data="select_project_0")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['project_1']['title']} - {PRODUCTS['project_1']['price']} Stars", callback_data="select_project_1")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['notion_system']['title']} - {PRODUCTS['notion_system']['price']} Stars", callback_data="select_notion_system")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['shopify_playbook']['title']} - {PRODUCTS['shopify_playbook']['price']} Stars", callback_data="select_shopify_playbook")]
        ]
        
        await query.message.reply_text(free_text, reply_markup=InlineKeyboardMarkup(free_keyboard), parse_mode="Markdown")

    elif data.startswith("select_"):
        prod_key = data.replace("select_", "")
        prod = PRODUCTS.get(prod_key)
        
        if not prod:
            return

        # പെയ്ഡ് പ്രൊഡക്റ്റുകൾക്ക് അതത് വിലയും വെവ്വേറെ ഡിസ്ക്രിപ്ഷനും വെച്ച് ഇൻവോയ്സ് അയക്കുന്നു
        prices = [LabeledPrice(prod['title'], prod['price'])]
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=prod['title'],
            description=prod['description'],
            payload=f"payload_{prod_key}",
            provider_token="",
            currency="XTR",
            prices=prices
        )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload.startswith("payload_"):
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    payload = update.message.successful_payment.invoice_payload
    prod_key = payload.replace("payload_", "")
    prod = PRODUCTS.get(prod_key)

    await update.message.reply_text(
        "🎉 Payment Successful! Thank you for your purchase.\n\n"
        "Here is your digital product file. Enjoy! 🚀",
        parse_mode="Markdown"
    )
    
    if prod and 'file_path' in prod and os.path.exists(prod['file_path']):
        try:
            with open(prod['file_path'], 'rb') as file_obj:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=file_obj,
                    caption=f"📄 {prod['title']}"
                )
        except Exception as e:
            logging.error(f"Failed to send file: {e}")
            await update.message.reply_text("⚠️ Error sending the file. Please contact support.")
    else:
        await update.message.reply_text("⚠️ File not found on server. Please contact support.")

def main():
    keep_alive()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
