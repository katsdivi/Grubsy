import asyncio
from url_finder import resolve_input_to_place_url

async def test_inputs():
    test_cases = [
        "Hungry Howies near apache",
        "Starbucks at mill",
        "https://www.google.com/maps?q=33.41278509999999,-111.8757584,ChIJTaRPqhYIK4cRLpP5vo7Gsj0"
    ]

    for input_str in test_cases:
        print(f"\n🔍 Input: {input_str}")
        try:
            resolved_url = await resolve_input_to_place_url(input_str)
            print(f"✅ Resolved URL: {resolved_url}")
        except Exception as e:
            print(f"❌ Failed for input: {input_str}\n   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_inputs())
