from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from models.user_model import create_user, find_user_by_email, verify_password
from utils.jwt_utils import generate_token
from utils.auth_middleware import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username') 
    password = data.get('password')
    
    db = current_app.config['DB']
    if find_user_by_email(db, email):
        return jsonify({'message': 'El usuario ya existe'}), 400

    user = create_user(db, email, username, password)
    return jsonify({'message': 'Usuario registrado con éxito', 'email': user['email']}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    db = current_app.config['DB']
    user = find_user_by_email(db, email)
    
    if not user or not verify_password(user['password'], password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = generate_token(user['_id'], current_app.config['JWT_SECRET'])
    return jsonify({'token': token, 'email': user['email']}), 200

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(user_id):
    return jsonify({'message': f'Acceso permitido. Tu ID es {user_id}'}), 200