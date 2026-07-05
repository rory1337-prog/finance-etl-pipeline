from sqlalchemy import select

from app.db.models import DailyMetric
from app.db.session import SessionLocal


def main():
    with SessionLocal() as db:
        rows = db.scalars(
            select(DailyMetric)
            .order_by(DailyMetric.timestamp.desc())
            .limit(5)
        ).all()

        for row in rows:
            print(
                row.timestamp,
                row.daily_return,
                row.ma7,
                row.ma30,
                row.ema20,
                row.volatility,
            )


if __name__ == "__main__":
    main()