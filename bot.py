import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import load_config
from handlers import start, caps, echo, unknown, generate_and_send_image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    cfg = load_config()
    application = ApplicationBuilder().token(cfg["telegram_bot_token"]).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(CommandHandler('image', generate_and_send_image))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()

if __name__ == '__main__':
    main()
