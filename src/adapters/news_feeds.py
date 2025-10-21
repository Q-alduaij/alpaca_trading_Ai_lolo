# src/adapters/news_feeds.py
import os, httpx

async def fetch_news_from_newsapi(symbol: str, limit: int = 10):
    key = os.getenv("NEWSAPI_KEY_1")
    if not key:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {"q": symbol, "pageSize": limit, "language": "en", "sortBy": "publishedAt", "apiKey": key}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json().get("articles", [])
