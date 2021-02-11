from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
import logging
import random
from newssearch import search_keyword



updater = Updater(token='1686427047:AAHQSLOVFSow3IVT7xrgy34flkOXcmp_k_I', use_context=True)

dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def language(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Suomi", callback_data='fi'),
            InlineKeyboardButton("Svenska", callback_data='sv'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Millä kielellä haluat lukea artikkeleita?', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    
    if(query.data == 'fi'):
        language = 'suomi'
    elif(query.data == 'sv'):
        language = 'svenska'
    else:
        language = 'et valinnut kieltä'

    query.edit_message_text(text=f"Valittu kieli: {language}")


def moro(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Kato Sauli terve!")


def kukaoot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moikka! Mä olen Ella-Botti ja autan sua etsimään sisältöä sun elämään. :)")

def search(update, context):
    text = update.message.text
    search_word = text[8:]
    i = 0
    for i in range(i, i+5):
        print(search_word)
        results = search_keyword(search_word)
        print(results)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=results[i])

        


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.dispatcher.add_handler(CommandHandler('language', language))
updater.dispatcher.add_handler(CallbackQueryHandler(button))


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
