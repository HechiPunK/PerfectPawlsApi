from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import config

# Importación de Blueprints para las rutas principales de la API
from routes.auth_routes import auth_bp
from routes.chatbot_routes import chatbot_bp
from routes.image_routes import image_bp

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir peticiones desde otros orígenes

# Conexión con MongoDB usando la URI definida en config.py
client = MongoClient(config.MONGO_URI)
db = client.get_database()  # Obtiene la base de datos por defecto de la URI
app.config['DB'] = db  # Guarda la instancia de la base de datos en la configuración de la app
app.config['JWT_SECRET'] = config.JWT_SECRET  # Guarda el secreto JWT en la configuración

# Registro de Blueprints para organizar las rutas de la API
app.register_blueprint(auth_bp, url_prefix='/api/auth')      # Rutas de autenticación
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot') # Rutas del chatbot
app.register_blueprint(image_bp, url_prefix='/api')           # Rutas de imágenes

# Inicializa la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)