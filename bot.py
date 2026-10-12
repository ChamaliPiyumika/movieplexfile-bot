import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render වෙනුවෙන් Port එක Open කර තබන Web Server එක
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"MoviePlex Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Bot Token
BOT_TOKEN = "8845160703:AAGkTLzifU6rrNCSB9UxrAbF12v8uuzn76M"

# Movie Database
MOVIES_DATABASE = {
    "movie_1": "BAACAgUAAxkBAAEvpXRqy75NXLGOfbyMOzzCWhxWsXc4gACtYIAAhLrUFZuE9y127JIUz0E",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        movie_key = context.args[0]
        if movie_key in MOVIES_DATABASE:
            file_id = MOVIES_DATABASE[movie_key]
            await update.message.reply_video(video=file_id, caption="Here is your movie! 🎬")
        else:
            await update.message.reply_text("Movie not found.")
    else:
        await update.message.reply_text("Welcome to MoviePlex Bot!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Python 3.14 සමඟ ගැළපෙන ලෙස polling ආරම්භ කිරීම
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Bot එක අඛණ්ඩව ක්‍රියාත්මක වීමට තබා ගැනීම
    stop_event = asyncio.Event()
    await stop_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
