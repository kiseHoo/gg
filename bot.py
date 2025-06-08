from flask import Flask, request, abort
from pyrogram import Client
import asyncio

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@bot_backup"
MESSAGE_ID = 7

app = Flask(__name__)

pyro = Client("my_bot", bot_token=BOT_TOKEN)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)
        asyncio.run(process_update(update))
        return "OK"
    else:
        abort(403)

async def process_update(update):
    from pyrogram.types import Update as PyroUpdate
    py_update = PyroUpdate(**update)
    # Pyrogram does not provide direct way to process raw update,
    # so you need to handle message manually here:
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        try:
            await pyro.forward_messages(
                chat_id,
                CHANNEL_USERNAME,
                MESSAGE_ID
            )
        except Exception as e:
            print("Forward failed:", e)

if __name__ == "__main__":
    pyro.start()
    app.run(host="0.0.0.0", port=8080)
