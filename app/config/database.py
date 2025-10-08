from pymongo import MongoClient
from .settings import settings

class Database:
    client = None
    db = None

    @classmethod
    def connect(cls):
        """Connect to MongoDB"""
        if cls.client is None:
            cls.client = MongoClient(settings.mongodb_uri)
            cls.db = cls.client[settings.database_name]
        return cls.db

    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.db is None:
            cls.connect()
        return cls.db

    @classmethod
    def close(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
