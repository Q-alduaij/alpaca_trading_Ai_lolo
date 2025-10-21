import pandas as pd
from alpaca.data.timeframe import TimeFrame
from src.adapters.alpaca_data import get_bars
from src.utils.indicators import ema, sma, rsi, atr
from src.models import TechnicalSummary

def _trend_from_ma(price: float, ema50: float, sma200: float) -> str:
    if price > ema50 > sma200: return "up"
    if price < ema50 < sma200: return "down"
    return "sideways"

def compute_technical_summary(symbol: str) -> TechnicalSummary:
    m15 = get_bars(symbol, TimeFrame.Minute, lookback_days=5)
    h4  = get_bars(symbol, TimeFrame.Hour,   lookback_days=30)
    d1  = get_bars(symbol, TimeFrame.Day,    lookback_days=365)

    # Resample to H4 from Hour (simple approach if H4 not directly available)
    h4_df = h4.copy()

    # indicators
    h4_df["ema50"] = ema(h4_df["close"], 50)
    h4_df["sma200"] = sma(h4_df["close"], 200)
    h4_df["rsi"] = rsi(h4_df["close"], 14)
    h4_df["atr"] = atr(h4_df.rename(columns={"timestamp":"ts"}).set_index("timestamp").rename_axis(None).reset_index().rename(columns={"index":"timestamp"}), 14)

    d1_df = d1.copy()
    d1_df["ema50"] = ema(d1_df["close"], 50)
    d1_df["sma200"] = sma(d1_df["close"], 200)

    last_h4 = h4_df.iloc[-1]
    last_d1 = d1_df.iloc[-1]
    last_m15 = m15.iloc[-1]

    key_levels = [h4_df["close"].tail(100).max(), h4_df["close"].tail(100).min()]

    trend = _trend_from_ma(last_h4["close"], last_h4["ema50"], last_h4["sma200"])
    return TechnicalSummary(
        symbol=symbol,
        ema50_h4=float(last_h4["ema50"]), sma200_h4=float(last_h4["sma200"]),
        ema50_d1=float(last_d1["ema50"]), sma200_d1=float(last_d1["sma200"]),
        rsi_m15=float(rsi(m15["close"], 14).iloc[-1]),
        rsi_h4=float(last_h4["rsi"]),
        atr_h4=float(last_h4["atr"]),
        key_levels=[float(k) for k in key_levels],
        trend=trend,
        notes="Auto-computed ema/sma/rsi/atr and simple key levels"
    )
