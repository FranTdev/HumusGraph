import os
from datetime import datetime, timedelta
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Coordinate estimate for KM 18 Via al Mar/Dagua, Cali
# You can change these using .env variables
KM18_LAT = os.getenv("WEATHER_LAT", "3.513")
KM18_LON = os.getenv("WEATHER_LON", "-76.608")

# Headers for RapidAPI
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_rapidapi_key_here")
RAPIDAPI_HOST = "meteostat.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}


async def get_external_weather():
    """
    Fetches weather data for KM 18.
    Strategy:
    1. Find the nearest station using /stations/nearby.
    2. Query /stations/daily for that specific station ID.
    This is more robust than /point/daily for rural locations.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. Find Nearest Station
            print(f"Finding nearest station for {KM18_LAT}, {KM18_LON}...")
            url_nearby = "https://meteostat.p.rapidapi.com/stations/nearby"
            params_nearby = {"lat": KM18_LAT, "lon": KM18_LON, "limit": "1"}

            resp_nearby = await client.get(
                url_nearby, headers=HEADERS, params=params_nearby
            )
            if resp_nearby.status_code != 200:
                print(f"Error fetching nearby stations: {resp_nearby.status_code}")
                return None

            stations = resp_nearby.json().get("data", [])
            if not stations:
                print("No nearby stations found.")
                return None

            station_id = stations[0]["id"]
            station_name = stations[0].get("name", {}).get("en", "Unknown Station")
            print(f"Nearest Station: {station_name} (ID: {station_id})")

            # 2. Get Daily Data for that Station
            # Check last 5 days to ensure we get at least one record
            today = datetime.now()
            start_date = (today - timedelta(days=5)).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

            url_daily = "https://meteostat.p.rapidapi.com/stations/daily"
            params_daily = {"station": station_id, "start": start_date, "end": end_date}

            print(
                f"Fetching daily data for station {station_id} ({start_date} to {end_date})..."
            )
            resp_daily = await client.get(
                url_daily, headers=HEADERS, params=params_daily
            )

            if resp_daily.status_code == 200:
                data = resp_daily.json().get("data", [])
                if data:
                    print(f"Success! Retrieved {len(data)} daily records.")
                    return data
                else:
                    print("Station found, but no recent daily data available.")

                    # Fallback: Try Hourly if daily is empty
                    print("Trying hourly data as fallback...")
                    url_hourly = "https://meteostat.p.rapidapi.com/stations/hourly"
                    resp_hourly = await client.get(
                        url_hourly, headers=HEADERS, params=params_daily
                    )
                    if resp_hourly.status_code == 200:
                        hourly_data = resp_hourly.json().get("data", [])
                        if hourly_data:
                            latest = hourly_data[-1]
                            return [
                                {
                                    "date": latest.get("time"),
                                    "tavg": latest.get("temp"),
                                    "prcp": latest.get("prcp"),
                                    "wspd": latest.get("wspd"),
                                    "pres": latest.get("pres"),
                                }
                            ]
            else:
                print(f"Error fetching daily data: {resp_daily.status_code}")

            return []

    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        return None
