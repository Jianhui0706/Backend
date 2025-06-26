import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Load variables from .env

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["parking_app"]
user_collection = db["users"]