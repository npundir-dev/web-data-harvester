import time
import schedule
from .logger import get_logger

logger = get_logger(__name__)


def schedule_job(job_func, interval_minutes: int = 60) -> None:
    schedule.every(interval_minutes).minutes.do(job_func)
    logger.info(f"Job scheduled to run every {interval_minutes} minute(s)")


def run_scheduler(stop_after: int = None) -> None:
    logger.info("Scheduler started - press ctrl+C to stop")
    start_time = time.time()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)

            if stop_after and (time.time() - start_time) >= stop_after:
                logger.info("Scheduler stopped after time limit")
                break
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")


def clear_jobs() -> None:
    schedule.clear()
    logger.info("All scheduled jobs cleared")
