import os
import pymongo
from Utils.constans import constants


async def get_sync_db_connection():
    client = pymongo.MongoClient(os.getenv("DB_CONNECTION_URI"))
    db = client[constants.db_name]
    return db
