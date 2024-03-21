from pymongo import MongoClient


import os
from dotenv import load_dotenv
import pymongo

load_dotenv()


mongo_uri = os.getenv("MONGO_URL")

client = MongoClient(mongo_uri) 
print(12)
db = client["ZuPay"]
print(db)
users_collection = db["users"]
blogs_collection = db["blogs"]


