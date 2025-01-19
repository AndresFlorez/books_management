from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.client = MongoClient(host, port, username=user, password=password)
        self.database = self.client[database]

    def get_database(self):
        return self.database
