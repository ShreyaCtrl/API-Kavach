from flask import request, current_app
import jwt

def decode_token_and_get_user_id(token):
    try:
        # Decode the JWT token using the secret key
        decoded = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=current_app.config['JWT_ALGORITHM'])
        # Return the user ID from the decoded token
        # print(decoded)
        return decoded.get('username')
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None
