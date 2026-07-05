from sqlalchemy.orm import Session
from app.db.models import Asset

class AssetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_symbol(self, symbol: str) -> Asset | None:
        return (
            self.db.query(Asset)
            .filter(Asset.symbol == symbol)
            .one_or_none()
        )
    
    def get_or_create(self, symbol: str, name: str, asset_type: str = "crypto", exchange: str = "BingX", currency: str = "USDT") -> Asset:
        asset = self.get_by_symbol(symbol)
        if asset:
            return asset
        asset = Asset(symbol=symbol, name=name, asset_type=asset_type, exchange=exchange, currency=currency)
        self.db.add(asset)
        self.db.flush()
        return asset
    