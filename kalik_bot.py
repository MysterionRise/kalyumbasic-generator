from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async


@run_async
def help(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, text="""
        <b>Kalik Bot Commands:</b>

        /help - show this help
        /sendKalik - send Kalik-based message
        """, parse_mode='HTML')


prev_titles = set()


@run_async
def sendKalik(update, context):
    try:
        chat_id = update.message.chat.id
        kalik_message = ''
        print(kalik_message)
        msg = context.bot.send_message(chat_id, kalik_message, parse_mode='HTML')
    except Exception as e:
        print(e)


def main(argv):
    updater = Updater("", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', help))
    updater.dispatcher.add_handler(CommandHandler('kalik', sendKalik))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main(sys.argv[1:])