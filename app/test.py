import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
import json

# Now import your FastAPI app using an absolute import.
from app.app import app

client = TestClient(app)

def main():
    payload = {
        "url": "https://www.google.com/maps?q=33.41278509999999,-111.8757584,ChIJTaRPqhYIK4cRLpP5vo7Gsj0"
    }
    print("Sending POST /analyze with payload:")
    print(json.dumps(payload, indent=2))
    response = client.post("/analyze", json=payload)
    print("\nStatus Code:", response.status_code)
    try:
        response_data = response.json()
        print("Response JSON:")
        print(json.dumps(response_data, indent=2))
    except Exception as e:
        print("Response text:", response.text)

if __name__ == "__main__":
    main()
