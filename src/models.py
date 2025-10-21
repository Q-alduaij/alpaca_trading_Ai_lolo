from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class PortfolioState(BaseModel):
    timestamp: datetime
    cash: float
    equity: float
    positions: dict  # {symbol: {"qty": int, "avg_price": float, "sector": Optional[str]} }
    daily_drawdown_pct: float
    max_drawdown_pct: float

class NewsInsight(BaseModel):
    timestamp: datetime
    ticker: str
    sentiment_score: float  # -1..+1
    impact_score: int       # 1..10
    event_type: Optional[str] = None
    summary: str

class TechnicalSummary(BaseModel):
    symbol: str
    ema50_h4: float
    sma200_h4: float
    ema50_d1: float
    sma200_d1: float
    rsi_m15: float
    rsi_h4: float
    atr_h4: float
    key_levels: List[float]
    trend: Literal["up","down","sideways"]
    notes: Optional[str] = None

class TradeProposal(BaseModel):
    symbol: str
    side: Literal["long","short"]
    entry_hint: Optional[float] = None
    sl_hint: Optional[float] = None
    tp1_hint: Optional[float] = None
    tp2_hint: Optional[float] = None
    confidence: int
    scenario: Literal["A","B","C"]
    cot_justification: str  # LLM CoT (your spec requires logging CoT)  # :contentReference[oaicite:2]{index=2}

class ApprovedOrder(BaseModel):
    symbol: str
    side: Literal["buy","sell"]
    qty: int
    entry_type: Literal["limit","market"]
    limit_price: Optional[float]
    sl_price: float
    tp1_price: float
    tp2_price: float
