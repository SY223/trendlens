from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    headline: str = Field(..., min_length=3)

class AnalyzeResponse(BaseModel):
    sentiment: str
    confidence: float

class HeadlinesRequest(BaseModel): #What the client request
    query: Optional[str] = None
    from_date: Optional[str] = None  # YYYY-MM-DD
    to_date: Optional[str] = None
    page_size: int = 20

class Headline(BaseModel): #What a single headline looks like
    title: str
    source: str
    published_at: str
    url: str

class HeadlinesResponse(BaseModel):
    count: int
    items: List[Headline]

class BatchAnalyzeRequest(BaseModel):
    headlines: List[str]

class BatchAnalyzeItem(BaseModel):
    headline: str
    sentiment: str
    confidence: float

class BatchAnalyzeResponse(BaseModel):
    results: List[BatchAnalyzeItem]