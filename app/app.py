from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

from google_trigger import run_node_scraper
from insights import generate_actionable_insights, generate_actionable_summaries

app = FastAPI()

class ReviewRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "Use POST /analyze with a Google Maps URL to generate a business summary."}

@app.post("/analyze")
def analyze_reviews(request: ReviewRequest):
    url = request.url
    print(f"🔍 Scraping: {url}")

    # Step 1: Scrape Reviews
    try:
        reviews, ratings = run_node_scraper(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping reviews: {e}")

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this URL.")

    # Step 2: NLP Insights
    try:
        insights, strengths = generate_actionable_insights(reviews)
        recommendations = generate_actionable_summaries(insights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing review insights: {e}")

    summary_input = {
        "strengths": strengths,
        "insights": insights,
        "recommendations": recommendations
    }

    # Step 3: AI Prompt for Mistral
    prompt = f"""
You are an AI assistant summarizing customer review analysis for a business owner.

Given the following structured review data:
{json.dumps(summary_input, indent=2)}

Please return your output in this clean JSON format:

{{
  "qualities": ["short, clear bullet points of what customers liked..."],
  "weaknesses": ["short, clear bullet points of what customers disliked..."],
  "recommendations": ["clear, actionable suggestions the business should consider..."]
}}

✦ Be concise and professional.  
✦ Do not mention sentiment scores or quote the keywords.  
✦ Avoid repeating similar points.  
✦ Keep bullet points under 20 words if possible.
"""

    mistral_payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    # Step 4: Call Ollama + Post-clean Response
    try:
        ollama_response = requests.post("http://localhost:11434/api/generate", json=mistral_payload)
        if ollama_response.status_code != 200:
            raise Exception(f"Ollama error: {ollama_response.text}")

        ai_response = ollama_response.json()["response"]

        # Attempt to parse as JSON
        try:
            summary = json.loads(ai_response)

            # Post-cleaning utility
            def clean_list(items):
                return [item.strip().replace("\n", " ").replace("  ", " ") for item in items]

            return {
                "avg_rating":sum(ratings)/len(ratings),
                "qualities": clean_list(summary.get("qualities", [])),
                "weaknesses": clean_list(summary.get("weaknesses", [])),
                "recommendations": clean_list(summary.get("recommendations", []))
            }

        except json.JSONDecodeError:
            # If AI returns plain text instead of JSON
            return {"ai_summary": ai_response.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate AI summary: {e}")
