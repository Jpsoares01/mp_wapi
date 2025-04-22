from sqlalchemy import Column, Integer, String, JSON
from datetime import datetime
from app.database.db import Base

class WeatherRequest(Base):
    __tablename__ = "weather_requests"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    data = Column(JSON)
