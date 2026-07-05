import logging
from app.config import settings
from app.db.session import SessionLocal
from app.extract.bingx import BingXProvider
from app.services.etl_service import ETLService

logger = logging.getLogger(__name__)

def execute_pipeline(assets: tuple[dict, ...]) -> None:
    logger.info("Finance ETL pipeline started")
    provider = BingXProvider()
    with SessionLocal() as db:
        service = ETLService(db=db, provider=provider)
        run = service.etl_runs.start()
        total_candles = 0
        total_metrics = 0
        try:
            for asset in assets:
                rows_inserted = service.load_market_data(
                    symbol=asset["symbol"],
                    name=asset["name"],
                    interval=settings.default_interval,
                    limit=settings.default_limit,
                )
                metrics_saved = service.calculate_and_save_metrics(asset["symbol"])
                total_candles += rows_inserted
                total_metrics += metrics_saved
                logger.info(
                    "%s | candles=%s | metrics=%s",
                    asset["symbol"],
                    rows_inserted,
                    metrics_saved,
                )
            service.etl_runs.finish(run, total_candles + total_metrics)
            db.commit()
            logger.info(
                "Finance ETL pipeline finished successfully | candles=%s | metrics=%s",
                total_candles,
                total_metrics,
            )
        except Exception as exc:
            logger.exception("Finance ETL pipeline failed")
            service.etl_runs.fail(run, exc)
            db.commit()
            raise
