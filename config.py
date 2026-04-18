import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "http://books.toscrape.com"
    BOOKS_PAGE = "http://books.toscrape.com/catalogue"
    SELECTORS = {
        "book_container": "article.product_pod",
        "title": "h3 a",
        "price": "p.price_color",
        "rating": "p.star-rating",
        "availability": "p.instock.availability"
    }
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data")
    CSV_FILE = os.path.join(OUTPUT_DIR, "books.csv")
    JSON_FILE = os.path.join(OUTPUT_DIR, "books.json")

    # ============ SCRAPING BEHAVIOR ============
    REQUEST_TIMEOUT = 10  # seconds
    DELAY_BETWEEN_REQUESTS = 1  # seconds (be respectful to the server)
    MAX_PAGES = 5  # limit for testing; remove or increase for full scrape

    # ============ LOGGING ============
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FOLDER = os.getenv("LOG_FOLDER", "logs")

    @classmethod
    def validate(cls,required=None):
        """Check all required configs are present"""
        if required is None:
            required = ["BASE_URL","SELECTORS",]
        missing = [key for key in required if not getattr(cls, key,None)]
        if missing:
            raise ValueError(f"Missing required config: {missing}")
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.LOG_FOLDER, exist_ok=True)