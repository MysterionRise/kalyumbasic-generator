import logging
import os.path
import pickle

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, ApplicationBuilder,
                          CallbackQueryHandler, CommandHandler, ContextTypes)

import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

feedback = {}
TEXT_MODEL = None


def read_feedback():
    global feedback
    if os.path.exists("feedback"):
        with open("feedback", "rb") as f:
            feedback = pickle.load(f)
    else:
        feedback = {}


def read_model():
    global TEXT_MODEL
    with open("model.data", "rb") as f:
        TEXT_MODEL = pickle.load(f)


async def bot_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id,
        text="""
        <b>Kalik Bot Commands:</b>

        /help - show this help
        /kalik - send Kalik-based message
        """,
        parse_mode="HTML",
    )


def make_sentence():
    sentence = None
    while sentence is None:
        sentence = TEXT_MODEL.make_sentence()
    return sentence


async def send_kalik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("I like it!😊", callback_data="like"),
            InlineKeyboardButton("It's crap😒", callback_data="dislike"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        chat_id = update.message.chat.id
        kalik_message = make_sentence()
        logging.info(kalik_message)
        await context.bot.send_message(
            chat_id, kalik_message, reply_markup=reply_markup, parse_mode="HTML"
        )
    except Exception as e:
        logging.error(e)


async def vote(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    msg_id = query.message.message_id
    user_id = query.from_user.id

    messages = feedback.get(chat_id, {})
    values = messages.get(msg_id, {})
    if query.data == "like":
        values[user_id] = 1
    else:
        values[user_id] = -1
    messages[msg_id] = values
    values["text"] = query.message.text
    feedback[chat_id] = messages
    await query.answer()
    logging.info(feedback)


async def post_stop(application: Application) -> None:
    with open("feedback", "wb") as f:
        pickle.dump(feedback, f)
    logging.info("Shutting down...")


def main():
    read_feedback()
    read_model()

    application = (
        ApplicationBuilder().token(settings.AUTH_TOKEN).post_stop(post_stop).build()
    )

    start_handler = CommandHandler("start", bot_help)
    application.add_handler(start_handler)

    help_handler = CommandHandler("help", bot_help)
    application.add_handler(help_handler)

    kalik_handler = CommandHandler("kalik", send_kalik)
    application.add_handler(kalik_handler)

    application.add_handler(CallbackQueryHandler(vote))

    application.run_polling()


if __name__ == "__main__":
    main()
