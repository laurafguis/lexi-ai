import unittest
from app.services.chat_service import ChatService

class TestChatService(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        """
        self.chat_service = ChatService()

    def test_send_message_valid(self):
        """
        Verifica que un mensaje válido se procese correctamente.
        """
        response = self.chat_service.send_message("Hola, ¿cómo estás?")
        self.assertEqual(response["status"], "success")
        self.assertIn("response", response)

    def test_send_message_empty(self):
        """
        Verifica que un mensaje vacío sea rechazado.
        """
        response = self.chat_service.send_message("")
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "El mensaje no puede estar vacío.")

    def test_send_message_special_characters(self):
        """
        Verifica que un mensaje con caracteres especiales sea aceptado.
        """
        response = self.chat_service.send_message("¿Cuál es el valor de π?")
        self.assertEqual(response["status"], "success")
        self.assertIn("response", response)

    def test_message_history(self):
        """
        Verifica que el historial de mensajes se almacene correctamente.
        """
        self.chat_service.send_message("Hola")
        self.chat_service.send_message("¿Cómo estás?")
        history = self.chat_service.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["message"], "Hola")
        self.assertEqual(history[1]["message"], "¿Cómo estás?")

if __name__ == "__main__":
    unittest.main()
