from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.db.models import PriceHistory
from app.extract.base import Candle

class PriceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_candles(self, asset_id: int, candles: list[Candle]) -> int:
        if not candles:
            return 0
        rows = [
            {
                "asset_id": asset_id,
                "timestamp": candle.timestamp,
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "volume": candle.volume,
            }
            for candle in candles
        ]
        stmt = insert(PriceHistory).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=["asset_id", "timestamp"])
        result = self.db.execute(stmt)
        return result.rowcount or 0
    
    def get_by_asset_id(self, asset_id: int) -> list[PriceHistory]:
        return (
            self.db.query(PriceHistory)
            .filter(PriceHistory.asset_id == asset_id)
            .order_by(PriceHistory.timestamp.asc())
            .all()
        )