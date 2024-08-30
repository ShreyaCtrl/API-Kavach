from functools import wraps
from flask import request, jsonify, current_app
from models.user import User
from .before_request import decode_token_and_get_user_id

def check_user_role(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({"message": "Token is missing"}), 401

            # You would need to decode the token and extract user information here
            # This is just a placeholder for actual token decoding
            username = decode_token_and_get_user_id(token)

            if not username:
                return jsonify({"message": "User not authenticated"}), 401

            # Fetch the user from the database
            user_collection = User()
            user = user_collection.find_user_by_username(username)[0]

            if not user:
                return jsonify({"message": "User not found"}), 401

            if user['role'] not in required_roles:
                return jsonify({
                    "message": "Access denied. Insufficient privileges."
                }), 403

            # Proceed to the route handler
            return f(*args, **kwargs)

        return decorated_function

    return decorator

# def decode_token_and_get_user_id(token):
#     try:
#         # Decode the JWT token using the secret key
#         decoded = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=current_app.config['JWT_ALGORITHM'])
#         # Return the user ID from the decoded token
#         print(decoded)
#         return decoded.get('username')
#     except jwt.ExpiredSignatureError:
#         # Token has expired
#         return None
#     except jwt.InvalidTokenError:
#         # Invalid token
#         return None
