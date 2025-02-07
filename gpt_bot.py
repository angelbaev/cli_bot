import openai

class GptBot:
    def __init__(self, api_key, model_version):
        self.api_key = api_key
        self.model_version = model_version

        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.history = []
            print(f"Gpt client initialized successfully (v{self.model_version or 'gpt-4'})")
        except Exception as e:
            print(f"Error initializing Gpt client: {e}")
            self.client = None
            self.chat = None        

    def get_response(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=self.model_version,
                messages=self.history
            )
            reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})
            
            return reply
        except Exception as e:

            return f"Error: {str(e)}"
