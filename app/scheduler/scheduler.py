import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from app.constants import TRACKED_ASSETS
from app.pipeline.runner import execute_pipeline

logger = logging.getLogger(__name__)
def run_scheduled_etl() -> None:
    execute_pipeline(TRACKED_ASSETS)


def main() -> None:
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(
        run_scheduled_etl,
        trigger="cron",
        hour=0,
        minute=0,
        id="daily_finance_etl",
        replace_existing=True,
    )
    logger.info("Starting ETL scheduler")
    scheduler.start()


if __name__ == "__main__":
    main()
