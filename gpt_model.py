from abc import ABC, abstractmethod

# Step 1: Define the GPT Interface
class GPTModel(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

    @abstractmethod
    def get_provider(self) -> str:
        pass

    @abstractmethod
    def get_model(self) -> str:
        pass

    @abstractmethod
    def get_provider_model(self) -> str:
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        pass