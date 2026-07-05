from app.config import settings
from app.extract.bingx import BingXProvider

def main() -> None:
    provider = BingXProvider()
    candles = provider.get_klines(
        symbol="BTC-USDT",
        interval=settings.default_interval,
        limit=5,
    )
    print(f"Downloaded {len(candles)} candles")

    for candle in candles:
        print(candle)
if __name__ == "__main__":
    main()