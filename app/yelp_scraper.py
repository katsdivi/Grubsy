import undetected_chromedriver as uc
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time

def scrape_yelp(url: str, max_scrolls: int = 5) -> list[str]:
    options = uc.ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={UserAgent().random}")

    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Let the page load

    # Scroll down multiple times
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Try both p.comment and span.raw (Yelp sometimes uses one or both)
    review_tags = soup.select("p.comment__373c0__Nsutg, span.raw__373c0__tQAx6")

    reviews = [tag.get_text(strip=True) for tag in review_tags if tag.get_text(strip=True)]


    driver.quit()
    return reviews