import httpx
import asyncio

API_KEY = "b51e0c093dd7dbb543fe8b1c9e24677642d7190ccabff279dad41b8257de4411"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam


async def test_voice():
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": "Prueba de voz Adam.",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    print(f"Testing ElevenLabs API with Voice ID: {VOICE_ID}...")
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Audio binary received.")
    else:
        print(f"Error Response: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_voice())
