from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["secure_file_sharing"]
users_collection = db["users"]
files_collection = db["files"]
