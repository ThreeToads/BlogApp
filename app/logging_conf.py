"""Конфигурация логирования приложения с поддержкой ротации логов."""
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.getenv('APP_LOG_DIR', '/app/logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, 'app.log')

logger = logging.getLogger('blog_app')
logger.setLevel(logging.INFO)

# file handler (rotating)
file_handler = RotatingFileHandler(
    LOG_PATH,
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'),
)
logger.addHandler(file_handler)

# also log to stdout for docker
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'),
)
logger.addHandler(stream_handler)
