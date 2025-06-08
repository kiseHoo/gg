from flask import Flask, request, abort
from pyrogram import Client
import asyncio

BOT_TOKEN = "7088553190:AAHqVkG6b0Cv093Tl-jHtbFYOnRg57euRj0"
API_ID = 14050586  # Replace with your actual API ID
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"  # Replace with your actual API HASH
CHANNEL_USERNAME = "@bot_backup"
MESSAGE_ID = 7

app = Flask(__name__)

# Create Pyrogram Client
pyro = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            try:
                await pyro.forward_messages(
                    chat_id=chat_id,
                    from_chat_id=CHANNEL_USERNAME,
                    message_ids=MESSAGE_ID
                )
            except Exception as e:
                print("Forward failed:", e)

        return "OK"
    else:
        abort(403)

if __name__ == "__main__":
    async def start():
        await pyro.start()
        app.run(host="0.0.0.0", port=8080)

    asyncio.run(start())
