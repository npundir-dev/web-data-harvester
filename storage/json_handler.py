import json
import os
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


def save_to_json(
    books: list, filepath: str = Config.JSON_FILE, append: bool = False
) -> None:
    if not books:
        logger.warning("No books to save - JSON write skipped")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if append and os.path.exists(filepath):
        existing = load_from_json(filepath)
        books = existing + books

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(books, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(books)} books to {filepath}")
    except OSError as e:
        logger.error(f"Failed to write JSON: {e}")
        raise


def load_from_json(filepath: str = Config.JSON_FILE) -> list:
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} books from {filepath}")
        return data
    except FileNotFoundError:
        logger.warning(f"JSON file not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return []
