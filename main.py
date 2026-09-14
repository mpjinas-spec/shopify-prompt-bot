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

# മൂന്ന് പ്രൊഡക്റ്റുകളുടെയും കൃത്യമായ വിവരങ്ങളും ഫയലുകളും
PRODUCTS = {
    "ai_prompt_vault": {
        "title": "🔥 The Ultimate E-commerce ChatGPT Prompt Vault",
        "description": "110+ high-converting prompts for Shopify store owners (PDF).",
        "price": 850,
        "file_path": "The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners.pdf",
        "cover": "Ecommerce AI Prompt Vault.jpg"
    },
    "notion_system": {
        "title": "📊 Notion Business System",
        "description": "Centralized Notion workspace templates and operational dashboards.",
        "price": 600,
        "file_path": "notion-links.txt",
        "cover": "Notion System.jpg"
    },
    "shopify_playbook": {
        "title": "🚀 Shopify Scale Playbook",
        "description": "Complete 5-Module E-Commerce Growth System.",
        "price": 1000,
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
        "Please choose a digital product or free option below:"
    )
    
    keyboard = []
    # മൂന്ന് പ്രൊഡക്റ്റുകൾക്കുള്ള ബട്ടണുകൾ
    for key, product in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(f"⭐ {product['title']} - {product['price']} Stars", callback_data=f"buy_{key}")])
    
    # ഫ്രീ പ്രൊംപ്റ്റിനുള്ള ബട്ടൺ താഴെ ചേർക്കുന്നു
    keyboard.append([InlineKeyboardButton("🎁 Get Free AI Prompts (Sample)", callback_data="free_prompts")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "free_prompts":
        try:
            with open(PRODUCTS["ai_prompt_vault"]["cover"], 'rb') as photo_file:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo_file,
                    caption="📄 **The Ultimate E-commerce ChatGPT Prompt Vault**\n(Preview of what you get inside)"
                )
        except Exception as e:
            logging.error(f"Failed to send cover image: {e}")

        free_text = (
            "🎁 **Here are 2 Free High-Converting Shopify AI Prompts:**\n\n"
            "**1. Product Description Prompt:**\n"
            "`Act as an expert copywriter. Write a high-converting product description for [Product Name] focusing on benefits, emotional triggers, and bullet points.`\n\n"
            "**2. Instagram/TikTok Ad Hook Prompt:**\n"
            "`Generate 5 viral hook lines for a Shopify store selling [Product Niche] that stops users from scrolling instantly.`\n\n"
            "💡 *Try these out and see how much time they save you!* 🔥"
        )
        keyboard = [[InlineKeyboardButton("⭐ Unlock Full Prompt Vault (850 Stars)", callback_data="buy_ai_prompt_vault")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(free_text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data.startswith("buy_"):
        product_key = query.data.replace("buy_", "")
        product = PRODUCTS.get(product_key)
        
        if not product:
            return

        chat_id = query.message.chat_id
        prices = [LabeledPrice(product['title'], product['price'])]
        
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=product['title'],
            description=product['description'],
            payload=f"payload_{product_key}",
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
    product_key = payload.replace("payload_", "")
    product = PRODUCTS.get(product_key)

    await update.message.reply_text(
        "🎉 Payment Successful! Thank you for your purchase.\n\n"
        "Here is your digital product file. Enjoy! 🚀",
        parse_mode="Markdown"
    )
    
    if product and os.path.exists(product['file_path']):
        try:
            with open(product['file_path'], 'rb') as file_obj:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=file_obj,
                    caption=f"📄 {product['title']}"
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
