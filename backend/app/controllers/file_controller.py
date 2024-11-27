from flask import Blueprint, request, jsonify
from app.services.file_service import FileService
import os

file_bp = Blueprint("file", __name__)

@file_bp.route("/file/upload", methods=["POST"])
def upload_file():
    """
    Endpoint para subir un archivo.
    """
    if "file" not in request.files:
        return jsonify({"error": "No se encontró ningún archivo en la solicitud."}), 400

    uploaded_file = request.files["file"]
    if not uploaded_file.filename:
        return jsonify({"error": "El archivo no tiene un nombre válido."}), 400

    try:
        file_data = {
            "filename": uploaded_file.filename,
            "content": uploaded_file.read().decode("utf-8")
        }
    except UnicodeDecodeError:
        return jsonify({"error": "El contenido del archivo no es válido o está corrupto."}), 400

    is_valid, message = FileService.validate_file(file_data)
    if not is_valid:
        return jsonify({"error": message}), 400

    try:
        file_path = FileService.save_file(file_data)
        return jsonify({
            "message": "Archivo guardado correctamente.",
            "file_path": file_path
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al guardar el archivo: {str(e)}"}), 500

@file_bp.route("/file/summary", methods=["POST"])
def summarize_file():
    """
    Endpoint para generar un resumen de un archivo.
    """
    # Verificar si se recibe un archivo o un nombre de archivo
    if "file" in request.files:
        # Modo: Enviar un archivo nuevo
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"error": "El archivo no tiene un nombre válido."}), 400

        try:
            file_data = {
                "filename": uploaded_file.filename,
                "content": uploaded_file.read().decode("utf-8")
            }
        except UnicodeDecodeError:
            return jsonify({"error": "El contenido del archivo no es válido o está corrupto."}), 400

        is_valid, message = FileService.validate_file(file_data)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Guardar el archivo temporalmente para procesarlo
        file_path = FileService.save_file(file_data)

    elif request.json and "filename" in request.json:
        # Modo: Usar un archivo ya existente en el servidor
        file_path = FileService.get_file_path(request.json["filename"])
        if not os.path.exists(file_path):
            return jsonify({"error": "El archivo no existe."}), 404

    else:
        return jsonify({"error": "No se proporcionó archivo ni nombre de archivo."}), 400

    # Generar el resumen
    try:
        summary = FileService.summarize_file(file_path)
        return jsonify({
            "message": "Resumen generado con éxito.",
            "summary": summary
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al generar el resumen: {str(e)}"}), 500


@file_bp.route("/file/translate", methods=["POST"])
def translate_file():
    """
    Endpoint para traducir el contenido de un archivo cargado.
    """
    if "file" in request.files:
        # Modo: Enviar un archivo nuevo
        uploaded_file = request.files["file"]
        target_language = request.form.get("target_language", "inglés")  # Idioma predeterminado

        if not uploaded_file.filename:
            return jsonify({"error": "El archivo no tiene un nombre válido."}), 400

        try:
            file_data = {
                "filename": uploaded_file.filename,
                "content": uploaded_file.read().decode("utf-8")
            }
        except UnicodeDecodeError:
            return jsonify({"error": "El contenido del archivo no es válido o está corrupto."}), 400

        is_valid, message = FileService.validate_file(file_data)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Guardar el archivo y traducir
        try:
            file_path = FileService.save_file(file_data)
            result = FileService.translate_file(file_path, target_language)
            return jsonify({
                "message": "Traducción realizada con éxito.",
                "translated_file_path": result["translated_file_path"],
                "translated_content": result["translated_content"]
            }), 200
        except Exception as e:
            return jsonify({"error": f"Error al traducir el archivo: {str(e)}"}), 500

    elif request.json and "filename" in request.json and "target_language" in request.json:
        # Modo: Traducir un archivo existente
        file_path = FileService.get_file_path(request.json["filename"])
        target_language = request.json["target_language"]

        if not os.path.exists(file_path):
            return jsonify({"error": "El archivo no existe."}), 404

        try:
            result = FileService.translate_file(file_path, target_language)
            return jsonify({
                "message": "Traducción realizada con éxito.",
                "translated_file_path": result["translated_file_path"],
                "translated_content": result["translated_content"]
            }), 200
        except Exception as e:
            return jsonify({"error": f"Error al traducir el archivo: {str(e)}"}), 500

    return jsonify({"error": "No se proporcionó archivo ni datos necesarios."}), 400


@file_bp.route("/chat/translate", methods=["POST"])
def translate_text():
    """
    Endpoint para traducir texto directamente desde el chat.
    """
    data = request.get_json()
    if not data or "content" not in data or "target_language" not in data:
        return jsonify({"error": "Faltan campos 'content' o 'target_language'."}), 400

    content = data["content"]
    target_language = data["target_language"]

    try:
        translation = FileService.translate_text(content, target_language)
        return jsonify({
            "message": "Traducción realizada con éxito.",
            "translated_content": translation
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al traducir el texto: {str(e)}"}), 500
