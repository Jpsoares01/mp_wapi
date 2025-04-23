from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.database.db import init_db
from app.database.models import WeatherRequest
from app.core.cache import get_weather_from_cache, set_weather_in_cache
from app.core.weather_service import fetch_weather, search_weather_at_hour, search_weather_at_days


async def _get_cached_weather_data(city: str, current: bool, forecast: bool, current_hour: str) -> dict:
    cached_data = await get_weather_from_cache(city)
    if cached_data:
        if current:
            return {"source": "cache", "data": search_weather_at_hour(cached_data.copy(), current_hour)}
        
        elif not forecast:
            return {"source": "cache", "data": cached_data}
    return None


async def _get_db_weather_data(db_data: dict, current: bool, forecast: bool, current_date: str, current_hour: str) -> dict:
    days = db_data.data.get("days", [])

    if current:
        day_data = search_weather_at_days(db_data.data.copy(), current_date)
        hour_data = search_weather_at_hour(day_data, current_hour)
        return {"source": "database", "data": hour_data}

    else:
        if (forecast and len(days) > 1):
            return {"source": "database", "data": db_data.data}
        
        elif (not forecast and len(days) > 1):
            data = search_weather_at_days(db_data.data.copy(), current_date)
            return {"source": "database", "data": data} 

        elif (not forecast):
            return {"source": "database", "data": db_data.data}


async def get_weather_data(city: str, current: bool = True, forecast: bool = False, db: Session = Depends(init_db)) -> dict:    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().replace(minute=0, second=0).strftime("%H:%M:%S")

    cached_result = await _get_cached_weather_data(city, current, forecast, current_hour)
    if cached_result:
        return cached_result

    db_data = db.query(WeatherRequest).filter(
        WeatherRequest.city == city,
        func.json_extract(WeatherRequest.data, '$.days[0].datetime') == current_date
    ).first()

    if db_data:
        db_result = await _get_db_weather_data(db_data, current, forecast, current_date, current_hour)
        if db_result:
            return db_result
           
    try:
        weather_data = await fetch_weather(city, forecast)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not forecast:
        await set_weather_in_cache(city, weather_data)

    existing_entry = db.query(WeatherRequest).filter_by(city=city).first()

    if existing_entry:
        existing_entry.data = weather_data
    else:
        db_entry = WeatherRequest(
            city=city,
            data=weather_data,
        )
        db.add(db_entry)

    db.commit()

    if current:    
        return {"source": "api", "data": search_weather_at_hour(weather_data.copy(), current_hour)}
    
    return {"source": "api", "data": weather_data}
