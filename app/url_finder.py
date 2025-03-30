from playwright.sync_api import sync_playwright
import urllib.parse
import re

from playwright.async_api import async_playwright
import urllib.parse

async def get_detailed_place_url(place_name):
    query = urllib.parse.quote(place_name)
    search_url = f"https://www.google.com/maps/search/?api=1&query={query}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(search_url)

        # Use a generic selector to match any restaurant/place
        selector = 'a.hfpxzc[aria-label][href^="https://www.google.com/maps/place/"]'
        await page.wait_for_selector(selector, timeout=15000)
        element = page.locator(selector).first  # No 'await' here
        link = await element.get_attribute("href")  # Await the get_attribute call

        await browser.close()
        if link:
            return link
        else:
            raise Exception("Could not extract href from the result anchor tag.")


def convert_to_place_url(raw_url):
    match = re.search(r"maps\?q=[^,]+,[^,]+,([^&]+)", raw_url)
    if match:
        place_id = match.group(1)
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    return "Invalid URL format."

def is_google_maps_url(input_str):
    return "maps.google.com" in input_str or "www.google.com/maps" in input_str

async def resolve_input_to_place_url(input_str):
    if is_google_maps_url(input_str):
        return convert_to_place_url(input_str)  # Already a str
    else:
        return await get_detailed_place_url(input_str)  # Needs await

