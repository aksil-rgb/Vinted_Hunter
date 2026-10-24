import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salut ! Je suis ton assistant Vinted en ligne. Dis-moi ce que tu cherches !")

async def gerer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recherche = update.message.text
    await update.message.reply_text(f"🔍 Recherche reçue : '{recherche}'. Bientôt connectée à Vinted !")

if __name__ == '__main__':
    print("Le bot démarre...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerer_message))
    app.run_polling()
