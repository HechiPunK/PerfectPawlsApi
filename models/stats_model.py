from flask import current_app
from datetime import datetime
from collections import defaultdict

def contar_por_dia(nombre_coleccion):
    db = current_app.config['DB']
    coleccion = db[nombre_coleccion]
    conteo = defaultdict(int)
    for doc in coleccion.find():
        if "timestamp" in doc:
            fecha = doc["timestamp"]
            if isinstance(fecha, str):
                fecha = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            dia_str = fecha.strftime("%Y-%m-%d")
            conteo[dia_str] += 1
    resultado = [{"fecha": k, "conteo": v} for k, v in sorted(conteo.items())]
    return resultado
