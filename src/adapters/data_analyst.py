import json
from datetime import datetime, timezone
from src.adapters.llm_client import call_llm
from src.models import NewsInsight

PROMPT = """Extract financial news insight as JSON with keys:
ticker, sentiment_score (-1..1), impact_score (1..10), event_type, summary.
Be concise and avoid extra text.
News:
{news_text}
"""

async def analyze_news(news_text: str) -> NewsInsight:
    res = await call_llm(PROMPT.format(news_text=news_text), agent_role="Data Analyst")
    text = res["text"].strip()
    obj = json.loads(text)
    return NewsInsight(
        timestamp=datetime.now(timezone.utc),
        ticker=obj["ticker"],
        sentiment_score=float(obj["sentiment_score"]),
        impact_score=int(obj["impact_score"]),
        event_type=obj.get("event_type"),
        summary=obj.get("summary","")
    )
