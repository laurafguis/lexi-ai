from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint para interactuar con el modelo de chat.
    Entrada:
    - JSON con las claves 'message' (obligatorio) y 'target_language' (opcional).

    Retorna:
    - Respuesta generada por el modelo o traducción del mensaje.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No se encontró ningún mensaje en la solicitud."}), 400

    user_message = data["message"]
    target_language = data.get("target_language")  # Idioma opcional

    try:
        if target_language:
            # Traducir mensaje en lugar de interactuar
            translation = ChatService.translate_text(user_message, target_language)
            return jsonify({"translated_content": translation}), 200
        else:
            # Respuesta normal del modelo
            response = ChatService.interact_with_model(user_message)
            return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500
