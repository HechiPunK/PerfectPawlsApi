from flask import Blueprint, request, jsonify
from models.chatbot_model import buscar_respuesta_chatbot

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    consulta = data.get('consulta', '')
    resultados = buscar_respuesta_chatbot(consulta)

    if not resultados:
        return jsonify({'respuestas': ["Lo siento, no encontré información sobre ese tema. Prueba con otra consulta relacionada."]})

    respuestas = [r['respuesta'] for r in resultados]
    return jsonify({'respuestas': respuestas})