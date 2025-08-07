from flask import Blueprint, jsonify
from models.stats_model import contar_por_dia

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/rfid', methods=['GET'])
def stats_rfid():
    return jsonify(contar_por_dia("rfid_events"))

@stats_bp.route('/stats/poca_comida', methods=['GET'])
def stats_poca_comida():
    return jsonify(contar_por_dia("ultrasonic_events"))
