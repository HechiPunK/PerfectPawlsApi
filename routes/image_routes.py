from flask import Blueprint, jsonify
from models.image_model import obtener_imagenes

image_bp = Blueprint('image', __name__)

@image_bp.route('/imagenes', methods=['GET'])
def imagenes():
    imagenes = obtener_imagenes()
    return jsonify(imagenes)
