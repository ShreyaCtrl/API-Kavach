# from functools import wraps
# from flask import request, jsonify
# from .before_request import decode_token_and_get_user_id
# from models.user import User
#
# # Define roles and their access to API stages
# role_access = {
#     'Developer': ['Development', 'Testing'],
#     'Tester': ['Testing'],
#     'DevOps Engineer': ['Development', 'Testing', 'Staging', 'Production'],
#     'Administrator': ['Development', 'Testing', 'Staging', 'Production']
# }
#
# def api_access(required_stage=None):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             # Get the token from headers
#             token = request.headers.get('Authorization')
#
#             if not token:
#                 return jsonify({"message": "Token is missing"}), 401
#
#             # Decode the token and extract user information
#             username = decode_token_and_get_user_id(token)
#
#             if not username:
#                 return jsonify({"message": "User not authenticated"}), 401
#
#             # Fetch the user from the database
#             user_collection = User()
#             user = user_collection.find_user_by_username(username)[0]
#
#             if not user:
#                 return jsonify({"message": "User not found"}), 401
#
#             # Check if the user's role has access to the required stage
#             user_role = user['role']
#             user_stages = role_access.get(user_role, [])
#
#             # If a specific stage is required, check access
#             if required_stage and required_stage not in user_stages:
#                 return jsonify({"message": f"Access denied: Unauthorized for stage {required_stage}"}), 403
#
#             # Otherwise, grant access
#             return f(current_user=user, *args, **kwargs)
#
#         return decorated_function
#
#     return decorator

# from functools import wraps
# from flask import request, jsonify
# from .before_request import decode_token_and_get_user_id
# from models.user import User
#
# # Define roles and their access to API stages
# role_access = {
#     'Developer': ['Development', 'Testing'],
#     'Tester': ['Testing'],
#     'DevOps Engineer': ['Development', 'Testing', 'Staging', 'Production'],
#     'Administrator': ['Development', 'Testing', 'Staging', 'Production']
# }
#
# def api_access(required_stage=None):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             # Get the token from headers
#             token = request.headers.get('Authorization')
#
#             if not token:
#                 return jsonify({"message": "Token is missing"}), 401
#             print(token)
#
#             # Decode the token and extract user information
#             username = decode_token_and_get_user_id(token)
#
#             if not username:
#                 return jsonify({"message": "User not authenticated"}), 401
#
#             # Fetch the user from the database
#             user_collection = User()
#             user = user_collection.find_user_by_username(username)[0]
#
#             if not user:
#                 return jsonify({"message": "User not found"}), 401
#
#             # Check if the user's role has access to the required stage
#             user_role = user['role']
#             user_stages = role_access.get(user_role, [])
#
#             # If a specific stage is required, check access
#             if required_stage and required_stage not in user_stages:
#                 return jsonify({"message": f"Access denied: Unauthorized for stage {required_stage}"}), 403
#
#             # Pass the user information as a keyword argument
#             return f(current_user=user, *args, **kwargs)
#
#         return decorated_function
#
#     return decorator

from functools import wraps
from flask import request, jsonify, g
from .before_request import decode_token_and_get_user_id
from models.user import User

# Define roles and their access to API stages
role_access = {
    'Developer': ['Development', 'Testing'],
    'Tester': ['Testing'],
    'DevOps Engineer': ['Development', 'Testing', 'Staging', 'Production'],
    'Administrator': ['Development', 'Testing', 'Staging', 'Production']
}

def api_access(required_stage=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the token from headers
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({"message": "Token is missing"}), 401

            # Decode the token and extract user information
            username = decode_token_and_get_user_id(token)

            if not username:
                return jsonify({"message": "User not authenticated"}), 401

            # Fetch the user from the database
            user_collection = User()
            user = user_collection.find_user_by_username(username)[0]

            if not user:
                return jsonify({"message": "User not found"}), 401

            # Check if the user's role has access to the required stage
            user_role = user['role']
            user_stages = role_access.get(user_role, [])

            # If a specific stage is required, check access
            if required_stage and required_stage not in user_stages:
                return jsonify({"message": f"Access denied: Unauthorized for stage {required_stage}"}), 403

            # Store current_user in Flask's g object
            # g.current_user = user

            # Pass the current_user as a keyword argument
            return f(current_user=user, *args, **kwargs)

        return decorated_function

    return decorator