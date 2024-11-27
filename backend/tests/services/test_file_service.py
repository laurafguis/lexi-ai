import unittest
import os
from app.services.file_service import FileService

class TestFileService(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        """
        # Usar un directorio de pruebas separado
        FileService.uploads_dir = "test_uploads"
        if not os.path.exists(FileService.uploads_dir):
            os.makedirs(FileService.uploads_dir)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar todos los archivos en el directorio de pruebas
        for file in os.listdir(FileService.uploads_dir):
            file_path = os.path.join(FileService.uploads_dir, file)
            os.remove(file_path)
        os.rmdir(FileService.uploads_dir)

    def test_validate_file_valid(self):
        """
        Verifica que un archivo válido pase la validación.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        is_valid, message = FileService.validate_file(file)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Archivo válido.")

    def test_validate_file_empty(self):
        """
        Verifica que un archivo vacío sea rechazado.
        """
        file = {"filename": "empty_file.txt", "content": ""}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo está vacío.")

    def test_validate_file_too_large(self):
        """
        Verifica que un archivo con más de 1000 caracteres sea rechazado.
        """
        file = {"filename": "large_file.txt", "content": "A" * 1001}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo supera el tamaño permitido de 1000 caracteres.")

    def test_validate_file_invalid_extension(self):
        """
        Verifica que solo se admitan archivos con extensión .txt.
        """
        file = {"filename": "invalid_file.pdf", "content": "Contenido válido."}
        is_valid, message = FileService.validate_file(file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "El archivo debe tener la extensión .txt.")

    def test_save_file_valid(self):
        """
        Verifica que un archivo válido se guarde correctamente en el directorio 'uploads/'.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        file_path = FileService.save_file(file)
        self.assertTrue(os.path.exists(file_path))

    def test_get_uploaded_files(self):
        """
        Verifica que los archivos subidos se recuperen correctamente.
        """
        file = {"filename": "valid_file.txt", "content": "Contenido válido."}
        FileService.save_file(file)
        uploaded_files = FileService.get_uploaded_files()
        self.assertIn("valid_file.txt", uploaded_files)

    def test_summarize_file(self):
        """
        Verifica que se genere un resumen del contenido del archivo.
        """
        file = {"filename": "summary_file.txt", "content": "Este es un archivo de prueba con contenido para resumir."}
        file_path = FileService.save_file(file)
        summary = FileService.summarize_file(file_path)
        self.assertIn("Resumen del archivo:", summary)
        self.assertIn(file["content"][:100], summary)

    def test_translate_file(self):
        """
        Verifica que se genere una traducción simulada del contenido del archivo.
        """
        file = {"filename": "translate_file.txt", "content": "Este es un contenido para traducir."}
        file_path = FileService.save_file(file)
        translation = FileService.translate_file(file_path, target_language="en")
        self.assertIn("Traducción al en:", translation)
        self.assertIn(file["content"], translation)

if __name__ == "__main__":
    unittest.main()

