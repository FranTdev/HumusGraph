import httpx
import asyncio
import json

# KM 18 Coordinates
LAT = "3.513"
LON = "-76.608"
ALT = "1800"

RAPIDAPI_KEY = "a893590b79mshb250d5ae9c397b1p1710c0jsn5c2b86fdccfd"
RAPIDAPI_HOST = "meteostat.p.rapidapi.com"

HEADERS = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}


async def debug_meteostat():
    async with httpx.AsyncClient() as client:
        print("--- 1. Testing Stations Nearby ---")
        url_nearby = "https://meteostat.p.rapidapi.com/stations/nearby"
        params_nearby = {"lat": LAT, "lon": LON, "limit": "5"}
        try:
            resp = await client.get(url_nearby, headers=HEADERS, params=params_nearby)
            print(f"Status: {resp.status_code}")
            stations = resp.json().get("data", [])
            print(json.dumps(stations, indent=2))

            if not stations:
                print("No nearby stations found.")
                return

            # Pick the nearest station
            nearest_station = stations[0]["id"]
            print(f"\n--- 2. Testing Data for Nearest Station ({nearest_station}) ---")

            url_daily = "https://meteostat.p.rapidapi.com/stations/daily"
            # Try getting data for 2024 or 2025 to see if there is ANY recent data
            params_daily = {
                "station": nearest_station,
                "start": "2024-01-01",
                "end": "2024-01-05",
            }
            resp_daily = await client.get(
                url_daily, headers=HEADERS, params=params_daily
            )
            print(f"Status: {resp_daily.status_code}")
            print(json.dumps(resp_daily.json(), indent=2))

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(debug_meteostat())
