import configparser
from gpt_model import GPTModel
import ollama

# Load configuration
config = configparser.ConfigParser()
# Check if the configuration file exists and read it
try:
    with open('config.properties', 'r') as config_file:
        config.read_file(config_file)
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config.properties' was not found.")


# Step 3: Implement the Ollama Model
class OllamaModel(GPTModel):
    def __init__(self, model: str, role: str):
        self.provider = "OLlama"
        self.role=role
        self.temperature = config.get('Ollama', 'temperature')
        self.max_tokens = config.get('Ollama', 'max_tokens')
        self.history=[]
        self.model = model if model else config.get('Ollama', 'model_name')
        self.initial_instructions = config.get('Ollama', 'initial_instructions')
        self.history.append({"role": "system", "content": self.initial_instructions})

    def generate_response(self, prompt: str) -> str:
        self.prompt = prompt
        self.history.append({'role': self.role, 'content': prompt})
        try:
            response = ollama.chat(model=self.model, messages=self.history, max_tokens=self.max_tokens, temperature=self.temperature)
        except Exception as e:
            return f"A model error occurred: {e}"
        self.history.append({'role': self.role, 'content': response['message']['content']})
        return response['message']['content']

    def generate_response_old(self, prompt: str) -> str:
        self.prompt = prompt
        self.history.append({'role': 'user', 'content': prompt})
        response = ollama.chat(model=self.model, messages=self.history)
        return response['message']['content']

    def get_provider(self) -> str:
        return self.provider

    def get_model(self) -> str:
        return self.model

    def get_prompt(self) -> str:
        return self.prompt

    def get_provider_model(self) -> str:
        return self.provider + "/" + self.model + ": "

# Example usage
if __name__ == "__main__":
    models = ["llama2-uncensored", "llama3.2"]
    prompts = ["Hello!"]

    for model in models:
        chat_model = OllamaModel(model,"assistant")
        for prompt in prompts:
            response = chat_model.generate_response(prompt)
            print(f"Provider: {chat_model.get_provider()}\nModel: {chat_model.get_model()}\nPrompt: {prompt}\nResponse: {response}\n")
