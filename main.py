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

# മുഴുവൻ പ്രൊഡക്റ്റുകളുടെയും വിവരങ്ങളും കവർ ഫയൽ നാമങ്ങളും
PRODUCTS = {
    "project_0": {
        "title": "🎁 The Ultimate E-commerce ChatGPT Prompt Vault (Free Samples)",
        "description": "110+ proven prompts for Shopify store owners (Free Samples).",
        "price": 0,
        "is_free": True,
        "cover": "cover.jpg"  # ഫ്രീ സാമ്പിളിന് നിലവിലുള്ള കവർ
    },
    "ai_prompt_vault": {
        "title": "🔥 Ecommerce AI Prompt Vault",
        "description": "110+ high-converting prompts for Shopify store owners (PDF).",
        "price": 850,
        "is_free": False,
        "file_path": "The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners.pdf",
        "cover": "Ecommerce AI Prompt Vault.jpg"  # ഗിറ്റ്‌ഹബ്ബിലുള്ള കൃത്യമായ പേര്
    },
    "notion_system": {
        "title": "📊 Notion Business System",
        "description": "Centralized Notion workspace templates and operational dashboards.",
        "price": 600,
        "is_free": False,
        "file_path": "notion-links.txt",
        "cover": "Notion System.jpg"  # ഗിറ്റ്‌ഹബ്ബിലുള്ള കൃത്യമായ പേര്
    },
    "shopify_playbook": {
        "title": "🚀 Shopify Scale Playbook",
        "description": "Complete 5-Module E-Commerce Growth System.",
        "price": 1000,
        "is_free": False,
        "file_path": "Shopify_Scale_Playbook_Final.pdf",
        "cover": "Shopify Scale Playbook.jpg"  # ഗിറ്റ്‌ഹബ്ബിലുള്ള കൃത്യമായ പേര്
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

# മെയിൻ മെനു കീബോർഡ് (5 ഓപ്ഷനുകൾ - Project 0 എന്ന വാക്ക് ഒഴിവാക്കിയിരിക്കുന്നു)
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁 Free AI Prompts", callback_data="select_free_entry")],
        [InlineKeyboardButton("🎁 The Ultimate E-commerce ChatGPT Prompt Vault", callback_data="select_project_0")],
        [InlineKeyboardButton(f"⭐ {PRODUCTS['ai_prompt_vault']['title']} - {PRODUCTS['ai_prompt_vault']['price']} Stars", callback_data="select_ai_prompt_vault")],
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

    if data == "select_free_entry" or data == "select_project_0":
        # കവർ ഫോട്ടോ അയക്കുന്നു
        cover_file = PRODUCTS["project_0"]["cover"]
        if os.path.exists(cover_file):
            try:
                with open(cover_file, 'rb') as photo_file:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file,
                        caption="📦 **The Ultimate E-commerce ChatGPT Prompt Vault (Free Samples)**"
                    )
            except Exception as e:
                logging.error(f"Failed to send cover image: {e}")

        free_text = (
            "🎁 **Free AI Prompts Samples**\n"
            "*(From The Ultimate E-commerce ChatGPT Prompt Vault for Shopify Owners)*\n\n"
            "**1. Product Description Prompt:**\n"
            "`Act as an expert copywriter. Write a high-converting product description for [Product Name] focusing on benefits and emotional triggers.`\n\n"
            "**2. Instagram/TikTok Ad Hook Prompt:**\n"
            "`Generate 5 viral hook lines for a Shopify store selling [Product Niche] that stops users from scrolling instantly.`\n\n"
            "💡 *Want to unlock all 110+ proven prompts? Get the full vault below!* 🔥"
        )
        
        # ഫ്രീ പ്രൊംപ്റ്റിനകത്ത് ഫുൾ വാൾട്ട് വാങ്ങാനുള്ള ബട്ടണും മെയിൻ മെനുവും വെക്കുന്നു
        free_keyboard = [
            [InlineKeyboardButton(f"⭐ Unlock Full Prompt Vault - {PRODUCTS['ai_prompt_vault']['price']} Stars", callback_data="select_ai_prompt_vault")],
            [InlineKeyboardButton("🎁 Free AI Prompts", callback_data="select_free_entry")],
            [InlineKeyboardButton("🎁 The Ultimate E-commerce ChatGPT Prompt Vault", callback_data="select_project_0")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['ai_prompt_vault']['title']} - {PRODUCTS['ai_prompt_vault']['price']} Stars", callback_data="select_ai_prompt_vault")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['notion_system']['title']} - {PRODUCTS['notion_system']['price']} Stars", callback_data="select_notion_system")],
            [InlineKeyboardButton(f"⭐ {PRODUCTS['shopify_playbook']['title']} - {PRODUCTS['shopify_playbook']['price']} Stars", callback_data="select_shopify_playbook")]
        ]
        
        await query.message.reply_text(free_text, reply_markup=InlineKeyboardMarkup(free_keyboard), parse_mode="Markdown")

    elif data.startswith("select_") and data != "select_free_entry":
        prod_key = data.replace("select_", "")
        prod = PRODUCTS.get(prod_key)
        
        if not prod:
            return

        # പെയ്ഡ് പ്രൊഡക്റ്റുകളുടെ കവർ ഫോട്ടോ അയക്കുന്നു (ഫയൽ ഉണ്ടോയെന്ന് ചെക്ക് ചെയ്യുന്നു)
        cover_file = prod.get('cover')
        if cover_file and os.path.exists(cover_file):
            try:
                with open(cover_file, 'rb') as photo_file:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo_file,
                        caption=f"📦 **{prod['title']}**\nPreview Cover"
                    )
            except Exception as e:
                logging.error(f"Failed to send cover image {cover_file}: {e}")
        else:
            logging.warning(f"Cover image not found on server: {cover_file}")

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
