import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# توکنەکەت لێرە دابنێ
TOKEN = "8933985744:AAETq8QY3O1RkvHYJSz_Gx27cKWKBfvB29I"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! من بوتێکی داونلۆدەرم، تەنها لینکێکم بۆ بنێرە.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return

    status = await update.message.reply_text("خەریکە ڤیدیۆکە ئامادە دەکەم... ⏳")
    
    output_file = f"video_{update.effective_user.id}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await update.message.reply_video(video=open(output_file, 'rb'), caption="فەرموو ✨")
        await status.delete()
        os.remove(output_file)
    except Exception as e:
        await update.message.reply_text(f"کێشەیەک هەبوو: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
