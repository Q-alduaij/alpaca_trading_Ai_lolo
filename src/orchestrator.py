import logging, asyncio
from datetime import datetime, timezone
from alpaca.data.timeframe import TimeFrame
from src.logging_setup import configure_logging
from src.adapters.alpaca_data import get_bars
from src.models import PortfolioState
from src.agents.data_analyst import analyze_news
from src.agents.technical_analyst import compute_technical_summary
from src.agents.strategist import propose_trade
from src.agents.risk_manager import risk_checks_and_size
from src.agents.execution_agent import execute_order

logger = logging.getLogger(__name__)

async def run_once(symbol: str, news_text: str, portfolio_snapshot: PortfolioState):
    # 1) Ingest + analysis in parallel
    news_task = asyncio.create_task(analyze_news(news_text))
    tech_summary = compute_technical_summary(symbol)
    news_insight = await news_task

    # 2) Strategist
    proposal = await propose_trade(news_insight, tech_summary)
    logger.info("COT: %s", proposal.cot_justification)  # per your spec, we log CoT. :contentReference[oaicite:12]{index=12}

    # 3) Get last price
    df = get_bars(symbol, TimeFrame.Minute, lookback_days=2)
    last_price = float(df["close"].iloc[-1])

    # TODO: compute sector_exposure & major_event flags from your own data sources
    sector_exposure_pct = 0.0
    major_event_within_60m = False

    # 4) Risk manager
    approved = risk_checks_and_size(
        portfolio=portfolio_snapshot,
        tech=tech_summary,
        proposal=proposal,
        last_price=last_price,
        sector_exposure_pct=sector_exposure_pct,
        major_event_within_60m=major_event_within_60m
    )
    if not approved:
        logger.info("Trade rejected by risk checks.")
        return

    # 5) Execution
    result = execute_order(approved)
    logger.info("Order submitted: %s", result)
