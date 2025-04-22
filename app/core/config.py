from dotenv import load_dotenv
import os

load_dotenv('./dotenv/.env')

class Settings:
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


    if not API_KEY or not BASE_URL or not DATABASE_URL:
        raise ValueError("Missing required environment variables.")
    
settings = Settings()
