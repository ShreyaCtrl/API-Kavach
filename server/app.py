from flask import Flask
from flask_cors import CORS
from config import MONGO_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_DELTA, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from config import ZAP_API_KEY, ZAP_BASE_URL
from routes.authenticate import authenticate
from aws import api_gateway_client, logs_client
from routes.api_routes import api_bp
from routes.logs_route import logs
from routes.zap_routes import zap

# print(MONGO_URL)
app = Flask(__name__)

app.config['MONGO_URL'] = MONGO_URL
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
app.config['JWT_EXPIRATION_DELTA'] = JWT_EXPIRATION_DELTA
app.config['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
app.config['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
app.config['AWS_REGION'] = AWS_REGION
app.config['ZAP_API_KEY'] = ZAP_API_KEY
app.config['ZAP_BASE_URL'] = ZAP_BASE_URL

CORS(app)
# print(api_gateway_client, logs_client)

# db = MongoClient(
#     app.config['MONGO_URL'],
#     serverSelectionTimeoutMS=5000
# )
# print(db.server_info())

app.register_blueprint(authenticate)
app.register_blueprint(api_bp)
app.register_blueprint(logs)
app.register_blueprint(zap)

if __name__ == '__main__':
    app.run(debug=True)