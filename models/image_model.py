from flask import current_app

def obtener_imagenes():
    db = current_app.config['DB']
    documentos = db.images.find()
    imagenes = []
    for doc in documentos:
        imagenes.append({
            "id": str(doc["_id"]),
            "fecha": doc.get("fecha"),
            "imagen_b64": doc.get("imagen_b64")
        })
    return imagenes
