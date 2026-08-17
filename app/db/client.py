from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os 

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
mongo_client: AsyncMongoClient = AsyncMongoClient(MONGO_URI)