from loguru import logger
import os, sys

LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> | <level>{level}</level> | {message}")
logger.add(os.path.join(LOG_DIR, "backend.log"), rotation="5 MB", retention="7 days", level="INFO")
