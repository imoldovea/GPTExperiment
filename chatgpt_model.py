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
    def __init__(self,model:str, role: str):
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

    def generate_response(self, prompt: str) -> str:
        self.prompt = prompt
        self.history.append({'role':self.role, 'content': prompt})
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=self.history,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            assistant_content = response.choices[0].message.content.strip()
            self.history.append({'role': 'assistant', 'content': assistant_content})
            return assistant_content
        except Exception as e:
            return f"A model error occurred: {e}"


    def get_provider(self) -> str:
        return self.provider

    def get_model(self) -> str:
        return self.model

    def get_provider_model(self) -> str:
        return self.provider + "/" + self.model + ": "
    def get_prompt(self) -> str:
        return self.prompt

# Example usage
if __name__ == "__main__":
    models = ["gpt-3.5-turbo", "gpt-4o-mini"]
    prompts = ["Hello!"]

    for model in models:
        chat_model = ChatGPTModel(model,"user")
        for prompt in prompts:
            response = chat_model.generate_response(prompt)
            print(f"Provider: {chat_model.get_provider()}\nModel: {chat_model.get_model()}\nPrompt: {prompt}\nResponse: {response}\n")
