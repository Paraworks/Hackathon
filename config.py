import json

def load_config():
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)
    return config
