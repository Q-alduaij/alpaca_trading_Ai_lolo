from typing import Optional
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopLossRequest, TakeProfitRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from src.adapters.alpaca_exec import trading
from src.models import ApprovedOrder

def execute_order(order: ApprovedOrder):
    side_enum = OrderSide.BUY if order.side == "buy" else OrderSide.SELL

    if order.entry_type == "market":
        req = MarketOrderRequest(
            symbol=order.symbol,
            qty=order.qty,
            side=side_enum,
            time_in_force=TimeInForce.DAY,
            take_profit=TakeProfitRequest(limit_price=order.tp1_price),  # initial TP1; upgrade later
            stop_loss=StopLossRequest(stop_price=order.sl_price)
        )
        result = trading.submit_order(req)
    else:
        req = LimitOrderRequest(
            symbol=order.symbol,
            qty=order.qty,
            side=side_enum,
            limit_price=order.limit_price,
            time_in_force=TimeInForce.DAY,
            take_profit=TakeProfitRequest(limit_price=order.tp1_price),
            stop_loss=StopLossRequest(stop_price=order.sl_price)
        )
        result = trading.submit_order(req)

    # NOTE: After TP1 fill detection, you would:
    # - close 50% and modify remaining position SL to breakeven
    # This requires fill monitoring + OCO management (left as orchestration step).
    return result
