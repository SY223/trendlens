from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    newsapi_key: str | None = os.getenv("NEWSAPI_KEY")
    # Optional: throttle or defaults
    default_query: str = "fintech OR payments OR banking OR crypto OR blockchain"
    newsapi_url: str = "https://newsapi.org/v2/everything"

settings = Settings()