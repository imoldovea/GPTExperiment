import configparser
from gpt_factory import GPTFactory

# Load configuration
config = configparser.ConfigParser()

# Check if the configuration file exists and read it
try:
    with open('config.properties', 'r') as config_file:
        config.read_file(config_file)
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config.properties' was not found.")

def print_dialog(provider_model: str, response: str, sequence_number: int):
    print(f"[94m{provider_model} [{sequence_number}][0m {response}")

def generate_and_print_response(model, prompt, sequence_number):
    response = model.generate_response(prompt)
    print_dialog(model.get_provider_model(), response, sequence_number)
    return response

def create_dialog_models():
    """
    Factory method to create the two models involved in the dialog.
    Modify provider and model values to use different combinations as needed.
    """
    llm1 = GPTFactory.create_gpt_model("Ollama", "llama3.2:3b","user")
    llm2 = GPTFactory.create_gpt_model("ChatGPT", "gpt-4-turbo", "assistant")
    #llm2 = GPTFactory.create_gpt_model("ChatGPT", "gpt-3.5-turbo", "assistant")
    #llm2 = GPTFactory.create_gpt_model("Ollama", "llama3.2:3b ", "assistant")

    return llm1, llm2

def main():
    llm1, llm2 = create_dialog_models()

    initial_prompt = config.get('Prompt', 'initial_prompt')
    print_dialog(llm1.get_provider_model(), initial_prompt, 1)

    llm2_response = generate_and_print_response(llm2, initial_prompt, 1)

    for i in range(2):
        llm1_response = generate_and_print_response(llm1, llm2_response, i+2)
        llm2_response = generate_and_print_response(llm2, llm1_response, i+2)

def test():
    # Create a ChatGPT model instance
    chat_gpt3_5 = GPTFactory.create_gpt_model("ChatGPT", "gpt-3.5-turbo")
    generate_and_print_response(chat_gpt3_5, "Hello", 1)

    # Create an Ollama model instance
    ollama_uncensord = GPTFactory.create_gpt_model("Ollama","llama2-uncensored")
    generate_and_print_response(ollama_uncensord, "Hello", 2)

if __name__ == "__main__":
    main()
