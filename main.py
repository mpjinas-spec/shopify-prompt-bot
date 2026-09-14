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

# കൃത്യമായ പ്രൊജക്റ്റുകളും അവയുടെ കവർ ഫയൽ നാമങ്ങളും
PROJECTS = {
    "project_0": {
        "title": "🎁 Project 0: Free AI Prompts (2 Free Samples)",
        "description": "Get your free high-converting AI prompts instantly.",
        "price": 0,
        "is_free": True,
        "cover": "cover.jpg"  # പ്രൊജക്റ്റ് സീറോയുടെ ഒറിജിനൽ കവർ പേര്
    },
    "project_1": {
        "title": "🔥 Project 1: Ecommerce AI Prompt Vault",
        "description": "110+ high-converting prompts for Shopify store owners (PDF).",
        "price": 850,
        "is_free": False,
        "file_path": "The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners.pdf",
        "cover": "Ecommerce AI Prompt Vault.jpg"
    },
    "project_2": {
        "title": "📊 Project 2: Notion Business System",
        "description": "Centralized Notion workspace templates and operational dashboards.",
        "price": 600,
        "is_free": False,
        "file_path": "notion-links.txt",
        "cover": "Notion System.jpg"
    },
    "project_3": {
        "title": "🚀 Project 3: Shopify Scale Playbook",
        "description": "Complete 5-Module E-Commerce Growth System.",
        "price": 1000,
        "is_free": False,
        "file_path": "Shopify_Scale_Playbook_Final.pdf",
        "cover": "Shopify Scale Playbook.jpg"
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Hello {user_name}!\n\n"
        "Welcome to **Qyro Scale Hub** 🚀\n"
        "Choose a project below (Project 0 to Project 3):"
    )
    
    keyboard = []
    
    for key, proj in PROJECTS.items():
        if proj["is_free"]:
            btn_text = f"🎁 {proj['title']}"
        else:
            btn_text = f"⭐ {proj['title']} - {proj['price']} Stars"
        
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"select_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("select_"):
        proj_key = data.replace("select_", "")
        proj = PROJECTS.get(proj_key)
        
        if not proj:
            return

        chat_id = query.message.chat_id
        
        # അതത് പ്രൊജക്റ്റിന്റെ കവർ ഫോട്ടോ അയക്കുന്നു
        cover_file = proj.get('cover')
        if cover_file and os.path.exists(cover_file):
            try:
                with open(cover_file, 'rb') as photo_file:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file,
                        caption=f"📦 **{proj['title']}**\nPreview Cover"
                    )
            except Exception as e:
                logging.error(f"Failed to send cover image: {e}")

        if proj["is_free"]:
            free_text = (
                "🎁 **Project 0: Free AI Prompts Samples**\n\n"
                "**1. Product Description Prompt:**\n"
                "`Act as an expert copywriter. Write a high-converting product description for [Product Name] focusing on benefits and emotional triggers.`\n\n"
                "**2. Instagram/TikTok Ad Hook Prompt:**\n"
                "`Generate 5 viral hook lines for a Shopify store selling [Product Niche] that stops users from scrolling instantly.`\n\n"
                "💡 *Use these for your store! Check out Project 1, 2, and 3 below for full versions.* 🔥"
            )
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
            await query.message.reply_text(free_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
        else:
            prices = [LabeledPrice(proj['title'], proj['price'])]
            await context.bot.send_invoice(
                chat_id=chat_id,
                title=proj['title'],
                description=proj['description'],
                payload=f"payload_{proj_key}",
                provider_token="",
                currency="XTR",
                prices=prices
            )

    elif data == "back_to_menu":
        user_name = update.effective_user.first_name
        welcome_text = f"👋 Welcome back {user_name}!\nChoose a project below (Project 0 to Project 3):"
        keyboard = []
        for key, proj in PROJECTS.items():
            if proj["is_free"]:
                btn_text = f"🎁 {proj['title']}"
            else:
                btn_text = f"⭐ {proj['title']} - {proj['price']} Stars"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"select_{key}")])
        
        await query.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload.startswith("payload_"):
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    payload = update.message.successful_payment.invoice_payload
    proj_key = payload.replace("payload_", "")
    proj = PROJECTS.get(proj_key)

    await update.message.reply_text(
        "🎉 Payment Successful! Thank you for your purchase.\n\n"
        "Here is your project file. Enjoy! 🚀",
        parse_mode="Markdown"
    )
    
    if proj and 'file_path' in proj and os.path.exists(proj['file_path']):
        try:
            with open(proj['file_path'], 'rb') as file_obj:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=file_obj,
                    caption=f"📄 {proj['title']}"
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
