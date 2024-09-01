import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGODB_URL')
print(MONGO_URL)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secureauth')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 86400

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')

ZAP_API_KEY= os.environ.get('ZAP_API_KEY')
ZAP_BASE_URL = os.environ.get('ZAP_BASE_URL')
