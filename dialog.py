import configparser
from gpt_factory import GPTFactory


# Load configuration
def load_configuration(file_path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file '{file_path}' was not found.")
    return config


def log_dialog(model_name: str, message: str, seq_num: int):
    print(f"\033[94m{model_name} [{seq_num}]\033[0m : {message}")


def generate_and_log_response(model, prompt, seq_num):
    response = model.generate_response(prompt)
    log_dialog(model.get_provider_model(), response, seq_num)
    return response


def initialize_models():
    return (
        GPTFactory.create_gpt_model("Ollama", "llama3.2:3b", "user"),
        GPTFactory.create_gpt_model("Ollama", "tinyllama:latest", "assistant")
    )


def main():
    config = load_configuration('config.properties')
    user_model, assistant_model = initialize_models()
    initial_prompt = config.get('Prompt', 'initial_prompt')

    log_dialog(user_model.get_provider_model(), initial_prompt, 1)

    assistant_response = generate_and_log_response(assistant_model, initial_prompt, 1)
    for i in range(3):
        user_response = generate_and_log_response(user_model, assistant_response, i + 2)
        assistant_response = generate_and_log_response(assistant_model, user_response, i + 2)


def test():
    chat_gpt_model = GPTFactory.create_gpt_model("ChatGPT", "gpt-3.5-turbo")
    generate_and_log_response(chat_gpt_model, "Hello", 1)

    ollama_model = GPTFactory.create_gpt_model("Ollama", "llama2-uncensored")
    generate_and_log_response(ollama_model, "Hello", 2)


if __name__ == "__main__":
    main()