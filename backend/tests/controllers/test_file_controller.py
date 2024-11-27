import unittest
import os
from app.services.file_service import FileService

class TestFileService(unittest.TestCase):
    """
    Clase para probar las funcionalidades del servicio de archivos utilizando TDD.
    """

    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        Crea un directorio temporal para los tests.
        """
        # Usar un directorio de pruebas separado para evitar conflictos
        FileService.uploads_dir = "test_uploads"
        if not os.path.exists(FileService.uploads_dir):
            os.makedirs(FileService.uploads_dir)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        Elimina los archivos generados durante las pruebas.
        """
        for file in os.listdir(FileService.uploads_dir):
            file_path = os.path.join(FileService.uploads_dir, file)
            os.remove(file_path)
        os.rmdir(FileService.uploads_dir)

    def test_validate_file_valid(self):
        """
        Verifica que un archivo válido pase la validación.
        Este test asegura que el sistema acepta correctamente archivos válidos.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        is_valid, message = FileService.validate_file(file)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Archivo válido.")

    def test_validate_file_empty(self):
        """
        Verifica que un archivo vacío sea rechazado.
        Este test asegura que los archivos vacíos no se acepten.
        """
        file = {"filename": "empty_file.txt", "content": ""}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo está vacío.")

    def test_validate_file_too_large(self):
        """
        Verifica que un archivo con más de 1000 caracteres sea rechazado.
        Este test evalúa la validación del tamaño máximo permitido.
        """
        file = {"filename": "large_file.txt", "content": "A" * 1001}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo supera el tamaño permitido de 1000 caracteres.")

    def test_validate_file_invalid_extension(self):
        """
        Verifica que solo se admitan archivos con extensión .txt.
        Este test asegura que el sistema no acepte extensiones no válidas.
        """
        file = {"filename": "invalid_file.pdf", "content": "Contenido válido."}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo debe tener la extensión .txt.")

    def test_save_file_valid(self):
        """
        Verifica que un archivo válido se guarde correctamente.
        Este test asegura que los archivos se almacenan en el directorio definido.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        file_path = FileService.save_file(file)
        self.assertTrue(os.path.exists(file_path))

    def test_get_uploaded_files(self):
        """
        Verifica que los archivos subidos se recuperen correctamente.
        Este test valida la funcionalidad de listar archivos almacenados.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        FileService.save_file(file)
        uploaded_files = FileService.get_uploaded_files()
        self.assertIn("valid_file.txt", uploaded_files)

    def test_summarize_file(self):
        """
        Verifica que se genere un resumen en un archivo separado.
        Este test evalúa la funcionalidad de resumir contenido de archivos.
        """
        file = {"filename": "summary_file.txt", "content": "Este es un archivo de prueba con contenido para resumir."}
        file_path = FileService.save_file(file)
        summary_path = FileService.summarize_file(file_path)
        self.assertTrue(os.path.exists(summary_path))

        with open(summary_path, "r", encoding="utf-8") as f:
            summary_content = f.read()

        self.assertIn("Resumen:", summary_content)
        self.assertIn(file["content"][:100], summary_content)

def test_translate_file(self):
    """
    Verifica que se genere una traducción en un archivo separado.
    """
    # Crear archivo de prueba
    file = {"filename": "translate_file.txt", "content": "This is a test file for translation."}
    file_path = FileService.save_file(file)

    # Llamar al método de traducción
    result = FileService.translate_file(file_path, target_language="es")

    # Verificar que el archivo traducido existe
    self.assertTrue(os.path.exists(result["translated_file_path"]))

    # Verificar el contenido del archivo traducido
    with open(result["translated_file_path"], "r", encoding="utf-8") as f:
        translated_content = f.read()

    self.assertIn("Traducción al es:", translated_content)
    self.assertIn(file["content"], translated_content)


if __name__ == "__main__":
    unittest.main()
