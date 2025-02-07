from openai import OpenAI

class DeepseekBot:
    def __init__(self, api_key, model_version):
        self.api_key = api_key
        self.model_version = model_version

        try:
            self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
            print(f"DeepSeek client initialized successfully(v: {self.model_version})")
        except Exception as e:
            print(f"Error initializing Gpt client: {e}")
            self.client = None

    def get_response(self, user_input):
        if self.client is None:
            return "Error: DeepSeek client not initialized. Check your API key and model."

        try:
            response = self.client.chat.completions.create(
                model=self.model_version,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": user_input},
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
