from telegram import Update
from telegram.ext import ContextTypes
from openai_integration import generate_response
from stable_diffusion_integration import generate_image
import tempfile
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = await generate_response(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# supposing "/image <prompt>" to generate and send an image
async def generate_and_send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    try:
        image_data = generate_image(prompt)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(image_data)
            tmp_file.seek(0)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(tmp_file.name, 'rb'))
            os.unlink(tmp_file.name)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))