import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class ConfigMYSQL:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy's modification tracking
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_DATABASE_URL")
        

class ConfigMongo:
    # Use a class-level attribute to store the MongoDB client instance
    _mongo_client = None

    @staticmethod
    def get_client():
        if ConfigMongo._mongo_client is None:
            ConfigMongo._mongo_client = MongoClient(os.getenv("MONGODB_DATABASE_URL"), serverSelectionTimeoutMS=2000)
        return ConfigMongo._mongo_client["ProjectData"]  # Return the database instance
