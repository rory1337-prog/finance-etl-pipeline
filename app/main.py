from app.config import settings
from app.db.session import SessionLocal
from app.extract.bingx import BingXProvider
from app.services.etl_service import ETLService

def main() -> None:
    provider = BingXProvider()
    with SessionLocal() as db:
        service = ETLService(db=db, provider=provider)
        run = service.etl_runs.start()
        try:
            rows_inserted = service.load_market_data(
                symbol="BTC-USDT",
                name="Bitcoin / Tether",
                interval=settings.default_interval,
                limit=settings.default_limit,
            )
            metrics_saved = service.calculate_and_save_metrics("BTC-USDT")
            service.etl_runs.finish(
                run,
                rows_inserted + metrics_saved,
            )
            db.commit()
            print(f"Loaded {rows_inserted} new candles")
            print(f"Saved {metrics_saved} metric rows")
        except Exception as exc:
            service.etl_runs.fail(run, exc)
            db.commit()
            raise


if __name__ == "__main__":
    main()