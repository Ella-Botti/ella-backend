from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import random
from newssearch import search_keyword
from dotenv import load_dotenv
import os
from pathlib import Path
from factOfTheDay import search_fact

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater.start_polling()


updater = Updater(token=BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher


#Luodaan globaali dictionary johon tullaan tallentamaan hakuja chat.idn perusteella
global_user_list = {
    
}



# functions
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hei, olen Ella-Botti! Voit hakea Elävän arkiston artikkeleita komennolla /hae_artikkeli [aihe]. Esimerkiksi koira-artikkeleita saat komennolla \"/hae_artikkeli koira\" Haku palauttaa 5 artikkelia")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hej, jag är Boten-Ella. Du kan söka från Yle Arkivet med befallning /sok [tema]. Till exempel med \"/sok hund\" får du hundartiklar. Sök returnerar 5 artiklar")


def apua(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
🔵  Ella botilla voit hakea sisälöä eri tavoilla:


🔵  /hae aloittaaksesi sisällön haku (Ohjattu haku kaikkeen sisältöön).

🔵  /hae_artikkeli *hakusana*, jos haluat artikkelisisältöä hakusanalla.

🔵  /hae_tv *hakusana*, jos etsit videosisältöä hakusanalla.

🔵  /hae_radio *hakusana*, jos etsit radiosisältöä hakusanalla.

🔵  /paivan_fakta antaa kiinnostavan historiallisen faktan """)


def search(update, context, language, word, position):
    global global_user_list
    #Hakee funktiokutsusta
    if word:
        global_user_list[update.effective_chat.id] = word



    #Jos ei ole funktiokutsussa tai komennon mukana tuoduissa argumenteissa
    elif not word and not context.args:
        print(global_user_list[update.effective_chat.id])
        

    #Komennon mukana tulleissa argumenteissa
    elif not word:
        print(context.args)
        global_user_list[update.effective_chat.id] = context.args[0]

    #Juokseva luku artikkeleille
    i = position
    
    #Jos hakusana ei ole tyhjä, hakee tietokannasta
    if len(global_user_list[update.effective_chat.id]) > 1:
        results = search_keyword(global_user_list[update.effective_chat.id], language)

        #Jos hakutuloksia ei löydy
        if len(results) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Ei hakutuloksia / Inga sökresultat")

        #Palauttaa seuraavat viisi tulosta
        else:
            for i in range(i, i+5):
                print(global_user_list[update.effective_chat.id])

                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=results[i])
        show_more(update, context, 5)
        print(results)


    #Kehoittaa käuyyäjää syöttämään haulle hakusanan
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Käytä hakusanaa")

#Antaa käyttäjälla napin jolla voi pyytää lisää hakutuloksia
def show_more(update: Update, context: CallbackContext, position):
    keyboard = [
        [
            InlineKeyboardButton("Näytä lisää", callback_data='s1')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Näytä lisää tuloksia ", reply_markup=reply_markup)

#Kuuntelee show_more nappia ja kutsuu hakua
def handle_showmore(update: Update, context: CallbackContext) -> None:
    query = update.callback_query


    word = global_user_list[update.effective_chat.id]
    print(word)
    
    if query.data == 's1':
        search(update, context, "sv", "", 5)
    
#Komento tv-ohjelmien hakemiseen hakusanalla
def search_tv(update, context):
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ei hakusanaa! Käytä komentoa /hae_tv *hakusana*")
    else:
        print("hae program,json tiedostosta tietoja")


#Komento daily_fact haulle
def daily_fact(update, context):
    lista = search_fact()
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(lista))


#Antaa kategoriavaihtoehdot
def category(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Artikkelit", callback_data='c1'),
            InlineKeyboardButton("Media", callback_data='c2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Mitä etsit?', reply_markup=reply_markup)

#Kuuntelee kategorioita ja kutsuu tagifunktioita
def handle_category(update, context):
    query = update.callback_query

    if query.data == 'c1':
        articles_tag(update, context)
        query.edit_message_text(text='Etsitään artikkeleita...')
    elif query.data == 'c2':
        media_tag(update, context)
        query.edit_message_text(text='Etsitään mediaa...')

#Antaa artikkelivaihtoehdot
def articles_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Kotimaa", callback_data='a1'),
            InlineKeyboardButton("Ulkomaat", callback_data='a2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Mitä uutisia haluat lukea?', reply_markup=reply_markup)

#Kuuntelee articles_tag ja tekee valinnan mukaisen haun
def handle_articles_tag(update, context):
    query = update.callback_query

    if query.data == 'a1':
        print('kutsuu funktiota joka tietokannasta')
        search(update, context, 'fi', 'kotimaa', 0)
        query.edit_message_text(text='Etsitään kotimaan uutisia...')
    elif query.data == 'a2':
        query.edit_message_text(text='Etsitään ulkomaiden uutisia...')

#Antaa mediavaihtoehdot
def media_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Radio", callback_data='m1'),
            InlineKeyboardButton("TV", callback_data='m2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Etsitkö radio- vai tv-ohjelmia?', reply_markup=reply_markup)

#Kuuntelee media_tag komentoa ja tekee valinnan mukaisen haun
def handle_media_tag(update, context):
    query = update.callback_query

    if query.data == 'm1':
        radio_tag(update, context)
        query.edit_message_text(text='Etsitään radio-ohjelmia...')
    elif query.data == 'm2':
        tv_tag(update, context)
        query.edit_message_text(text='Etsitään tv-ohjelmia...')

#Antaa radiovaihtoehdot
def radio_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Musiikki", callback_data='r1'),
            InlineKeyboardButton("Podcast", callback_data='r2'),
            InlineKeyboardButton("Ajankohtaisohjelmat", callback_data='r3'),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Etsitkö musiikkia, podcasteja vai ajankohtaisohjelmia?', reply_markup=reply_markup)

#Kuuntelee radio_tag komentoa ja tekee valinnan mukaisen haun
def handle_radio_tag(update,context):
    query = update.callback_query

    if query.data == 'r1':
        query.edit_message_text(text='Etsitään musiikkia...')
    elif query.data == 'r2':
        query.edit_message_text(text='Etsitään podcasteja...')
    elif query.data == 'r3':
        query.edit_message_text(text='Etsitään ajankohtaisohjelmia...')
        #tähän haku tietokantaan

#Antaa tv vaihtoehtoja
def tv_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Sarjat", callback_data='t1'),
            InlineKeyboardButton("Elokuvat", callback_data='t2'),
            InlineKeyboardButton("Dokumentit", callback_data='t3'),
            InlineKeyboardButton("Urheilu", callback_data='t3')

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Etsitkö sarjoja, elokuvia, dokumentteja vai urheilua?', reply_markup=reply_markup)

#Kuuntelee tv_tag komentoa ja tekee valinnan mukaisen haun
def handle_tv_tag(update,context):
    query = update.callback_query

    if query.data == 't1':
        query.edit_message_text(text='Etsitään sarjoaj...')
    elif query.data == 't2':
        query.edit_message_text(text='Etsitään elokuvia...')
    elif query.data == 't3':
        query.edit_message_text(text='Etsitään dokumentteja...')
    elif query.data == 't4':
        query.edit_message_text(text='Etsitään urheilua...')
        #tähän haku tietokantaan



#Komento artikkelin haulle hakusanalla
def hae_artikkeli(update, context):
    search(update, context, "fi", '', 0)


#Komento artikkelin haulle hakusanalla ruotsiksi
def sok(update, context):
    search(update, context, "sv", '', 0)

#Komento tuntemattomalle komentosyötteelle
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

    """ def language(update: Update, context: CallbackContext) -> None:

    keyboard = [
        [
            InlineKeyboardButton("Suomi", callback_data='l1'),
            InlineKeyboardButton("Svenska", callback_data='l2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Millä kielellä haluat lukea artikkeleita?', reply_markup=reply_markup) """


# handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# updater.dispatcher.add_handler(CommandHandler('language', language))

apua_handler = CommandHandler('apua', apua)
dispatcher.add_handler(apua_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(handle_showmore, pattern='s'))

hae_handler = CommandHandler('hae_artikkeli', hae_artikkeli)
dispatcher.add_handler(hae_handler)

sok_handler = CommandHandler('sok', sok)
dispatcher.add_handler(sok_handler)

search_tv_handler = CommandHandler("hae_tv", search_tv)
dispatcher.add_handler(search_tv_handler)

category_handler = CommandHandler('hae', category)
dispatcher.add_handler(category_handler)

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_category, pattern='c'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_articles_tag, pattern='a'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_media_tag, pattern='m'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_radio_tag, pattern='r'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_tv_tag, pattern='t'))

search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

daily_fact_handler = CommandHandler("paivan_fakta", daily_fact)
dispatcher.add_handler(daily_fact_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


if __name__ == "__main__":
    main()
