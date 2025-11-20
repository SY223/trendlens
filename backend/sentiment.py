from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Tuple, List

# Lazy-load model once at startup
_model = None
_tokenizer = None
_labels = ["negative", "neutral", "positive"]

def load_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        # Force safetensors if available
        _tokenizer = AutoTokenizer.from_pretrained(
            "ProsusAI/finbert",
            use_safetensors=True,
            trust_remote_code=True
        )
        _model = AutoModelForSequenceClassification.from_pretrained(
            "ProsusAI/finbert",
            use_safetensors=True,
            trust_remote_code=True
        )
        _model.eval()
    return _model, _tokenizer


def analyze_text(text: str) -> Tuple[str, float]:
    model, tokenizer = load_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1).numpy()[0]
    idx = int(np.argmax(probs))
    sentiment = _labels[idx]
    confidence = float(probs[idx])
    return sentiment, round(confidence, 4)

def analyze_batch(texts: List[str]) -> List[Tuple[str, float]]:
    return [analyze_text(t) for t in texts]