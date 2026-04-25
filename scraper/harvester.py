import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class BookHarvester:
    """Scrapes book data from books.toscrape.com"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a single page"""
        try:
            logger.debug(f"Fetching {url}")
            response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            logger.info(f"Successfully fetched {url}")
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def extract_book_data(self, book_element) -> Dict[str, str]:
        """Extract data from a single book container"""
        try:
            title_tag = book_element.select_one(Config.SELECTORS["title"])
            price_tag = book_element.select_one(Config.SELECTORS["price"])
            rating_tag = book_element.select_one(Config.SELECTORS["rating"])
            availability_tag = book_element.select_one(Config.SELECTORS["availability"])

            return {
                "title": title_tag.get("title", "").strip() if title_tag else "",
                "price": price_tag.text.strip() if price_tag else "",
                "rating": rating_tag.get("class", [])[-1] if rating_tag else "",
                "availability": (
                    availability_tag.text.strip() if availability_tag else ""
                ),
            }
        except Exception as e:
            logger.warning(f"Error extracting book data: {e}")
            return {}

    def scrape_page(self, page_num: int = 1) -> List[Dict[str, str]]:
        """Scrape all books from a single page"""
        # if page_num == 1:
        url = f"{Config.BOOKS_PAGE}/page-{page_num}.html"

        soup = self.fetch_page(url)
        book_containers = soup.select(Config.SELECTORS["book_container"])

        logger.info(f"Found {len(book_containers)} books on page {page_num}")

        books = []
        for container in book_containers:
            book_data = self.extract_book_data(container)
            if book_data:
                books.append(book_data)

        return books

    def scrape_all(self, max_pages: int = None) -> List[Dict[str, str]]:
        """Scrape multiple pages"""
        if max_pages is None:
            max_pages = Config.MAX_PAGES

        all_books = []

        for page_num in range(1, max_pages + 1):
            logger.info(f"Scraping page {page_num}/{max_pages}")

            try:
                books = self.scrape_page(page_num)
                all_books.extend(books)

                if page_num < max_pages:
                    time.sleep(Config.DELAY_BETWEEN_REQUESTS)

            except Exception as e:
                logger.error(f"Error on page {page_num}: {e}")
                break

        logger.info(f"Total books scraped: {len(all_books)}")
        return all_books
