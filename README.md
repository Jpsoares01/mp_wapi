# Weather API Wrapper Service

A high-performance Weather API Wrapper Service built using FastAPI, SQLAlchemy, Redis, and the VisualCrossing API. This service provides efficient, scalable, and reliable access to current and forecasted weather data. It integrates caching and persistent storage for faster response times and data consistency.

## Features
- Real-Time Weather Fetching: Fetch current weather data, including temperature, humidity, and other key metrics.
- Hourly Weather Data: Access hour-by-hour weather data for today, with the ability to filter by specific hours.
- 7-Day Weather Forecast: Retrieve forecast data for the next 7 days, broken down by day and hour.
- Caching with Redis: Cached responses to minimize external API calls, leading to reduced load times and more efficient data retrieval.
- SQLite Storage: Stores historical weather queries for fallback purposes and can serve as a backup in case caching or external API data retrieval fails.
- Fallback Mechanism: Automatically uses cached data or database-stored data when external API requests are not possible.

## Technologies Used
- FastAPI: A modern, high-performance web framework for building APIs with Python.
- SQLAlchemy: ORM (Object Relational Mapper) used for interacting with the SQLite database.
- Redis: An in-memory data store used for caching weather data to speed up repeated requests.
- SQLite: A lightweight database used to persist weather data for fallbacks and historical queries.
- VisualCrossing API: External API used as the source for weather data (e.g., temperature, humidity, forecasts).
- Python 3.9+: The programming language used to build the service.

## API Endpoints
### GET `/weather`
Fetch weather data for a specified city. You can request current weather or forecast data.

## Query Parameters:
- city (str): The name of the city you want to fetch weather data for (e.g., London).
- current (bool, optional): If True, returns current weather data. Default is True.
- forecast (bool, optional): If True, returns weather forecast for the next 7 days. Default is False.

### Example Request:

```bash
GET /weather?city=London&current=true&forecast=false
```

### Example Request (JSON)
```json
{
  "source": "api",
  "data": {
    "Address": "London, England, United Kingdom",
    "timezone": "Europe/London",
    "days": [
      {
        "datetime": "2025-04-28",
        "temp": 16.3,
        "feelslike": 16.3,
        "humidity": 58.4,
        "windspeed": 11.5,
        "winddir": 142.9,
        "pressure": 1026.5,
        "cloudcover": 57,
        "visibility": 21.8,
        "uvindex": 8,
        "sunrise": "05:37:49",
        "sunset": "20:19:20",
        "moonphase": 0.02,
        "conditions": "Partially cloudy",
        "icon": "partly-cloudy-day",
        "hours": [
          {
            "datetime": "04:00:00",
            "temp": 10.4,
            "feelslike": 10.4,
            "humidity": 80.01,
            "windspeed": 2.9,
            "winddir": 215.7,
            "pressure": 1026,
            "visibility": 24.1,
            "cloudcover": 56,
            "uvindex": 0,
            "conditions": "Partially cloudy",
            "icon": "partly-cloudy-night"
          }
        ]
      }
    ]
  }
}
```

### Response Example Breakdown:
- "source": Indicates the origin of the data (api, database, cache).
- "data": Weather data for the requested city, including temperature, humidity, and conditions for both current and forecast data.

## Setup and Installation
**1.** Clone this repository:
```bash
git clone https://github.com/Jpsoares01/mp_wapi.git
```

**2.** Install dependencies:
```bash
pip install -r requirements.txt
```

**3.** Set up your environment variables: Ensure you have the necessary credentials for the VisualCrossing API and Redis. Set up these environment variables in a .env file.

**4.** Set up Redis using Docker:
- First, ensure you have Docker installed and running
- Run the following command to pull the official Redis image and start a Redis container:

```bash
docker run --name redis -p 6379:6379 -d redis
```

**5.** Run the application: Start the FastAPI server with Uvicorn:
```bash
uvicorn app.main:app --reload
```

**6.** Visit http://localhost:8000/docs to view the auto-generated Swagger API documentation.

## Project Structure
```text
mp_wapi/
├── README.md
├── requirements.txt
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── cache.py
│   │   ├── config.py
│   │   ├── weather_handler.py
│   │   └── weather_service.py
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   └── main.py
├── dotenv/
│   └── .env_example
```
