from datetime import datetime, UTC
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), nullable=False, index=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    daily_return: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    ma7: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    ma30: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    ema20: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    rsi14: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    atr14: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    volatility: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    asset = relationship("Asset", back_populates="metrics")

    __table_args__ = (
        UniqueConstraint(
            "asset_id",
            "timestamp",
            name="uq_daily_metrics_asset_timestamp",
        ),
    )
