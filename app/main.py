from app.config import settings
from app.db.session import SessionLocal
from app.extract.bingx import BingXProvider
from app.services.etl_service import ETLService

def main() -> None:
    provider = BingXProvider()
    with SessionLocal() as db:
        service = ETLService(db=db, provider=provider)
        rows_inserted = service.load_market_data(symbol="BTC-USDT", name="Bitcoin / Tether", interval=settings.default_interval, limit=settings.default_limit)
    print(f"Loaded {rows_inserted} new candles")

if __name__ == "__main__":
    main()