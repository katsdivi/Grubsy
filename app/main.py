from google_trigger import run_node_scraper
from insights import generate_actionable_insights, generate_actionable_summaries

def main():
    # 🔗 Google Maps business URL
    url = "https://www.google.com/maps/place/Starbucks/@33.4097855,-111.9285169,16z/data=!4m8!3m7!1s0x872b08eaf90c9655:0x874259164a48a72b!8m2!3d33.409781!4d-111.925942!9m1!1b1!16s%2Fg%2F1q6cn9pl9?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoJLDEwMjExNjM5SAFQAw%3D%3D"
    print(f"🔍 Fetching reviews from: {url}")
    
    # 🔄 Scrape reviews + ratings
    reviews, ratings = run_node_scraper(url)

    print(f"🧾 Total Reviews Collected: {len(reviews)}")

    if not reviews:
        print("⚠️ No reviews found for this URL.")
        return

    # 🧠 Run full NLP pipeline on all reviews (not just low-rated)
    insights, strengths = generate_actionable_insights(reviews)
    summaries = generate_actionable_summaries(insights)

    # 📊 Output insights
    print("🔍 Actionable Insights:")
    for k, v in insights.items():
        print(f"- {k.title()}: {v}")

    print("\n🌟 Strengths:")
    for k, v in strengths.items():
        print(f"- {k.title()}: {v}")


    # 📋 Output summaries
    print("\n📋 Recommendations:")
    for summary in summaries:
        print("-", summary)

if __name__ == "__main__":
    main()
