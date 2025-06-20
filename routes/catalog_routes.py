from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from models.pets_model import create_pet, get_all_pets, get_pet_by_id, update_pet, delete_pet, get_pets_by_user
from utils.auth_middleware import token_required
import os

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/pets', methods=['GET'])
def list_pets():
    db = current_app.config['DB']
    pets = get_all_pets(db)
    
    # Convertir ObjectId a string y agregar URL de la foto si existe
    for pet in pets:
        pet['_id'] = str(pet['_id'])
        if 'photo_id' in pet and pet['photo_id']:
            pet['photo_url'] = f"/api/catalog/pets/{pet['_id']}/photo"
            del pet['photo_id']
        elif 'photo_id' in pet:
            del pet['photo_id']
    
    return jsonify(pets), 200

@catalog_bp.route('/pets', methods=['POST'])
@token_required
def add_pet(user_id):
    try:
        data = request.form
        photo_file = request.files.get('photo')
        
        # Validación básica en el endpoint
        if not data.get('name') or not data.get('species'):
            return jsonify({"error": "Nombre y especie son campos requeridos"}), 400
        
        pet = create_pet(
            db=current_app.config['DB'],
            name=data.get('name'),
            species=data.get('species'),
            breed=data.get('breed'),
            age=int(data.get('age')),
            description=data.get('description'),
            photo_file=photo_file,
            available=data.get('available', 'true').lower() == 'true',
            user_id=user_id
        )
        pet['_id'] = str(pet['_id'])
        if 'photo_id' in pet and pet['photo_id']:
            pet['photo_url'] = f"/api/catalog/pets/{pet['_id']}/photo"
            del pet['photo_id']
        elif 'photo_id' in pet:
            del pet['photo_id']
        return jsonify(pet), 201
        
    except ValueError as e:  # Captura errores de validación
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # Otros errores
        return jsonify({"error": "Error interno del servidor"}), 500

@catalog_bp.route('/pets/<pet_id>', methods=['PUT'])
@token_required
def edit_pet(user_id, pet_id):
    data = request.form
    photo_file = request.files.get('photo')
    
    update_data = {
        "name": data.get('name'),
        "species": data.get('species'),
        "breed": data.get('breed'),
        "age": int(data.get('age')),
        "description": data.get('description'),
        "available": data.get('available') == 'true'
    }
    
    if photo_file:
        update_data['photo_file'] = photo_file
    
    updated_pet = update_pet(
        db=current_app.config['DB'],
        pet_id=pet_id,
        update_data=update_data
    )
    
    if not updated_pet:
        return jsonify({"message": "Mascota no encontrada"}), 404
    
    updated_pet['_id'] = str(updated_pet['_id'])
    if 'photo_id' in updated_pet and updated_pet['photo_id']:
        updated_pet['photo_url'] = f"/api/catalog/pets/{pet_id}/photo"
        del updated_pet['photo_id']
    elif 'photo_id' in updated_pet:
        del updated_pet['photo_id']
    return jsonify(updated_pet), 200

@catalog_bp.route('/pets/<pet_id>', methods=['DELETE'])
@token_required
def remove_pet(user_id, pet_id):
    deleted_pet = delete_pet(
        db=current_app.config['DB'],
        pet_id=pet_id
    )
    
    if not deleted_pet:
        return jsonify({"message": "Mascota no encontrada"}), 404
    
    return jsonify({"message": "Mascota eliminada"}), 200

@catalog_bp.route('/user/pets', methods=['GET'])
@token_required
def user_pets(user_id):
    db = current_app.config['DB']
    pets = get_pets_by_user(db, user_id)
    
    for pet in pets:
        pet['_id'] = str(pet['_id'])
        if 'photo_id' in pet and pet['photo_id']:
            pet['photo_url'] = f"/api/catalog/pets/{pet['_id']}/photo"
            del pet['photo_id']
        elif 'photo_id' in pet:
            del pet['photo_id']
    
    return jsonify(pets), 200

@catalog_bp.route('/pets/<pet_id>/photo', methods=['GET'])
def get_pet_photo(pet_id):
    try:
        db = current_app.config['DB']
        fs = current_app.config['FS']
        
        pet = db.pets.find_one({"_id": ObjectId(pet_id)})
        if not pet or not pet.get("photo_id"):
            return jsonify({"error": "Foto no encontrada"}), 404
        
        # Obtener la imagen desde GridFS
        photo = fs.get(ObjectId(pet["photo_id"]))
        
        return current_app.response_class(
            photo.read(),
            mimetype='image/jpeg',  # Ajusta según el tipo de imagen (png, etc.)
            headers={'Content-Disposition': f'attachment; filename={photo.filename}'}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500