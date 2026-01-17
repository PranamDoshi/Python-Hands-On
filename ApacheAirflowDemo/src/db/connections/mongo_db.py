"""MongoDB connection handler."""
from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
from src.config.settings import settings


class MongoDB:
    """MongoDB handler."""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
    
    def connect(self):
        """Connect to MongoDB."""
        if self.client is None:
            self.client = MongoClient(settings.MONGODB_URL)
            self.db = self.client[settings.MONGODB_DB_NAME]
        return self.db
    
    def get_database(self) -> Database:
        """Get the database instance."""
        if self.db is None:
            return self.connect()
        return self.db
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None


_mongo_db = MongoDB()


def get_mongo_client() -> Database:
    """Get MongoDB database instance."""
    return _mongo_db.get_database()
