import pytest
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from app.extract.base import Candle
from app.transform.indicators import calculate_indicators, candles_to_dataframe

def make_candle(day: int, close: Decimal) -> Candle:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=day)
    return Candle(
        symbol="BTC-USDT",
        timestamp=timestamp,
        open=close,
        high=close,
        low=close,
        close=close,
        volume=Decimal("100"),
    )

def test_candles_to_dataframe_sorts_by_timestamp():
    candles = [
        make_candle(2, Decimal("120")),
        make_candle(0, Decimal("100")),
        make_candle(1, Decimal("110")),
    ]
    df = candles_to_dataframe(candles)
    assert list(df["close"]) == [100.0, 110.0, 120.0]

def test_calculate_indicators_adds_expected_columns():
    candles = [
        make_candle(day, Decimal(str(100 + day)))
        for day in range(40)
    ]
    df = candles_to_dataframe(candles)
    result = calculate_indicators(df)
    assert "daily_return" in result.columns
    assert "ma7" in result.columns
    assert "ma30" in result.columns
    assert "ema20" in result.columns
    assert "volatility" in result.columns

def test_calculate_daily_return():
    candles = [
        make_candle(0, Decimal("100")),
        make_candle(1, Decimal("110")),
    ]
    df = candles_to_dataframe(candles)
    result = calculate_indicators(df)
    assert result["daily_return"].iloc[1] == pytest.approx(0.1)