import logging
import os
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
log_folder = os.getenv("LOG_FOLDER", "logs")

os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(log_folder, "harvester.log")

logging.basicConfig(
    level=log_level,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
