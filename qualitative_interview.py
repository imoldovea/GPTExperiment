import configparser
from gpt_model import GPTModel
from gpt_factory import GPTFactory

# Constants
CONFIG_FILE = 'interview.properties'
OUTPUT_FILE = 'output_qualitative.txt'
DEFAULT_SECTION = 'DEFAULT'
QUALITATIVE_SECTION = 'Qualitative'
ERROR_CONFIG_NOT_FOUND = "The configuration file 'interview.properties' was not found."


# Load and read configuration
def load_and_read_config(file_path):
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as file:
            config.read_file(file)
    except FileNotFoundError:
        raise FileNotFoundError(ERROR_CONFIG_NOT_FOUND)
    return config


def get_config_value(config, section, option, fallback=None):
    try:
        if fallback:
            return config.get(section, option, fallback=config.get(DEFAULT_SECTION, option))
        return config.get(section, option)
    except configparser.NoOptionError:
        return fallback


def get_config_int(config, section, option, fallback=None):
    try:
        if fallback:
            return config.getint(section, option, fallback=config.getint(DEFAULT_SECTION, option))
        return config.getint(section, option)
    except configparser.NoOptionError:
        return fallback


config = load_and_read_config(CONFIG_FILE)
config._defaults = {k.lower(): v for k, v in config.defaults().items()}

# Read configurations
questions = [q.strip().strip('"') for q in get_config_value(config, QUALITATIVE_SECTION, 'questions').split(",")]
model_count = get_config_int(config, QUALITATIVE_SECTION, 'model_cont')
initial_prompt = f"{get_config_value(config, QUALITATIVE_SECTION, 'initial_prompt1')}. {get_config_value(config, QUALITATIVE_SECTION, 'initial_prompt2')}. "
model_provider = get_config_value(config, QUALITATIVE_SECTION, 'model_provider')
models_list = [model.strip() for model in get_config_value(config, QUALITATIVE_SECTION, 'models').split(",")]


# Define functions
def print_dialog(provider_model: str, response: str, output_file):
    print(f"{provider_model} {response}")
    output_file.write(f"{provider_model}: {response}\n")


def generate_and_print_response(model: GPTModel, prompt: str, output_file):
    response = model.generate_response(prompt, False)
    print_dialog(model.get_provider_model(), response, output_file)
    return response


def create_dialog_models(model_count: int):
    models = []
    number_of_models = len(models_list)
    multiplier, remainder = divmod(model_count, number_of_models)

    for _ in range(multiplier):
        for model_name in models_list:
            models.append(GPTFactory.create_gpt_model(model_provider, model_name, "assistant"))

    for i in range(remainder):
        models.append(GPTFactory.create_gpt_model(model_provider, models_list[i % number_of_models], "assistant"))

    return models


def main():
    with open(OUTPUT_FILE, 'w', encoding="utf-8") as output_file:
        models = create_dialog_models(model_count)
        for idx, question in enumerate(questions, start=1):
            print(f"Question {idx}: {question}" +"\n")
            output_file.write(f"Question {idx}: {question}\n")
            for model in models:
                generate_and_print_response(model, initial_prompt + question, output_file)
                output_file.write('\n')
                print()

if __name__ == "__main__":
    main()