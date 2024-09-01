from bson import ObjectId
from flask import current_app
from pymongo import MongoClient

class Zap_alerts:
    def __init__(self):
        try:
            self.db = MongoClient(
                current_app.config['MONGO_URL'],
                serverSelectionTimeoutMS=5000
            ).grid.alerts
            # self.db.server_info()
        except Exception as e:
            print(e)
        self.db = MongoClient(current_app.config['MONGO_URL']).grid.alerts

    def store_alert(self, alert):
        alerts_collection = self.db
        alert_id = alerts_collection.insert_one(alert).inserted_id
        return alert_id

    def fetch_alert_by_id(self, alert_id):
        return self.db.find_one({'_id': ObjectId(alert_id)})