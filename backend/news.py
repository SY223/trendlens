import httpx
from typing import List
from .config import settings
from .models import HeadlinesRequest, Headline, HeadlinesResponse

class NewsError(Exception):
    pass

async def fetch_headlines(params: HeadlinesRequest) -> HeadlinesResponse:
    if not settings.newsapi_key:
        raise NewsError("Missing NEWSAPI_KEY in environment.")

    query = params.query or settings.default_query
    query = query.strip()

    qparams = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": min(params.page_size, 100),
        "apiKey": settings.newsapi_key,
    }
    if params.from_date:
        qparams["from"] = params.from_date
    if params.to_date:
        qparams["to"] = params.to_date

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(settings.newsapi_url, params=qparams)
        if r.status_code != 200:
            raise NewsError(f"News API error: {r.status_code} {r.text}")
        data = r.json()

    articles = data.get("articles", [])
    items: List[Headline] = []
    for a in articles:
        title = a.get("title") or ""
        source = (a.get("source") or {}).get("name") or "Unknown"
        published_at = a.get("publishedAt") or ""
        url = a.get("url") or ""
        if title:
            items.append(Headline(title=title, source=source, published_at=published_at, url=url))

    return HeadlinesResponse(count=len(items), items=items)