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
    welcome_text = (
        "Welcome to Ecom AI Growth! 🚀\n\n"
        "Get *The Ultimate E-commerce ChatGPT Prompt Vault* built specifically for Shopify store owners. "
        "110+ battle-tested prompts to scale your store and save hundreds of hours.\n\n"
        "Click the button below to purchase instantly using Telegram Stars."
    )
    keyboard = [[InlineKeyboardButton("Buy Now for 850 ⭐ ($17)", callback_data="buy_prompt")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "buy_prompt":
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
    await update.message.reply_text(
        "🎉 Payment Successful! Thank you for your purchase.\n\n"
        "Here is your *The Ultimate E-commerce ChatGPT Prompt Vault* PDF guide.",
        parse_mode="Markdown"
    )

def main():
    # Start the Flask server in the background for UptimeRobot
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
