from flask import request, jsonify, current_app
import jwt

def token_required(f):
    """Decorator to protect routes requiring authentication"""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'],
                              algorithms=[current_app.config['JWT_ALGORITHM']])
            current_user = data['username']
        except Exception as e:
            return jsonify({"message": "Invalid or expired token!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated