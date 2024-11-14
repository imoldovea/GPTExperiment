import configparser
import openai
from gpt_model import GPTModel

# Load configuration
config = configparser.ConfigParser()
# Check if the configuration file exists and read it
try:
    with open('config.properties', 'r') as config_file:
        config.read_file(config_file)
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config.properties' was not found.")


# Implement the ChatGPT Model
class ChatGPTModel(GPTModel):
    def __init__(self, model: str, role: str):
        self.provider = "OpenAI"
        self.role = role
        self.api_key = config.get('ChatGPT', 'api_key')
        self.model = model if model else config.get('ChatGPT', 'model_name')
        self.max_tokens = config.getint('ChatGPT', 'max_tokens')
        self.initial_instructions = config.get('Ollama', 'initial_instructions')
        self.temperature = config.getfloat('ChatGPT', 'temperature')
        self.history = []
        self.history.append({"role": "system", "content": self.initial_instructions})
        openai.api_key = self.api_key

    def generate_response(self, prompt: str, use_history: bool = True) -> str:
        if use_history:
            self.history.append({'role': self.role, 'content': prompt})
            chat_input = self.history
        else:
            chat_input = [{'role': self.role, 'content': prompt}]

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=chat_input,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            assistant_content = response.choices[0].message.content.strip()
            if use_history:
                self.history.append({'role': 'assistant', 'content': assistant_content})
            return assistant_content
        except Exception as e:
            return f"A model error occurred: {e}"

    def get_provider(self) -> str:
        return self.provider

    def get_model(self) -> str:
        return self.model

    def get_provider_model(self) -> str:
        return self.provider + "/" + self.model

    def get_prompt(self) -> str:
        return self.history[-1]['content'] if self.history else ''


# Example usage
if __name__ == "__main__":
    models = ["gpt-3.5-turbo", "gpt-4o-mini"]
    prompts = ["Hello!"]

    for model in models:
        chat_model = ChatGPTModel(model, "user")
        for prompt in prompts:
            response = chat_model.generate_response(prompt, use_history=False)
            print(
                f"Provider: {chat_model.get_provider()}\nModel: {chat_model.get_model()}\nPrompt: {prompt}\nResponse: {response}\n")