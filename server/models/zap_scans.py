from flask import current_app
from pymongo import MongoClient

class Zap_scan:
    def __init__(self):
        try:
            self.db = MongoClient(
                current_app.config['MONGO_URL'],
                serverSelectionTimeoutMS=5000
            ).grid.scans
            # self.db.server_info()
        except Exception as e:
            print(e)
        self.db = MongoClient(current_app.config['MONGO_URL']).grid.scans

    def store_scan(self, scan):
        scan_collection = self.db
        scan_id = scan_collection.insert_one(scan).inserted_id
        return scan_id

    def find_scan(self):
        return self.db.find()