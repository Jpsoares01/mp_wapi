import httpx
from datetime import datetime, timedelta
from app.core.config import settings

BASE_URL = settings.BASE_URL

async def _fetch_weather_for_date(client: httpx.AsyncClient, city: str, params: dict, date: datetime) -> dict:
    url = f"{BASE_URL.rstrip('/')}/{city}/{date.strftime('%Y-%m-%d')}"
    print(BASE_URL)
    
    response = await client.get(url, params=params)
    response.raise_for_status()

    return _parse_weather_response(response.json())


async def _fetch_forecast(client: httpx.AsyncClient, city: str, params: dict) -> list:
    forecast_data = []
    
    for day_offset in range(1, 7):
        date = datetime.now() + timedelta(days=day_offset)
        daily_weather = await _fetch_weather_for_date(client, city, params, date)
        forecast_data.extend(daily_weather["days"])
    
    return forecast_data


def search_weather_at_hour(data: dict, current_hour: str) -> dict:
    for hour in data["days"][0]["hours"]:
        if hour["datetime"] == current_hour:
            data["days"][0]["hours"] = [hour]
            return data
        

def search_weather_at_days(data: dict, current_day: str) -> dict:
    for day in data["days"]:
        if day["datetime"] == current_day:
            data["days"] = [day]
            return data


def _parse_weather_response(data: dict) -> dict:
    weather_info = {
        "Address": data["resolvedAddress"],
        "timezone": data["timezone"],
        "days": data["days"],
    }

    return weather_info


async def fetch_weather(city:str, forecast: bool = False) -> dict:
    url = f"{BASE_URL}/{city}"

    elements_list = [
    "datetime",
    "temp",
    "feelslike",
    "humidity",
    "windspeed",
    "winddir",
    "pressure",
    "visibility",
    "cloudcover",
    "uvindex",
    "conditions",
    "icon",
    "sunrise",
    "sunset",
    "moonphase"
    ]
    
    params = {
        "key": settings.API_KEY,
        "unitGroup": "metric",
        "include": "hours",
        "elements": ",".join(elements_list),
    }
    
    async with httpx.AsyncClient() as client:
        try:
            weather_data = await _fetch_weather_for_date(client, city, params, datetime.now())

            if forecast:
                forecast_days = await _fetch_forecast(client, city, params)
                weather_data["days"].extend(forecast_days)

            return weather_data
                
        
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while requesting {e.request.url}.") from e
        
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Error response {e.response.status_code} while requesting {e.request.url}.") from e
