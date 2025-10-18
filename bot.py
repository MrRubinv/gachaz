import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext


def get_webapp_url() -> str:
    # Use Railway production URL
    return os.environ.get("WEBAPP_URL", "https://gachaz-production.up.railway.app/")


async def start(update: Update, context: CallbackContext) -> None:
    webapp_url = get_webapp_url()
    keyboard = [
        [InlineKeyboardButton(text="Open Pull Simulator", web_app=WebAppInfo(url=webapp_url))]
    ]
    await update.message.reply_text(
        "Welcome! Tap to open the WebApp:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def help_cmd(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Use /start to open the WebApp.")


def main() -> None:
    load_dotenv()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not set. Put it in .env or environment.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    app.run_polling(allowed_updates=["message", "callback_query"]) 


if __name__ == "__main__":
    main()


