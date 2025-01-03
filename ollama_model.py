import configparser
from gpt_model import GPTModel
import ollama

CONFIG_FILE = 'config.properties'
CONFIG_SECTION = 'Ollama'
TEMPERATURE_KEY = 'temperature'
MAX_TOKENS_KEY = 'max_tokens'
MODEL_NAME_KEY = 'model_name'
INITIAL_INSTRUCTIONS_KEY = 'initial_instructions'


def load_config(filename: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        with open(filename, 'r') as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file '{filename}' was not found.")
    return config


config = load_config(CONFIG_FILE)


class OllamaModel(GPTModel):
    def __init__(self, model: str, role: str):
        self.provider = "OLlama"
        self.role = role
        self.temperature = config.get(CONFIG_SECTION, TEMPERATURE_KEY)
        self.max_tokens = config.get(CONFIG_SECTION, MAX_TOKENS_KEY)
        self.history = []
        self.model = model if model else config.get(CONFIG_SECTION, MODEL_NAME_KEY)
        self.initial_instructions = config.get(CONFIG_SECTION, INITIAL_INSTRUCTIONS_KEY)
        self.history.append({"role": "system", "content": self.initial_instructions})

    def generate_response(self, prompt: str, use_history: bool = True) -> str:
        chat_input = self._prepare_chat_input(prompt, use_history)
        return self._fetch_response(chat_input, use_history)

    def _prepare_chat_input(self, prompt: str, use_history: bool) -> list:
        if use_history:
            self.history.append({'role': self.role, 'content': prompt})
            return self.history
        return [{'role': self.role, 'content': prompt}]

    def _fetch_response(self, chat_input: list, use_history: bool) -> str:
        try:
            response = ollama.chat(model=self.model, messages=chat_input)
        except Exception as e:
            return f"Model error: {e}"
        response_content = response['message']['content']
        if use_history:
            self.history.append({'role': self.role, 'content': response_content})
        return response_content

    def get_provider(self) -> str:
        return self.provider

    def get_model(self) -> str:
        return self.model

    def get_prompt(self) -> str:
        return self.history[-1]['content'] if self.history else ''

    def get_provider_model(self) -> str:
        return f"{self.provider}/{self.model}"


if __name__ == "__main__":
    models = ["llama2-uncensored:latest", "gemma2:2b", "phi3.5:latest"]
    prompts = ["Hello!"]
    for model in models:
        chat_model = OllamaModel(model, "assistant")
        for prompt in prompts:
            response = chat_model.generate_response(prompt, use_history=False)
            print(f"{chat_model.get_provider_model()} {prompt}\n{response}\n")