import configparser
from gpt_model import GPTModel
import ollama


def load_config(filename: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        with open(filename, 'r') as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file '{filename}' was not found.")
    return config


config = load_config('config.properties')


class OllamaModel(GPTModel):
    def __init__(self, model: str, role: str):
        self.provider = "OLlama"
        self.role = role
        self.temperature = config.get('Ollama', 'temperature')
        self.max_tokens = config.get('Ollama', 'max_tokens')
        self.history = []
        self.model = model or config.get('Ollama', 'model_name')
        self.initial_instructions = config.get('Ollama', 'initial_instructions')
        self.history.append({"role": "system", "content": self.initial_instructions})

    def generate_response(self, prompt: str, use_history: bool = True) -> str:
        if use_history:
            self.history.append({'role': self.role, 'content': prompt})
            chat_input = self.history
        else:
            chat_input = [{'role': self.role, 'content': prompt}]

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
        return f"{self.provider}/{self.model} "


if __name__ == "__main__":
    models = ["llama2-uncensored:latest", "gemma2:2b", "phi3.5:latest"]
    prompts = ["Hello!"]
    for model in models:
        chat_model = OllamaModel(model, "assistant")
        for prompt in prompts:
            response = chat_model.generate_response(prompt, use_history=False)
            print(f"{chat_model.get_provider_model()} {prompt}\n{response}\n")