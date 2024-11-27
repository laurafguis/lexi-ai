import os
import logging
import ollama

logging.basicConfig(level=logging.INFO)

class FileService:
    """
    Servicio para gestionar la lógica de validación, almacenamiento y procesamiento de archivos.
    """

    # Directorio de almacenamiento relativo al proyecto
    uploads_dir = os.path.join("app", "uploads")

    # Instancia del cliente Ollama
    cliente = ollama.Client()

    @staticmethod
    def ensure_uploads_dir():
        """
        Asegura que el directorio de `uploads` exista.
        """
        os.makedirs(FileService.uploads_dir, exist_ok=True)

    @staticmethod
    def get_file_path(filename):
        """
        Obtiene la ruta completa de un archivo dentro del directorio de uploads.
        """
        return os.path.join(FileService.uploads_dir, filename)

    @staticmethod
    def validate_file(file):
        """
        Valida un archivo para verificar que cumple con las restricciones definidas.
        """
        if not file["filename"].endswith(".txt"):
            return False, "El archivo debe ser de tipo .txt."
        if len(file["content"]) > 1000:
            return False, "El archivo excede el límite de 1000 caracteres."
        if not file["content"]:
            return False, "El contenido del archivo está vacío."
        return True, "Archivo válido."

    @staticmethod
    def save_file(file):
        """
        Guarda un archivo en el sistema.
        """
        FileService.ensure_uploads_dir()
        file_path = FileService.get_file_path(file["filename"])
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file["content"])
            logging.info(f"Archivo guardado en: {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error al guardar el archivo: {str(e)}")
            raise

    @staticmethod
    def summarize_content(content):
        """
        Utiliza Ollama para resumir el contenido del archivo.
        """
        try:
            response = FileService.cliente.generate(
                model="llama3.1:latest",
                prompt=f"Resumir el siguiente contenido: {content}"
            )
            if "response" not in response:
                raise ValueError("Respuesta incompleta de Ollama.")
            return response["response"]
        except Exception as e:
            logging.error(f"Error al interactuar con Ollama: {str(e)}")
            return f"Error al interactuar con Ollama: {str(e)}"

    @staticmethod
    def summarize_file(file_path):
        """
        Genera un resumen del contenido de un archivo y lo guarda en un nuevo archivo.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        summary = FileService.summarize_content(content)
        summary_file_path = file_path.replace(".txt", ".summary.txt")
        with open(summary_file_path, "w", encoding="utf-8") as f:
            f.write(summary)
        logging.info(f"Resumen guardado en: {summary_file_path}")
        return {
            "summary_file_path": summary_file_path,
            "summary_content": summary
        }

    @staticmethod
    def translate_content(content, target_language):
        """
        Utiliza Ollama para traducir el contenido del archivo.
        """
        try:
            response = FileService.cliente.generate(
                model="llama3.1:latest",
                prompt=f"Traducir el siguiente contenido al {target_language}: {content}"
            )
            if "response" not in response:
                raise ValueError("Respuesta incompleta de Ollama.")
            return response["response"]
        except Exception as e:
            logging.error(f"Error al interactuar con Ollama: {str(e)}")
            return f"Error al interactuar con Ollama: {str(e)}"

    @staticmethod
    def translate_file(file_path, target_language):
        """
        Traduce el contenido de un archivo y lo guarda en un nuevo archivo.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        translation = FileService.translate_content(content, target_language)
        translated_file_path = file_path.replace(".txt", f".translated.{target_language}.txt")
        with open(translated_file_path, "w", encoding="utf-8") as f:
            f.write(translation)
        logging.info(f"Traducción guardada en: {translated_file_path}")
        return {
            "translated_file_path": translated_file_path,
            "translated_content": translation
        }

