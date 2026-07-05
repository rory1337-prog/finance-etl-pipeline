import argparse
from app.config import settings
from app.constants import TRACKED_ASSETS
from app.db.session import SessionLocal
from app.extract.bingx import BingXProvider
from app.services.etl_service import ETLService

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Finance ETL Pipeline",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true",help="Run ETL for all tracked assets")
    group.add_argument("--asset", type=str,help="Run ETL for a single asset symbol, e.g. BTC-USDT")
    return parser.parse_args()

def get_assets_to_process(args: argparse.Namespace) -> tuple[dict, ...]:
    if args.all:
        return TRACKED_ASSETS
    asset = next(
        (
            item
            for item in TRACKED_ASSETS
            if item["symbol"] == args.asset
        ),
        None,
    )
    if asset is None:
        available = ", ".join(item["symbol"] for item in TRACKED_ASSETS)
        raise ValueError(f"Unknown asset: {args.asset}. Available assets: {available}")
    return (asset,)

def run_etl_for_assets(assets: tuple[dict, ...]) -> None:
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
                print(
                    f"{asset['symbol']}: "
                    f"candles={rows_inserted}, "
                    f"metrics={metrics_saved}"
                )
            service.etl_runs.finish(run, total_candles + total_metrics)
            db.commit()
            print(f"Total candles: {total_candles}")
            print(f"Total metrics: {total_metrics}")
        except Exception as exc:
            service.etl_runs.fail(run, exc)
            db.commit()
            raise

def main() -> None:
    args = parse_args()
    assets = get_assets_to_process(args)
    run_etl_for_assets(assets)


if __name__ == "__main__":
    main()