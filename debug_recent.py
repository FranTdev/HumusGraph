import httpx
import asyncio
import json
from datetime import datetime, timedelta

RAPIDAPI_KEY = "a893590b79mshb250d5ae9c397b1p1710c0jsn5c2b86fdccfd"
RAPIDAPI_HOST = "meteostat.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}


async def check_recent():
    async with httpx.AsyncClient() as client:
        # Check last 5 days for station 80259 (Cali Airport)
        today = datetime.now()
        start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")

        print(f"Checking data for 80259 from {start} to {end}")
        url = "https://meteostat.p.rapidapi.com/stations/daily"
        params = {"station": "80259", "start": start, "end": end}

        try:
            resp = await client.get(url, headers=HEADERS, params=params)
            print(f"Status: {resp.status_code}")
            data = resp.json().get("data", [])
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(check_recent())
