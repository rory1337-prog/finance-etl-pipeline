from app.config import settings
from app.db.session import SessionLocal
from app.extract.bingx import BingXProvider
from app.services.etl_service import ETLService
from app.constants import TRACKED_ASSETS

def main() -> None:
    provider = BingXProvider()
    with SessionLocal() as db:
        service = ETLService(db=db, provider=provider)
        run = service.etl_runs.start()
        try:
            total_candles = 0
            total_metrics = 0
            for asset in TRACKED_ASSETS:
                rows = service.load_market_data(
                    symbol=asset["symbol"],
                    name=asset["name"],
                    interval=settings.default_interval,
                    limit=settings.default_limit,
                )
                metrics = service.calculate_and_save_metrics(asset["symbol"])
                total_candles += rows
                total_metrics += metrics
                print(
                    f"{asset['symbol']}: "
                    f"candles={rows}, metrics={metrics}"
                )
            service.etl_runs.finish(run, total_candles + total_metrics)
            print(f"Total candles: {total_candles}")
            print(f"Total metrics: {total_metrics}")
        except Exception as exc:
            service.etl_runs.fail(run, exc)
            db.commit()
            raise


if __name__ == "__main__":
    main()