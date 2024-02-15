from telegram.ext import ApplicationBuilder

import handlers
from logger import logger
from settings import settings


def main():
    logger.info("Start bot")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    handlers.add_handlers(application)
    application.run_polling()
    logger.info("Stop bot")


if __name__ == "__main__":
    main()
