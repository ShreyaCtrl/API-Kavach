from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app

class Api:
    def __init__(self):
        try:
            self.db = MongoClient(
                current_app.config['MONGO_URL'],
                serverSelectionTimeoutMS=5000
            ).grid.api
            # self.db.server_info()
        except Exception as e:
            print(e)
        self.db = MongoClient(current_app.config['MONGO_URL']).grid.api

    def create_api(self, api_data):
        db_response = self.db.insert_one(api_data)
        return str(db_response.inserted_id)

    def update_api(self, api_id, update_data):
        db_response = self.db.update_one({'_id': ObjectId(api_id)}, {'$set': update_data})
        return db_response.modified_count

    def find_api_by_apiname(self, apiname):
        api = self.db.find({'apiname': apiname})
        return list(api)

    def find_api_by_id(self, api_id):
        # Ensure the API ID is valid and convert to ObjectId
        try:
            api_object_id = ObjectId(api_id)
        except Exception as e:
            print(f"Invalid API ID format: {e}")
            return None

        api = self.db.find_one({'_id': api_object_id})
        return api

    def get_all_apis(self):
        # Fetch all APIs from the MongoDB collection
        apis = self.db.find()
        return list(apis)

    def insert_apis(self, insert_data):
        # db_response = self.db.insert_one(insert_data)
        db_response = self.db.insert_many(insert_data)

        return str(db_response.inserted_ids)