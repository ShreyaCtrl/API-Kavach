from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app

class User:
    def __init__(self):
        try:
            self.db = MongoClient(
                current_app.config['MONGO_URL'],
                serverSelectionTimeoutMS=5000
            ).grid.users
            # self.db.server_info()
        except Exception as e:
            print(e)
        self.db = MongoClient(current_app.config['MONGO_URL']).grid.users

    def create_user(self, user_data):
        db_response = self.db.insert_one(user_data)
        return str(db_response.inserted_id)

    def update_user(self, user_id, update_data):
        db_response = self.db.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return db_response.modified_count

    def find_user_by_username(self, username):
        user = self.db.find({'username': username})
        return list(user)