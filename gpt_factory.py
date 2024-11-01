from chatgpt_model import ChatGPTModel
from ollama_model import OllamaModel
from gpt_model import GPTModel

# Step 4: Create a Factory for Generating GPT Models
class GPTFactory:
    @staticmethod
    def create_gpt_model(provider: str, model:str, role:str) -> GPTModel:
        if provider == "ChatGPT":
            return ChatGPTModel(model,role)
        elif provider == "Ollama":
            return OllamaModel(model,role)
        else:
            raise ValueError(f"Unknown provider: {provider}")