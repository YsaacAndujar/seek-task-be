from pymongo import MongoClient
import os

_client = None

def get_database():
    global _client
    if _client is None:
        uri = os.environ.get("MONGO_URI")
        _client = MongoClient(uri)
    return _client["seek-task"]
