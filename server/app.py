# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
from pymongo import MongoClient
# import boto3
# import os
from flask import Flask
from flask_cors import CORS
from config import MONGO_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_DELTA
from routes.authenticate import authenticate

print(MONGO_URL)
app = Flask(__name__)
app.config['MONGO_URL'] = MONGO_URL
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
app.config['JWT_EXPIRATION_DELTA'] = JWT_EXPIRATION_DELTA
CORS(app)

# db = MongoClient(
#     app.config['MONGO_URL'],
#     serverSelectionTimeoutMS=5000
# )
# print(db.server_info())

app.register_blueprint(authenticate)

if __name__ == '__main__':
    app.run(debug=True)