# src/adapters/alpaca_exec.py
from alpaca.trading.client import TradingClient
from alpaca.common.types import BaseURL
from src.config import SETTINGS

trading = TradingClient(
    api_key=SETTINGS.alpaca_api_key_id,
    secret_key=SETTINGS.alpaca_api_secret_key,
    paper=True,
    url_override=BaseURL(SETTINGS.alpaca_paper_base_url)
)
