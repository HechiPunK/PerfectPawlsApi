from bson import ObjectId
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import current_app

def create_pet(db, name, species, breed, age, description, photo_file, available, user_id):
    # Validar campos obligatorios
    if not name or not isinstance(name, str) or name.strip() == "":
        raise ValueError("El nombre es obligatorio y debe ser texto válido")
    if not species or not isinstance(species, str) or species.strip() == "":
        raise ValueError("La especie es obligatoria y debe ser texto válido")
    
    fs = current_app.config['FS']
    
    if photo_file:
        filename = secure_filename(photo_file.filename)
        photo_id = fs.put(photo_file, filename=filename)
    else:
        photo_id = None

    pet = {
        "name": name.strip(),  # Elimina espacios en blanco
        "species": species.strip(),
        "breed": breed.strip() if breed else None,
        "age": int(age),
        "description": description.strip() if description else None,
        "photo_id": str(photo_id) if photo_id else None,
        "available": bool(available),
        "user_id": ObjectId(user_id),
        "created_at": datetime.utcnow()
    }
    result = db.pets.insert_one(pet)
    pet['_id'] = str(result.inserted_id)
    if 'photo_id' in pet:
        del pet['photo_id']
    return pet

def get_all_pets(db):
    return list(db.pets.find({"available": True}))

def get_pet_by_id(db, pet_id):
    pet = db.pets.find_one({"_id": ObjectId(pet_id)})
    if pet and 'photo_id' in pet:
        del pet['photo_id']
    return pet

def get_pets_by_user(db, user_id):
    pets = list(db.pets.find({"user_id": ObjectId(user_id)}))
    for pet in pets:
        if 'photo_id' in pet:
            del pet['photo_id']
    return pets

def update_pet(db, pet_id, update_data):
    if 'photo_file' in update_data:
        photo_file = update_data.pop('photo_file')
        fs = current_app.config['FS']
        filename = secure_filename(photo_file.filename)
        photo_id = fs.put(photo_file, filename=filename)
        update_data['photo_id'] = str(photo_id)
    db.pets.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": update_data}
    )
    pet = db.pets.find_one({"_id": ObjectId(pet_id)})
    if pet and 'photo_id' in pet:
        del pet['photo_id']
    return pet

def delete_pet(db, pet_id):
    pet = db.pets.find_one_and_delete({"_id": ObjectId(pet_id)})
    if pet and 'photo_id' in pet:
        fs = current_app.config['FS']
        fs.delete(ObjectId(pet['photo_id']))
        del pet['photo_id']
    return pet