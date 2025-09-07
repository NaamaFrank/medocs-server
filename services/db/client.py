import os
from pymongo import MongoClient
from utils.config import MONGO_URI
def get_mongo_client():
    """
    Establishes and returns a MongoDB client connection.

    Raises:
        ValueError: If the MONGODB_URI environment variable is not set.

    Returns:
        MongoClient: An instance of the MongoDB client.
    """
    mongodb_uri = MONGO_URI

    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable not set.")

    try:
        client = MongoClient(mongodb_uri)
        # The ismaster command is cheap and does not require auth.
        # It can be used to check connection health.
        client.admin.command('ismaster')
        print("Successfully connected to MongoDB Atlas!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")
        return None
