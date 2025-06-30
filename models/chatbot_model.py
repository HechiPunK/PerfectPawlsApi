from flask import current_app

def buscar_respuesta_chatbot(consulta):
    db = current_app.config['DB']
    coleccion = db['chatbotdata']
    consulta = consulta.lower()
    resultados = []

    documentos = coleccion.find({})
    for doc in documentos:
        for keyword in doc.get('keywords', []):
            if keyword in consulta:
                resultados.append({
                    'titulo': doc.get('titulo', ''),
                    'respuesta': doc.get('respuesta', '')
                })
                break  # Evitar duplicados
            
    return resultados