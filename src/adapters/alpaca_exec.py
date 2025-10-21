from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetAssetsRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.common.types import BaseURL
from typing import Optional
from src.config import SETTINGS

trading = TradingClient(
    api_key=SETTINGS.alpaca_api_key_id,
    secret_key=SETTINGS.alpaca_api_secret_key,
    paper=True,
    url_override=BaseURL(SETTINGS.alpaca_paper_base_url)
)

def place_market(symbol: str, qty: int, side: str):
    req = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )
    return trading.submit_order(req)

def place_limit(symbol: str, qty: int, side: str, limit_price: float):
    req = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        limit_price=limit_price,
        time_in_force=TimeInForce.DAY
    )
    return trading.submit_order(req)
