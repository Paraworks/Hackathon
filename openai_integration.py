from openai import OpenAI
from config import load_config

async def generate_response(user_input):
    cfg = load_config()
    client = OpenAI(api_key=cfg["openai_api_key"])
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
    )
    reply = chat_completion.choices[0].message.content
    return reply
