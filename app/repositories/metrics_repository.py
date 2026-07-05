from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.db.models import DailyMetric


class MetricRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_metrics(self, asset_id: int, metrics_rows: list[dict]) -> int:
        if not metrics_rows:
            return 0
        rows = []
        for row in metrics_rows:
            rows.append(
                {
                    "asset_id": asset_id,
                    "timestamp": row["timestamp"],
                    "daily_return": self._to_decimal(row.get("daily_return")),
                    "ma7": self._to_decimal(row.get("ma7")),
                    "ma30": self._to_decimal(row.get("ma30")),
                    "ema20": self._to_decimal(row.get("ema20")),
                    "volatility": self._to_decimal(row.get("volatility")),
                }
            )
        stmt = insert(DailyMetric).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["asset_id", "timestamp"],
            set_={
                "daily_return": stmt.excluded.daily_return,
                "ma7": stmt.excluded.ma7,
                "ma30": stmt.excluded.ma30,
                "ema20": stmt.excluded.ema20,
                "volatility": stmt.excluded.volatility,
            },
        )
        result = self.db.execute(stmt)
        return result.rowcount or 0

    @staticmethod
    def _to_decimal(value: float | None) -> Decimal | None:
        if value is None:
            return None
        if value != value:
            return None
        return Decimal(str(value))
