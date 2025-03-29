import subprocess
import os
import re

def extract_text_values(raw_output: str):
    """
    Extract all text values that appear between 'text' and 'language'.
    Returns a list of extracted text strings (reviews_list).
    """
    reviews_list = []
    matches = re.findall(r'text(.*?)language', raw_output)
    for match in matches:
        text_value = match.strip()
        if text_value:
            reviews_list.append(text_value)
    return reviews_list

def run_node_scraper(google_maps_url: str):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        possible_paths = [
            os.path.join(script_dir, "google-review-scraper", "index.js"),
            os.path.join(script_dir, "index.js"),
            os.path.join(script_dir, "..", "google-review-scraper", "index.js"),
        ]
        
        script_path = next((path for path in possible_paths if os.path.exists(path)), None)

        if not script_path:
            print("❌ Node script not found. Please provide the correct path.")
            return []

        print(f"🚀 Running Node script: {script_path}")
        result = subprocess.run(
            ["node", script_path, google_maps_url],
            capture_output=True,
            text=True,
            check=True
        )
        
        raw_output = result.stdout.strip().lstrip('\ufeff').strip()
        raw_output = re.sub(r'[^a-zA-Z0-9; ]', '', raw_output)

        reviews_list = extract_text_values(raw_output)

        # Final clean list (trim trailing characters like semicolons)
        final_reviews = [review[:-1].strip() if review.endswith(";") else review.strip() for review in reviews_list]
        final_reviews = [review[:-1].strip() if review.endswith("n") else review.strip() for review in reviews_list]

        print(len(final_reviews))
        return final_reviews

    except subprocess.CalledProcessError as e:
        print(f"❌ Node scraper process failed (exit code {e.returncode}):")
        print(f"STDERR: {e.stderr}")
        return []
    
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return []
