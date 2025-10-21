from src.models import NewsInsight, TechnicalSummary, TradeProposal
from src.adapters.llm_client import call_llm

PROMPT = """You are the Strategist. Using the inputs, decide Scenario A/B/C:

Rules summary:
- A: High-impact news (impact>=8 and |sentiment|>=0.7), align with H4/D1; allow override if impact=10 and M15 breakout.
- B: Technical breakout on H4 with supportive news in last 48h; enter on M15 retest.
- C: Mean reversion extremes on H4 RSI (<30 long or >70 short) near key level, only if no recent high-impact contrary news.

Return a JSON with:
scenario, side (long|short), entry_hint, sl_hint, tp1_hint, tp2_hint, confidence, cot
Inputs:
News: {news}
Technical: {tech}
"""

async def propose_trade(news: NewsInsight, tech: TechnicalSummary) -> TradeProposal:
    news_json = news.model_dump()
    tech_json = tech.model_dump()
    res = await call_llm(PROMPT.format(news=news_json, tech=tech_json), agent_role="Strategist")
    obj = __import__("json").loads(res["text"])
    return TradeProposal(
        symbol=tech.symbol,
        side=obj["side"],
        entry_hint=obj.get("entry_hint"),
        sl_hint=obj.get("sl_hint"),
        tp1_hint=obj.get("tp1_hint"),
        tp2_hint=obj.get("tp2_hint"),
        confidence=int(obj["confidence"]),
        scenario=obj["scenario"],
        cot_justification=obj["cot"]
    )
