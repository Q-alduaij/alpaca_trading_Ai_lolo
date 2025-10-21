from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.models import BarSet
from alpaca.common.types import BaseURL
from datetime import datetime, timedelta, timezone
import pandas as pd
from typing import List
from src.config import SETTINGS

_client = StockHistoricalDataClient(
    api_key=SETTINGS.alpaca_api_key_id,
    secret_key=SETTINGS.alpaca_api_secret_key
)

def get_bars(symbol: str, timeframe: TimeFrame, lookback_days: int = 60) -> pd.DataFrame:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=lookback_days)
    req = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=timeframe,
        start=start,
        end=end
    )
    bars: BarSet = _client.get_stock_bars(req)
    df = bars.df.reset_index()
    # normalize
    df.rename(columns={"timestamp":"ts"}, inplace=True)
    df = df[df["symbol"]==symbol].sort_values("ts")
    return df[["ts","open","high","low","close","volume"]].rename(columns={"ts":"timestamp"})
