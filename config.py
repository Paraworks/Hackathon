import json

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def add_prompt(config, prompt):
    config['prompts'].append(prompt)
    save_config(config)

def add_chat_log(config, message):
    config['chat_logs'].append(message)
    save_config(config)

def delete_prompt(config, prompt_index):
    if 0 <= prompt_index < len(config['prompts']):
        del config['prompts'][prompt_index]
        save_config(config)
    else:
        raise ValueError("Prompt index out of range")

def clear_prompts_and_logs(config):
    config['prompts'] = []
    config['chat_logs'] = []
    save_config(config)
