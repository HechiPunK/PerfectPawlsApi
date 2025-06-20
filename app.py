from flask import Flask
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
from gridfs import GridFS
from flask.json.provider import JSONProvider  # <-- Cambio importante
import json
import config

# Clase personalizada para manejar la serialización
class MongoJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self.default, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

from routes.auth_routes import auth_bp
from routes.catalog_routes import catalog_bp

app = Flask(__name__)
app.json = MongoJSONProvider(app) 
CORS(app)

# Conexión con MongoDB
client = MongoClient(config.MONGO_URI)
db = client.get_database()

# Configuración de GridFS para almacenar archivos
fs = GridFS(db)

# Guardamos la BD en la app para que todos los módulos puedan accederla
app.config['DB'] = db
app.config['FS'] = fs
app.config['JWT_SECRET'] = config.JWT_SECRET

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(catalog_bp, url_prefix='/api/catalog')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)