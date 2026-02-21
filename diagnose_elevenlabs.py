import httpx
import asyncio

# New Key provided by user
API_KEY = "sk_7709ba23f32e3372b7867c316cdc9f48c27c6ceb257551a5"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam


async def test_voice():
    url = f"https://api.elevenlabs.io/v1/user/subscription"
    headers = {"xi-api-key": API_KEY.strip(), "Content-Type": "application/json"}

    print(f"1. Checking Subscription Status for Key: {API_KEY[:5]}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Plan: {data.get('tier')}")
                print(
                    f"Character Count: {data.get('character_count')} / {data.get('character_limit')}"
                )
                if data.get("character_count") >= data.get("character_limit"):
                    print("❌ QUOTA EXCEEDED (Sin créditos)")
                else:
                    print("✅ Credits Available")
            else:
                print(f"❌ API Error: {response.text}")

        except Exception as e:
            print(f"❌ Network/Client Error: {e}")

    print("\n2. Testing Voice Synthesis...")
    url_synth = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    data = {"text": "Prueba de sistema.", "model_id": "eleven_monolingual_v1"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url_synth, json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Voice Synthesis Works!")
        else:
            print(f"❌ Synthesis Failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_voice())
