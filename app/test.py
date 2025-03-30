import requests

url = 'http://127.0.0.1:8000/analyze'
test_data = {
    "url": "https://www.google.com/maps/place/Panda+Express/@33.4555916,-112.0921321,12.51z/data=!4m10!1m2!2m1!1spanda+express!3m6!1s0x872b08ead4772ded:0x81b7f1d9efc0ae24!8m2!3d33.407917!4d-111.9257701!15sCg1wYW5kYSBleHByZXNzIgOIAQFaDyINcGFuZGEgZXhwcmVzc5IBEmNoaW5lc2VfcmVzdGF1cmFudOABAA!16s%2Fg%2F1ptxv8js7?entry=ttu&g_ep=EgoyMDI1MDMyNS4xIKXMDSoJLDEwMjExNjM5SAFQAw%3D%3D"
}

response = requests.post(url, json=test_data)

if response.status_code == 200:
    print("✅ Success!")
    print("📦 Response JSON:", response.json())
else:
    print(f"❌ Failed with status code {response.status_code}")
    print("Response Text:", response.text)
