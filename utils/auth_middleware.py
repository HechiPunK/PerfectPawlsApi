from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # El token debe estar en los headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Formato: Bearer <token>

        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(user_id, *args, **kwargs)
    return decorated