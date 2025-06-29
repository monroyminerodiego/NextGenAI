import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv; load_dotenv()

MONGO_URI = os.getenv("DATABASE_URL")

client = AsyncIOMotorClient(MONGO_URI)

mongo_db = client["nextgenai_db"]
