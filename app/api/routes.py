from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import init_db
from app.core.weather_handler import get_weather_data

router = APIRouter()

@router.get("/weather")
async def get_weather(
    city: str, 
    current: bool = True, 
    forecast: bool = False, 
    db: Session = Depends(init_db)
):
    return await get_weather_data(city, current, forecast, db)
