import csv
import os
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

FIELDNAMES = ["title", "price", "rating", "available"]


def save_to_csv(books: list, filepath: str = Config.CSV_FILE, append: bool = False):
    if not books:
        logger.warning("No books to save- CSV write skipped")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    mode = "a" if append else "w"
    write_header = not append or not os.path.exists(filepath)

    try:
        with open(filepath, mode=mode, newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerows(books)
        logger.info(f"Saved {len(books)} books to {filepath}")
    except OSError as e:
        logger.error(f"Failed to write CSV :{e}")
        raise
