import os
import asyncio
from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@bot_backup"
MESSAGE_ID = 7

bot_app = Application.builder().token(BOT_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_USERNAME,
            message_id=MESSAGE_ID
        )
    except Exception:
        await update.message.reply_text("⚠️ Forwarding failed.")

bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        asyncio.run(bot_app.update_queue.put(update))
        return "OK"
    else:
        abort(403)

if __name__ == "__main__":
    asyncio.run(bot_app.initialize())
    asyncio.run(bot_app.start())
    # Flask server running on port 8080
    app.run(host="0.0.0.0", port=8080)
