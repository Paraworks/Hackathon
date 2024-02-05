from config import add_chat_log, add_prompt, clear_prompts_and_logs, delete_prompt, load_config
from telegram import Update
from telegram.ext import ContextTypes
from openai_integration import generate_response
from stable_diffusion_integration import generate_image
import tempfile
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
Welcome to the Fashion Assistant Bot! 🎉

I'm here to help you find the perfect outfit combinations and inspire your fashion choices. You can ask me for fashion advice, ideas for specific occasions, or how to match pieces you already own.

To get started, simply type your request. For example, you could ask, "What should I wear for a casual day out?" or "Show me summer outfit ideas."

Commands you can use:
- /start: Restart this welcome message.
- /save: Save the last bot's reply as a prompt for generating images.
- /delete [number]: Delete a specific prompt by its list number.
- /restart: Clear all saved prompts and start a new session.
- /image: Generate images based on your saved prompts.

Feel free to ask me anything about fashion!
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = load_config()
    reply = await generate_response(update.message.text)
    add_chat_log(cfg, {"user": update.message.text, "bot": reply})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = load_config()
    # Check if there is at least one chat log
    if cfg['chat_logs']:
        # Fetch the last chat log
        last_chat_log = cfg['chat_logs'][-1]
        # Extract the bot's reply from the last chat log
        last_reply = last_chat_log.get("bot", "")
        if last_reply:
            # Add the last bot reply as a new prompt
            add_prompt(cfg, last_reply)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Last reply saved as a prompt.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No reply found to save.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No chat history to save from.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = load_config()
    try:
        prompt_index = int(context.args[0])
        delete_prompt(cfg, prompt_index)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Prompt deleted successfully.")
    except ValueError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = load_config()
    clear_prompts_and_logs(cfg)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation restarted. Please enter new prompts.")


# supposing "/image <prompt>" to generate and send an image
async def generate_and_send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = load_config()
    for prompt in cfg['prompts']:
        try:
            image_data = generate_image(prompt)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(image_data)
                tmp_file.seek(0)
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(tmp_file.name, 'rb'))
                os.unlink(tmp_file.name)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
