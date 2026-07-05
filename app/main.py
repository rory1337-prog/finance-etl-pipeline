import argparse
from app.logging_config import setup_logging
from app.constants import TRACKED_ASSETS
from app.pipeline.runner import execute_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finance ETL Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--asset", type=str)
    return parser.parse_args()


def get_assets_to_process(args: argparse.Namespace) -> tuple[dict, ...]:
    if args.all:
        return TRACKED_ASSETS
    asset = next(
        (item for item in TRACKED_ASSETS if item["symbol"] == args.asset),
        None,
    )
    if asset is None:
        available = ", ".join(item["symbol"] for item in TRACKED_ASSETS)
        raise ValueError(f"Unknown asset: {args.asset}. Available: {available}")
    return (asset,)


def main() -> None:
    setup_logging()
    args = parse_args()
    assets = get_assets_to_process(args)
    execute_pipeline(assets)


if __name__ == "__main__":
    main()
