from math import floor
from datetime import datetime, timezone
from src.models import PortfolioState, TechnicalSummary, TradeProposal, ApprovedOrder
from src.config import SETTINGS

def risk_checks_and_size(
    portfolio: PortfolioState,
    tech: TechnicalSummary,
    proposal: TradeProposal,
    last_price: float,
    sector_exposure_pct: float,
    major_event_within_60m: bool
) -> ApprovedOrder | None:
    # Circuit breakers
    if portfolio.daily_drawdown_pct <= -abs(SETTINGS.daily_dd_halt_pct):
        return None
    if portfolio.max_drawdown_pct <= -abs(SETTINGS.total_dd_halt_pct):
        return None

    # Confidence veto
    if proposal.confidence < SETTINGS.confidence_threshold:
        return None

    # Event horizon veto
    if major_event_within_60m:
        return None

    # Sector exposure veto
    if sector_exposure_pct > SETTINGS.max_sector_exposure_pct:
        return None

    # SL: max of structure vs volatility (1.5 * ATR H4)
    if proposal.sl_hint:
        structure_sl = proposal.sl_hint
    else:
        # naive structural SL using key levels
        structure_sl = tech.key_levels[1] if proposal.side == "long" else tech.key_levels[0]

    vol_sl = last_price - 1.5*tech.atr_h4 if proposal.side == "long" else last_price + 1.5*tech.atr_h4
    if proposal.side == "long":
        sl_price = min(structure_sl, vol_sl)
    else:
        sl_price = max(structure_sl, vol_sl)

    # Risk distance
    risk_dist = abs(last_price - sl_price)
    if risk_dist <= 0:
        return None

    # Position sizing by confidence
    if proposal.confidence >= 90:
        max_risk_pct = 0.02
    else:
        max_risk_pct = 0.01

    max_risk_value = portfolio.equity * max_risk_pct
    qty = floor(max_risk_value / risk_dist)
    if qty <= 0:
        return None

    # TP targets (1.5R and 3R)
    if proposal.side == "long":
        tp1 = last_price + 1.5 * risk_dist
        tp2 = last_price + 3.0 * risk_dist
        side = "buy"
    else:
        tp1 = last_price - 1.5 * risk_dist
        tp2 = last_price - 3.0 * risk_dist
        side = "sell"

    entry_type = "market" if proposal.scenario == "A" else "limit"
    limit_price = last_price if entry_type == "limit" else None

    return ApprovedOrder(
        symbol=tech.symbol,
        side=side,
        qty=qty,
        entry_type=entry_type,
        limit_price=limit_price,
        sl_price=sl_price,
        tp1_price=tp1,
        tp2_price=tp2
    )
