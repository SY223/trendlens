from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .models import (
    AnalyzeRequest, AnalyzeResponse,
    HeadlinesRequest, HeadlinesResponse,
    BatchAnalyzeRequest, BatchAnalyzeResponse, BatchAnalyzeItem,
)
from .sentiment import analyze_text, analyze_batch, load_model
from .news import fetch_headlines, NewsError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code before the "yield" runs on startup
    print("App startup: Loading sentiment model...")
    load_model()  # Your existing sync function is fine to call here
    print("Model loaded.")
    yield  # <-- The app is now running  
    # Code after the "yield" (if any) runs on shutdown
    print("App shutting down.")


app = FastAPI(title="Fintech News Sentiment Analyzer", version="1.0.0", lifespan=lifespan)

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        sentiment, confidence = analyze_text(req.headline)
        return AnalyzeResponse(sentiment=sentiment, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {e}")

@app.post("/headlines", response_model=HeadlinesResponse)
async def headlines(req: HeadlinesRequest):
    try:
        return await fetch_headlines(req)
    except NewsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Headlines error: {e}")

@app.post("/sentiment/batch", response_model=BatchAnalyzeResponse)
def sentiment_batch(req: BatchAnalyzeRequest):
    try:
        results_raw = analyze_batch(req.headlines)
        items = [
            BatchAnalyzeItem(headline=h, sentiment=s, confidence=c)
            for h, (s, c) in zip(req.headlines, results_raw)
        ]
        return BatchAnalyzeResponse(results=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis error: {e}")

# To run the app, use: uvicorn backend.main:app --reloadp