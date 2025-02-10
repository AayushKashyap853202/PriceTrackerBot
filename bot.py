from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

TOKEN = "7730076837:AAGQ7p1JughcZwFEOQGSzpU4dxAc4vmROAk"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Mujhe kisi bhi product ka link bhejo, main uska price track karunga!")

def track_price(update: Update, context: CallbackContext):
    url = update.message.text
    price = get_price(url)
    if price:
        update.message.reply_text(f"🔹 Current Price: ₹{price}")
    else:
        update.message.reply_text("❌ Price fetch nahi ho raha hai!")

def get_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Amazon ke liye price extract karna
    price_tag = soup.find("span", {"class": "a-price-whole"})
    if price_tag:
        return price_tag.text.strip()
    return None

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("track", track_price))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
