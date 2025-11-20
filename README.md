# Fintech News Sentiment Analyzer

A web application that fetches fintech-related headlines, analyses their sentiment using **FinBERT**, and visualises sentiment distribution with **Chart.js**.  
Built with **FastAPI** (backend), **SQLite** (database), and a simple **HTML/CSS/JS frontend** styled with CSS Grid.

---

## 🚀 Features
- Search fintech headlines by keyword (e.g., *Stripe*, *Bitcoin*).
- Sentiment analysis powered by FinBERT (Positive / Neutral / Negative).
- Confidence scores for each prediction.
- Interactive sentiment distribution chart.
- Responsive UI with CSS Grid layout.

---

## 📦 Tech Stack
- **Backend:** FastAPI, Python
- **Frontend:** HTML, CSS Grid, JavaScript
- **Database:** SQLite
- **Visualization:** Chart.js
- **NLP Model:** FinBERT

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone git@github.com:SY223/trendlens.git
cd trendlens
```

### 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a .env file
You must create a .env file in the project root with your NewsAPI key:
```Env
NEWSAPI_KEY=your_api_key_here
```

### 5. Run the FastAPI server
```bash
uvicorn main:app --reload
```


