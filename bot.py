import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render එක වෙනුවෙන් Port එක Open කර තබන Dummy Web Server එක
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

# Bot Token එක මෙතැනට දෙන්න
BOT_TOKEN = "8845160703:AAHhVwnVxt_0rT4zGWvMDVdcZVFDoJ67cmE"

# නිවැරදි කරගත් File ID එක මෙතැනට දෙන්න
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

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
