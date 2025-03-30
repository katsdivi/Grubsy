from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google_trigger import run_node_scraper
from insights import generate_actionable_insights, generate_actionable_summaries

app = FastAPI()

# Request model for input validation
class ReviewRequest(BaseModel):
    url: str

@app.post("/analyze")
def analyze_reviews(request: ReviewRequest):
    url = request.url
    print(f"🔍 Fetching reviews from: {url}")

    # Scrape reviews + ratings
    reviews, ratings = run_node_scraper(url)

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this URL.")

    # Run NLP pipeline
    insights, strengths = generate_actionable_insights(reviews)
    summaries = generate_actionable_summaries(insights)

    return {
        "total_reviews": len(reviews),
        "insights": insights,
        "strengths": strengths,
        "recommendations": summaries
    }

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Review Analyzer!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
