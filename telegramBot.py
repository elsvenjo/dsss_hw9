from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, filters, ContextTypes)
from transformers import pipeline

model = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'

generator = pipeline('text-generation', model=model, device=0)


def generate_response(user_prompt):
    response = generator(f'Question: {user_prompt}.\nAnswer:',
                         max_length=200,
                         num_return_sequences=1,
                         temperature=0.7
                         )[0]['generated_text']
    return response.split('Answer:')[1].strip()


token = ''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! I am an AI assistant. How can I help you today!')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = generate_response(user_message)
    await update.message.reply_text(response)


def main():
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('running...')

    application.run_polling()


if __name__ == '__main__':
    main()

