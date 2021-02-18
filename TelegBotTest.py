from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
import logging
import random
from newssearch import search_keyword
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN=os.getenv('BOT_TOKEN')


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    updater.start_polling()

updater = Updater(token = BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher

lista = []
# functions

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hei, olen Ella-Botti! Voit hakea Elävän arkiston artikkeleita komennolla /hae_artikkeli [aihe]. Esimerkiksi koira-artikkeleita saat komennolla \"/hae_artikkeli koira\" Haku palauttaa 5 artikkelia")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hej, jag är Boten-Ella. Du kan söka från Yle Arkivet med befallning /sok [tema]. Till exempel med \"/sok hund\" får du hundartiklar. Sök returnerar 5 artiklar" )

""" def language(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Suomi", callback_data='l1'),
            InlineKeyboardButton("Svenska", callback_data='l2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Millä kielellä haluat lukea artikkeleita?', reply_markup=reply_markup) """


def search(update, context, language, word):
    if word:
        search_word = word
    elif not word: 
        print(context.args)
        search_word = context.args[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="käytä hakusanaa")

    i = 0
    results = search_keyword(search_word,language)
    if len(results) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ei hakutuloksia / Inga sökresultat")
    else:
        for i in range(i, i+5):
            print(search_word)
        
        
            context.bot.send_message(chat_id=update.effective_chat.id, text=results[i])
    print(results)

    global lista 
    lista = results
    show_more(update, context)
    

def show_more(update: Update, context : CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Näytä lisää", callback_data='s1')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Näytä lisää tuloksia ", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    #query.answer()
    
    """   if(query.data == 'l1'):
        language = 'fi'
        search(context, update, language)
    elif(query.data == 'l2'):
        language = 'se' """

    if(query.data == 's1'):
        global lista
        language = lista[5:10]



    #search(update, context)
    query.edit_message_text(text=f"{language}")

def category(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Artikkelit", callback_data='c1'),
            InlineKeyboardButton("Media", callback_data='c2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Mitä etsit?', reply_markup=reply_markup)


def handle_category(update, context):
    query = update.callback_query

    if query.data == 'c1':
        articles_tag(update, context)
        query.edit_message_text(text='Etsitään artikkeleita...')
    elif query.data == 'c2':
        media_tag(update, context)
        query.edit_message_text(text='Etsitään mediaa...')


def articles_tag(update, context):
    keyboard = [
            [
                InlineKeyboardButton("Kotimaa", callback_data='a1'),
                InlineKeyboardButton("Ulkomaat", callback_data='a2'),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Mitä uutisia haluat lukea?', reply_markup=reply_markup)


def handle_articles_tag(update, context):
    query = update.callback_query

    if query.data == 'a1':
        print('kutsuu funktiota joka tietokannasta')
        search(update, context, 'fi', 'kotimaa')
        query.edit_message_text(text='Etsitään kotimaan uutisia...')
    elif query.data == 'a2':
        query.edit_message_text(text='Etsitään ulkomaiden uutisia...')


def media_tag(update, context):
    keyboard = [
            [
                InlineKeyboardButton("Radio", callback_data='m1'),
                InlineKeyboardButton("TV", callback_data='m2'),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Etsitkö radio- vai tv-ohjelmia?', reply_markup=reply_markup)


def handle_media_tag(update, context):
    query = update.callback_query

    if query.data == 'm1':
        query.edit_message_text(text='Etsitään radio-ohjelmia...')
    elif query.data == 'm2':
        query.edit_message_text(text='Etsitään tv-ohjelmia...')


    
def hae_artikkeli(update, context):
    search(update, context, "fi", '')

def sok(update, context):
    search(update, context, "se", '')

def moro(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Kato Sauli terve!")

def kukaoot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moikka! Mä olen Ella-Botti ja autan sua etsimään sisältöä sun elämään. :)")

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")




# handlers  

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#updater.dispatcher.add_handler(CommandHandler('language', language))

updater.dispatcher.add_handler(CallbackQueryHandler(button, pattern='s'))

hae_handler = CommandHandler('hae_artikkeli', hae_artikkeli)
dispatcher.add_handler(hae_handler)

sok_handler = CommandHandler('sok', sok)
dispatcher.add_handler(sok_handler)

category_handler = CommandHandler('hae', category)
dispatcher.add_handler(category_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(handle_category, pattern='c'))

updater.dispatcher.add_handler(CallbackQueryHandler(handle_articles_tag, pattern='a'))

updater.dispatcher.add_handler(CallbackQueryHandler(handle_media_tag, pattern='m'))

search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

moro_handler = CommandHandler('moro', moro)
dispatcher.add_handler(moro_handler)

kukaoot_handler = CommandHandler('kukaoot', kukaoot)
dispatcher.add_handler(kukaoot_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


if __name__ == "__main__":
    main()
