from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from newssearch import search_keyword


updater = Updater(token='1686427047:AAHQSLOVFSow3IVT7xrgy34flkOXcmp_k_I', use_context=True)

dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def moro(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Kato Sauli terve!")


def kukaoot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moikka! Mä olen Ella-Botti ja autan sua etsimään sisältöä sun elämään. :)")


def search(update, context):
    text = update.message.text
    search_word = text[8:]
    print(search_word)
    results = search_keyword(search_word)
    print(results)
    context.bot.send_message(chat_id=update.effective_chat.id, text=results[0])


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

moro_handler = CommandHandler('moro', moro)
dispatcher.add_handler(moro_handler)

kukaoot_handler = CommandHandler('kukaoot', kukaoot)
dispatcher.add_handler(kukaoot_handler)

search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)



updater.start_polling()

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
