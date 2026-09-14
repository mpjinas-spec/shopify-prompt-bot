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
PRICE_STARS = 850
PDF_FILENAME = "The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners.pdf"

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
        "Get *The Ultimate E-commerce ChatGPT Prompt Vault* built specifically for Shopify store owners. "
        "110+ battle-tested prompts to scale your store and save hundreds of hours.\n\n"
        "👇 Choose an option below to get started:"
    )
    # ബട്ടണുകൾ അപ്ഡേറ്റ് ചെയ്തു (ഫ്രീ പ്രോംപ്റ്റ് ബട്ടണും പെയ്ഡ് ബട്ടണും ഉൾപ്പെടുത്തി)
    keyboard = [
        [InlineKeyboardButton("🎁 Get Free AI Prompts", callback_data="free_prompts")],
        [InlineKeyboardButton("⭐ Buy Full Vault for 850 ⭐ ($17)", callback_data="buy_prompt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "free_prompts":
        # യൂസർ ഫ്രീ പ്രോംപ്റ്റ് ചോദിക്കുമ്പോൾ കൊടുക്കുന്ന സൗജന്യ വാല്യൂ
        free_text = (
            "🎁 **Here are 2 Free Shopify AI Prompts to start with:**\n\n"
            "**1. High-Converting Product Description Prompt:**\n"
            "`Act as an expert copywriter. Write a high-converting product description for [Product Name] focusing on benefits, emotional triggers, and bullet points for features.`\n\n"
            "**2. Facebook Ad Hook Prompt:**\n"
            "`Generate 5 viral hook lines for a Shopify store selling [Product Niche] that stops users from scrolling on Instagram.`\n\n"
            "⭐ Want all 110+ battle-tested prompts? Click below to unlock the full Pro Vault!",
        )
        keyboard = [[InlineKeyboardButton("⭐ Unlock Full Pro Vault (850 Stars)", callback_data="buy_prompt")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(free_text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "buy_prompt":
        chat_id = query.message.chat_id
        title = "Shopify ChatGPT Prompt Vault"
        description = "Instant download: 110+ high-converting prompts for Shopify store owners (PDF)."
        payload = "shopify_prompt_payload"
        currency = "XTR"
        prices = [LabeledPrice("Prompt Vault PDF", PRICE_STARS)]
        
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",
            currency=currency,
            prices=prices
        )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload == "shopify_prompt_payload":
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(
        "🎉 Payment Successful! Thank you for your purchase.\n\n"
        "Here is your *The Ultimate E-commerce ChatGPT Prompt Vault* PDF guide. Enjoy scaling your Shopify store! 🚀",
        parse_mode="Markdown"
    )
    
    # Send the PDF file automatically
    try:
        with open(PDF_FILENAME, 'rb') as pdf_file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=pdf_file,
                caption="📄 The Ultimate E-commerce ChatGPT Prompt Vault"
            )
    except Exception as e:
        logging.error(f"Failed to send PDF: {e}")
        await update.message.reply_text("⚠️ Error sending the file. Please contact support.")

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
