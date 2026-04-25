import sys
from config import Config
from utils.logger import get_logger
from utils.scheduler import schedule_job, run_scheduler, clear_jobs
from scraper.harvester import BookHarvester
from scraper.cleaner import clean_books
from storage.csv_handler import save_to_csv
from storage.json_handler import save_to_json, load_from_json

logger = get_logger(__name__)

def run_scrape() -> None:
    logger.info("Starting scrape cycle")
    
    harvester = BookHarvester()
    raw_books = harvester.scrape_all()

    if not raw_books:
        logger.warning("No books scraped - exiting cycle")
        return
    
    cleaned_books = clean_books(raw_books)
    save_to_csv(cleaned_books)
    save_to_json(cleaned_books)

    logger.info(f"Scrape cycle complete - {len(cleaned_books)} books saved")

def show_menu() -> str:
    print("\n==============================")
    print("   Web Data Harvester CLI")
    print("================================")
    print("1. Scrape now")
    print("2. Schedule scraping")
    print("3. Exit")
    print("================================")
    return input("Enter your choice (1/2/3): ").strip()

def get_schedule_interval() -> int:
    while True:
        try:
            interval = int(input("Run every how many minutes? ").strip())
            if interval < 1:
                print("Please enter a number greater than 0")
                continue
            return interval
        except ValueError:
            print("Invalid input - please enter a whole number")

def main() -> None:
    logger.info("Data Harvester started")

    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    while True:
        choice = show_menu()

        if choice == "1":
            run_scrape()

        elif choice == "2":
            interval = get_schedule_interval()
            schedule_job(run_scrape, interval_minutes=interval)
            run_scheduler()
            clear_jobs()

        elif choice == "3":
            logger.info("Exiting - goodbye!")
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice - please enter 1, 2, or 3")

if __name__ == "__main__":
    main()