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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hei, olen Ella-Botti! Voit hakea Elävän arkiston artikkeleita komennolla /hae [aihe]. Esimerkiksi koira-artikkeleita saat komennolla \"/hae koira\" Haku palauttaa 5 artikkelia")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hej, jag är Boten-Ella. Du kan söka från Yle Arkivet med befallning /sok [tema]. Till exempel med \"/sok hund\" får du hundartiklar. Sök returnerar 5 artiklar" )

def apua(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
🟣 Ella botilla voit hakea sisälöä eri tavoilla:


🔴 /hae aloittaaksesi sisällön haku (Ohjattu haku kaikkeen sisältöön).

🟠 /hae_artikkeli *hakusana*, jos haluat artikkelisisältöä hakusanalla.

🟡 /hae_tv *hakusana*, jos etsit videosisältöä hakusanalla.

🟢 /hae_radio *hakusana*, jos etsit radiosisältöä hakusanalla.

🔵 /paivan_fakta antaa kiinnostavan historiallisen faktan""")

def language(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Suomi", callback_data='fi'),
            InlineKeyboardButton("Svenska", callback_data='se'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Millä kielellä haluat lukea artikkeleita?', reply_markup=reply_markup)





def search(update, context, language):
    
    print(context.args)
    search_word = context.args[0]

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
            InlineKeyboardButton("Näytä lisää", callback_data="s1")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Näytä lisää tuloksia ", reply_markup=reply_markup)
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query



    query.answer()
    
    if(query.data == 'fi'):
        language = 'fi'
        search(context, update, language)
    elif(query.data == 'se'):
        language = 'se'

    elif(query.data == 's1'):
        global lista
        language = lista[5:10]
    else:
        language = 'et valinnut kieltä'


    #search(update, context)
    query.edit_message_text(text=f"{language}")
    
def hae(update, context):
    search(update, context, "fi")

def sok(update, context):
    search(update, context, "se")

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

apua_handler = CommandHandler('apua', apua)
dispatcher.add_handler(apua_handler)

updater.dispatcher.add_handler(CommandHandler('language', language))

updater.dispatcher.add_handler(CallbackQueryHandler(button))

hae_handler = CommandHandler('hae', hae)
dispatcher.add_handler(hae_handler)

sok_handler = CommandHandler('sok', sok)
dispatcher.add_handler(sok_handler)

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
