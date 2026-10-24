import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Fonction pour chercher sur Vinted
def chercher_vinted(mot_cle):
    url = f"https://www.vinted.fr/api/v2/catalog/items?search_text={mot_cle}&per_page=5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            resultats = []
            for item in items[:3]: # On prend les 3 plus récentes
                titre = item.get('title')
                prix = item.get('price')
                url_item = item.get('url')
                resultats.append(f"👟 **{titre}**\n💰 Prix : {prix} €\n🔗 [Voir sur Vinted]({url_item})")
            return "\n\n".join(resultats) if resultats else "Aucun article trouvé."
        else:
            return "Impossible de récupérer les articles Vinted pour le moment."
    except Exception as e:
        return f"Erreur lors de la recherche : {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot Vinted Hunter activé ! Envoie-moi un mot-clé (ex: Nike Air Max, Stussy, Corteiz) pour dénicher les affaires.")

async def gerer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recherche = update.message.text
    await update.message.reply_text(f"🔍 Recherche en cours sur Vinted pour : '{recherche}'...")
    
    # Appel de la fonction Vinted
    resultat = chercher_vinted(recherche)
    await update.message.reply_text(resultat, parse_mode='Markdown', disable_web_page_preview=False)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerer_message))
    app.run_polling()
