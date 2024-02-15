import os

from loguru import logger

from settings import settings

LOGS_FOLDER = os.path.join(os.path.dirname(__file__), "logs")

os.makedirs(LOGS_FOLDER, exist_ok=True)

logger.add(
    sink=os.path.join(LOGS_FOLDER, "{time:DD-MM-YYYY}.log"),
    rotation="00:00",
    format="{time:HH:mm:ss DD-MM-YYYY} | {level: <8} | {message}",
    backtrace=False,
    level=settings.LOG_LEVEL,
)
