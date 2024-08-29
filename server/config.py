import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGODB_URL')
print(MONGO_URL)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secureauth')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 86400