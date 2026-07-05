from datetime import UTC, datetime
from decimal import Decimal
import requests
from app.config import settings
from app.extract.base import Candle, MarketDataProvider

class BingXProvider(MarketDataProvider):
    def __init__(self) -> None:
        self.base_url = settings.bingx_base_url

    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 365) -> list[Candle]:
        url = f"{self.base_url}/openApi/swap/v3/quote/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise RuntimeError(f"BingX API error: {payload}")
        candles: list[Candle] = []
        for item in payload.get("data", []):
            candles.append(
                Candle(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(
                        int(item["time"]) / 1000,
                        tz=UTC,
                    ),
                    open=Decimal(str(item["open"])),
                    high=Decimal(str(item["high"])),
                    low=Decimal(str(item["low"])),
                    close=Decimal(str(item["close"])),
                    volume=Decimal(str(item["volume"])),
                )
            )
        return candles