import re
from utils.logger import get_logger

logger = get_logger(__name__)

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def clean_price(raw_price: str) -> float:
    try:
        cleaned = re.sub(r"[^\d.]", "", raw_price)
        return float(cleaned)
    except (ValueError, TypeError) as e:
        logger.warning(f"Could not clean price: {raw_price!r}-{e}")
        return 0.0


def clean_rating(raw_rating: str) -> int:
    try:
        return RATING_MAP.get(raw_rating.strip(), 0)
    except AttributeError as e:
        logger.warning(f"Could not clean rating: {raw_rating!r}-{e}")
        return 0


def clean_availability(raw_availability: str) -> bool:
    try:
        return "in stock" in raw_availability.strip().lower()
    except AttributeError as e:
        logger.warning(f"Could not clean availability: {raw_availability!r}-{e}")
        return False


def clean_title(raw_title: str) -> str:
    try:
        return raw_title.strip()
    except AttributeError as e:
        logger.warning(f"could not clean title: {raw_title!r}-{e}")
        return ""


def clean_book(raw_book: dict) -> dict:
    return {
        "title": clean_title(raw_book.get("title", "")),
        "price": clean_price(raw_book.get("price", "")),
        "rating": clean_rating(raw_book.get("rating", "")),
        "available": clean_availability(raw_book.get("availability", "")),
    }


def clean_books(raw_books: list) -> list:
    cleaned = []
    for book in raw_books:
        try:
            cleaned.append(clean_book(book))
        except Exception as e:
            logger.error(f"skipping book due to unexpected error: {e}")
    logger.info(f"cleaned {len(cleaned)} of {len(raw_books)} books successfully")
    return cleaned
