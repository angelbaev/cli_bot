from google import genai
import os

class GeminiBot:
    def __init__(self, api_key, model_version):
        self.api_key = api_key
        self.model_version = model_version

        try:
            self.client = genai.Client(api_key=self.api_key)  # Moved inside __init__
            self.chat = self.client.chats.create(model=self.model_version or "gemini-2.0-flash")  # Moved inside __init__
            print(f"Gemini client initialized successfully (v{self.model_version or 'default'})")
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            self.client = None
            self.chat = None

    def get_response(self, user_input):
        if self.client is None or self.chat is None:
            return "Error: Gemini client not initialized. Check your API key and model."
        
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:

            return f"Error: {str(e)}"
