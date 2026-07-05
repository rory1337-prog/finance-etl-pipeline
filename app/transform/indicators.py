import pandas as pd
from app.constants import EMA_WINDOWS, MA_WINDOWS, VOLATILITY_WINDOW
from app.extract.base import Candle


def candles_to_dataframe(candles: list[Candle]) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "timestamp": [c.timestamp for c in candles],
            "close": [float(c.close) for c in candles],
            "high": [float(c.high) for c in candles],
            "low": [float(c.low) for c in candles],
            "volume": [float(c.volume) for c in candles],
        }
    )
    df = df.sort_values("timestamp")
    df = df.set_index("timestamp")
    return df


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    # Daily return
    result["daily_return"] = result["close"].pct_change()
    # Moving averages
    for window in MA_WINDOWS:
        result[f"ma{window}"] = result["close"].rolling(window=window).mean()
    # Exponential moving averages
    for span in EMA_WINDOWS:
        result[f"ema{span}"] = result["close"].ewm(span=span, adjust=False).mean()
    # Volatility
    result["volatility"] = (
        result["close"].pct_change().rolling(window=VOLATILITY_WINDOW).std()
    )
    return result
