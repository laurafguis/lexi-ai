import ollama

class ChatService:
    """
    Servicio para manejar la lógica del chat con Ollama.
    """

    # Configuración del cliente Ollama
    cliente = ollama.Client()

    @staticmethod
    def interact_with_model(message):
        """
        Envía un mensaje al modelo y obtiene la respuesta.

        Parámetros:
        - message (str): Mensaje enviado por el usuario.

        Retorna:
        - response (str): Respuesta generada por el modelo o mensaje de error.
        """
        try:
            if not ChatService.cliente:
                raise RuntimeError("El cliente de Ollama no está configurado.")

            response = ChatService.cliente.run(model="llama3.1:latest", prompt=message)
            return response.get("response", "Error: No se recibió una respuesta válida del modelo.")
        except RuntimeError as e:
            return f"Error de configuración: {str(e)}"
        except Exception as e:
            return f"Error al interactuar con Ollama: {str(e)}"

    @staticmethod
    def translate_text(content, target_language):
        """
        Traduce un texto usando Ollama.

        Parámetros:
        - content (str): Texto a traducir.
        - target_language (str): Idioma de destino.

        Retorna:
        - translated_content (str): Texto traducido o error.
        """
        try:
            if not ChatService.cliente:
                raise RuntimeError("El cliente de Ollama no está configurado.")

            response = ChatService.cliente.generate(
                model="llama3.1:latest",
                prompt=f"Traducir al {target_language}: {content}"
            )
            return response.get("response", "Error: No se pudo traducir el contenido.")
        except RuntimeError as e:
            return f"Error de configuración: {str(e)}"
        except Exception as e:
            return f"Error al traducir con Ollama: {str(e)}"
