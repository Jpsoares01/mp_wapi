from fastapi import FastAPI
from app.api.routes import router as weather_router
from app.database.db import init_db, engine, Base
from app.database.models import WeatherRequest


app = FastAPI(title="Weather API Wrapper")

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(weather_router, prefix="/api")