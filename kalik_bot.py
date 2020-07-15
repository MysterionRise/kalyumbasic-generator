from telegram.ext import Updater, CommandHandler
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
    try:
        chat_id = update.message.chat.id
        kalik_message = make_sentence()
        print(kalik_message)
        msg = context.bot.send_message(chat_id, kalik_message, parse_mode='HTML')
    except Exception as e:
        print(e)


def main():
    updater = Updater("", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', help))
    updater.dispatcher.add_handler(CommandHandler('kalik', sendKalik))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
