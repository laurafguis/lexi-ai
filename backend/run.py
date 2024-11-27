from flask import Flask
from app.controllers.file_controller import file_bp
from app.controllers.chat_controller import chat_bp  # Si tienes el chat
import os

class Config:
    # Cambiar el directorio de uploads para que esté dentro de `app/uploads`
    UPLOADS_DIR = os.getenv("UPLOADS_DIR", os.path.join(os.path.dirname(__file__), "app", "uploads"))
    DEBUG = os.getenv("DEBUG", True)

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Crear el directorio de subida si no existe
def create_uploads_dir():
    if not os.path.exists(app.config["UPLOADS_DIR"]):
        os.makedirs(app.config["UPLOADS_DIR"])

create_uploads_dir()

# Registrar blueprints
app.register_blueprint(file_bp)
app.register_blueprint(chat_bp)  # Si es necesario

# Ruta base de prueba
@app.route("/", methods=["GET"])
def home():
    return {"message": "Bienvenido a la API de Gestión de Archivos y Chat con IA"}

# Manejadores de errores globales
@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint no encontrado"}, 404

@app.errorhandler(500)
def server_error(error):
    return {"error": "Error interno del servidor"}, 500

# Ejecutar la aplicación
if __name__ == "__main__":
    debug = app.config.get("DEBUG", False)
    app.run(debug=debug, host="0.0.0.0", port=5000)
