from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram.ext.dispatcher import run_async
import pickle
import markovify


@run_async
def help(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, text="""
        <b>Kalik Bot Commands:</b>

        /help - show this help
        /kalik - send Kalik-based message
        """, parse_mode='HTML')


with open('model.data', 'rb') as f:
    text_model = pickle.load(f)


def make_sentence():
    sentence = None
    while sentence is None:
        sentence = text_model.make_sentence()

    return sentence


@run_async
def sendKalik(update, context):
    keyboard = [[InlineKeyboardButton("I like it!😊", callback_data='like'),
                 InlineKeyboardButton("It's crap😒", callback_data='dislike')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        chat_id = update.message.chat.id
        kalik_message = make_sentence()
        print(kalik_message)
        msg = context.bot.send_message(chat_id,
                                       kalik_message,
                                       reply_markup=reply_markup,
                                       parse_mode='HTML'
                                       )
    except Exception as e:
        print(e)


def inlinequery(update, context):
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def main():
    updater = Updater("1261701110:AAG27XYrDT5TYUn0Bq9z6HXKcQzZESjzJjQ", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', help))
    updater.dispatcher.add_handler(CommandHandler('kalik', sendKalik))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
