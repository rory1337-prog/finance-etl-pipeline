import pandas as pd
from sqlalchemy.orm import Session
from app.extract.base import MarketDataProvider
from app.repositories.asset_repository import AssetRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.metrics_repository import MetricRepository
from app.transform.indicators import calculate_indicators

class ETLService:
    def __init__(self, db: Session, provider: MarketDataProvider) -> None:
        self.db = db
        self.provider = provider
        self.assets = AssetRepository(db)
        self.prices = PriceRepository(db)
        self.metrics = MetricRepository(db)

    def load_market_data(self, symbol: str, name: str, interval: str = "1d", limit: int = 365) -> int:
        asset = self.assets.get_or_create(symbol=symbol, name=name)
        candles = self.provider.get_klines(symbol=symbol, interval=interval, limit=limit)
        rows_inserted = self.prices.upsert_candles(asset_id=asset.id, candles=candles)
        self.db.commit()

        return rows_inserted
    
    def calculate_and_save_metrics(self, symbol: str) -> int:
        asset = self.assets.get_by_symbol(symbol)
        if asset is None:
            raise ValueError(f"Asset not found: {symbol}")
        prices = self.prices.get_by_asset_id(asset.id)
        df = pd.DataFrame(
            {
                "timestamp": [p.timestamp for p in prices],
                "close": [float(p.close) for p in prices],
                "high": [float(p.high) for p in prices],
                "low": [float(p.low) for p in prices],
                "volume": [float(p.volume) for p in prices],
            }
        )
        df = df.sort_values("timestamp")
        df = df.set_index("timestamp")
        result = calculate_indicators(df)
        metrics_rows = []
        for timestamp, row in result.iterrows():
            metrics_rows.append(
                {
                    "timestamp": timestamp,
                    "daily_return": row.get("daily_return"),
                    "ma7": row.get("ma7"),
                    "ma30": row.get("ma30"),
                    "ema20": row.get("ema20"),
                    "volatility": row.get("volatility"),
                }
            )
        rows_upserted = self.metrics.upsert_metrics(
            asset_id=asset.id,
            metrics_rows=metrics_rows,
        )
        self.db.commit()
        return rows_upserted