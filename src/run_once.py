import asyncio
from datetime import datetime, timezone
from src.logging_setup import configure_logging
from src.models import PortfolioState
from src.orchestrator import run_once

if __name__ == "__main__":
    configure_logging()
    # Dummy portfolio snapshot (replace with live query from Alpaca account + positions)
    snapshot = PortfolioState(
        timestamp=datetime.now(timezone.utc),
        cash=100000.0,
        equity=100000.0,
        positions={},  # fill with your own sector metadata for exposure checks
        daily_drawdown_pct=0.0,
        max_drawdown_pct=0.0
    )
    asyncio.run(run_once("AAPL", "Breaking: Apple announces new device with strong demand signal.", snapshot))
