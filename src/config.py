from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
import os, sys

load_dotenv()

class Settings(BaseModel):
    # Alpaca (Paper)
    alpaca_api_key_id: str = Field(..., description="Alpaca API key (paper)")
    alpaca_api_secret_key: str = Field(..., description="Alpaca API secret (paper)")
    alpaca_paper_base_url: str = Field(default="https://paper-api.alpaca.markets")

    # Data/News providers (optional but supported)
    polygon_api_key: str | None = os.getenv("POLYGON_API_KEY")
    finnhub_api_key: str | None = os.getenv("FINNHUB_API_KEY")
    alphavantage_api_key: str | None = os.getenv("ALPHAVANTAGE_API_KEY")
    twelvedata_api_key: str | None = os.getenv("TWELVEDATA_API_KEY")
    fmp_api_key: str | None = os.getenv("FMP_API_KEY")
    newsapi_key_1: str | None = os.getenv("NEWSAPI_KEY_1")
    newsapi_key_2: str | None = os.getenv("NEWSAPI_KEY_2")
    newsapi_key_3: str | None = os.getenv("NEWSAPI_KEY_3")

    # LLM
    llm_mode: str = os.getenv("LLM_MODE", "openai_compat")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "local-only")

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")

    # Risk
    daily_dd_halt_pct: float = float(os.getenv("DAILY_DRAWDOWN_HALT_PCT", "5"))
    total_dd_halt_pct: float = float(os.getenv("TOTAL_DRAWDOWN_HALT_PCT", "15"))
    max_sector_exposure_pct: float = float(os.getenv("MAX_SECTOR_EXPOSURE_PCT", "30"))
    confidence_threshold: int = int(os.getenv("CONFIDENCE_THRESHOLD", "75"))

try:
    SETTINGS = Settings(
        alpaca_api_key_id=os.getenv("ALPACA_API_KEY_ID"),
        alpaca_api_secret_key=os.getenv("ALPACA_API_SECRET_KEY"),
        alpaca_paper_base_url=os.getenv("ALPACA_PAPER_BASE_URL", "https://paper-api.alpaca.markets"),
    )
except ValidationError as e:
    print("FATAL: Missing required environment variables for Alpaca. Create/complete your .env.")
    print(e)
    sys.exit(1)
