from google_trigger import run_node_scraper

def main():
    # Specify the Google Maps URL to fetch data from.
    url = "https://www.google.com/maps/place/Unphởgettable/@33.4127896,-111.8783333,17z/data=!3m1!4b1!4m6!3m5!1s0x872b0816aa4fa44d:0x3db2c68ebef9932e!8m2!3d33.4127851!4d-111.8757584!16s%2Fg%2F1tjgq15t?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoASAFQAw%3D%3D"
    print(f"🔍 Fetching reviews from: {url}")
    
    # Call the scraper to get raw output; this will print extracted substrings inside the function.
    raw_output = run_node_scraper(url)
    
    # Optionally, print the final raw output.
    print("\nFinal raw output:")
    print(raw_output)
    

if __name__ == "__main__":
    main()
