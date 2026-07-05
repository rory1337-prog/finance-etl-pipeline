from sqlalchemy.orm import Session
from app.extract.base import MarketDataProvider
from app.repositories.asset_repository import AssetRepository
from app.repositories.price_repository import PriceRepository

class ETLService:
    def __init__(self, db: Session, provider: MarketDataProvider) -> None:
        self.db = db
        self.provider = provider
        self.assets = AssetRepository(db)
        self.prices = PriceRepository(db)

    def load_market_data(self, symbol: str, name: str, interval: str = "1d", limit: int = 365) -> int:
        asset = self.assets.get_or_create(symbol=symbol, name=name)
        candles = self.provider.get_klines(symbol=symbol, interval=interval, limit=limit)
        rows_inserted = self.prices.upsert_candles(asset_id=asset.id, candles=candles)
        self.db.commit()

        return rows_inserted
    