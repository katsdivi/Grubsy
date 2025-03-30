from playwright.sync_api import sync_playwright
import urllib.parse
import re

def get_detailed_place_url(place_name):
    query = urllib.parse.quote(place_name)
    search_url = f"https://www.google.com/maps/search/?api=1&query={query}"

    aria_label_prefix = place_name.strip().split()[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False to debug visually
        page = browser.new_page()
        page.goto(search_url)

        selector = f'[aria-label^="{aria_label_prefix}"]'
        page.wait_for_selector(selector, timeout=10000)
        page.locator(selector).first.click()

        page.wait_for_timeout(5000)  # Wait for detailed view to load
        final_url = page.url
        browser.close()
        return final_url

def convert_to_place_url(raw_url):
    match = re.search(r"maps\?q=[^,]+,[^,]+,([^&]+)", raw_url)
    if match:
        place_id = match.group(1)
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    return "Invalid URL format."

def is_google_maps_url(input_str):
    return "maps.google.com" in input_str or "www.google.com/maps" in input_str

def resolve_input_to_place_url(input_str):
    if is_google_maps_url(input_str):
        return convert_to_place_url(input_str)
    else:
        return get_detailed_place_url(input_str)

# 🔧 Example usage
inputs = [
    "Dutch bros near HAV"
]

for i in inputs:
    print(resolve_input_to_place_url(i))
