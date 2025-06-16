from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import config

from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)

# Conexión con MongoDB
client = MongoClient(config.MONGO_URI)
db = client.get_database()

# Guardamos la BD en la app para que todos los módulos puedan accederla
app.config['DB'] = db
app.config['JWT_SECRET'] = config.JWT_SECRET

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    app.run(debug=True)