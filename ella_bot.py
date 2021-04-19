from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import random
from news_search import search_keyword
from dotenv import load_dotenv
import os
from pathlib import Path
from fact_of_the_day import search_fact
from tag_search import search_tag
from api_search_media import get_media, get_tag

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater.start_polling()

updater = Updater(token=BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher

# Luodaan globaali dictionary johon tullaan tallentamaan hakuja chat.idn perusteella
global_user_list = {

}


# functions
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="""
Hei, olen Ella-Botti! 
Voit hakea Elävän arkiston artikkeleita komennolla
/artikkeli *hakusana*.
Esimerkiksi koira-artikkeleita saat komennolla \"/artikkeli koira\"
Hakusanana voit käyttää myös useampaa sanaa.

Voit hakea elävän arkiston media ja radio sisältöä hakusanoilla
/tv *hakusana* ja /radio *hakusana*.

Komennolla /help saat listan kaikista komennoista. 
Aloita kokeilemalla /fakta komentoa. 
""")

    context.bot.send_message(chat_id=update.effective_chat.id,text=
"""Hej, jag är Boten-Ella. Du kan söka från Yle Arkivet med befallning /sok *slagord*.
Till exempel med \"/sok hund\" får du hundartiklar.
Tyvärr fungerar bara artikelsökningen just nu på svenska.
""")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
Ella botilla voit hakea sisälöä eri tavoilla:

/hae aloittaaksesi sisällön haku (Ohjattu haku kaikkeen sisältöön). 
/artikkeli *hakusana*, jos haluat artikkelisisältöä hakusanalla.
/tv *hakusana*, jos etsit videosisältöä hakusanalla.
/radio *hakusana*, jos etsit radiosisältöä hakusanalla.
/fakta antaa kiinnostavan historiallisen faktan. """)

# Hakee tietokannasta artikkeleita hakusanan perusteella
def search(update, context, language, word, position):
    try:
        global global_user_list

        # Hakee hakusanaa funktiokutsusta
        if word:
            global_user_list[update.effective_chat.id] = [word, language, position]
       
        # Jos hakusanaa ei ole funktiokutsussa tai komennon mukana tuoduissa argumenteissa
        elif not word and not context.args:
            print(global_user_list[update.effective_chat.id])

        # Hakee hakusanaa komennon mukana tulleissa argumenteissa
        elif not word:
            print(context.args)
            global_user_list[update.effective_chat.id] = [context.args[0], language, position]

        # Juokseva luku artikkeleille
        i = position

        # Jos hakusana ei ole tyhjä, hakee tietokannasta
        if len(global_user_list[update.effective_chat.id][0]) > 1:
            results = search_keyword(
                global_user_list[update.effective_chat.id][0], language)

            # Jos hakutuloksia ei löydy
            if len(results) == 0:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Ei hakutuloksia / Inga sökresultat")

            # Palauttaa seuraavat viisi tulosta
            else:
                i = global_user_list[update.effective_chat.id][2]
                for i in range(i, i+5):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=results[i])
                    global_user_list[update.effective_chat.id][2] = i+1
                show_more(update, context, i)
            print(update.effective_chat.id)

 # Kehoittaa käuyyäjää syöttämään haulle hakusanan
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Käytä hakusanaa, esimerkiksi '/artikkeli koira'")
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Olet ehtinyt lukea kaikki artikkelini tästä aiheesta, kokeile hakea jollain toisella hakusanalla!")


# Hakee artikkeleita tägien perusteella tietokannasta
def tag_search_articles(update, context, tag):
    try:
        results = search_tag(tag)
        i = 0
        for i in range(i, i+5):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=results[i])
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Olet ehtinyt lukea kaikki artikkelini tästä aiheesta, kokeile hakea jollain toisella hakusanalla!")


# Hakee tv sisältöä api rajapinnasta hakusanan perusteella 
def search_tv(update, context):
    try:
        global global_user_list

        if context.args[0]:
            global_user_list[update.effective_chat.id] = context.args[0]
            results = get_media(' '.join(context.args), 'tvprogram')
            i = 0
            for i in range(i, i+5):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=results[i])
            
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,text="Ei hakusanaa! Käytä komentoa /tv *hakusana*")
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="En löytänyt enempää kuin nämä, kokeile toista hakusanaa!")

# Hakee radio sisältöä api rajapinnasta hakusanan perusteella
def search_radio(update, context):
    global global_user_list

    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ei hakusanaa! Käytä komentoa /radio *hakusana*")
    else:
        global_user_list[update.effective_chat.id] = context.args[0]
        results = get_media(' '.join(context.args), 'radioprogram')
        i = 0
        for i in range(i, i+5):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=results[i])


# Hakee mediaa api rajapinnasta tagin (tyyppi ja kategoria) perusteella
def tag_search_media(update, context, type, category):
    try:
        results = get_tag(type, category)
        i = 0
        for i in range(i, i+5):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=results[i])
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="En löytänyt enempää kuin nämä, kokeile toista hakusanaa!")


# Antaa käyttäjälle napin jolla voi pyytää lisää hakutuloksia
def show_more(update: Update, context: CallbackContext, position):
    keyboard = [
        [
            InlineKeyboardButton("Näytä lisää", callback_data='s1')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Näytä lisää tuloksia ", reply_markup=reply_markup)


# Kuuntelee show_more nappia ja kutsuu hakua
def handle_show_more(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    word = global_user_list[update.effective_chat.id][0]
    print(word)

    if query.data == 's1':
        search(update, context, global_user_list[update.effective_chat.id][1], "", global_user_list[update.effective_chat.id][2])


# Päivän_fakta -komento
def daily_fact(update, context):
    lista = search_fact()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=random.choice(lista))


# Antaa kategoriavaihtoehdot /hae -komennolle
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


# Kuuntelee kategorioita ja kutsuu artikkeli / media tagifunktioita
def handle_category(update, context):
    query = update.callback_query

    if query.data == 'c1':
        articles_tag(update, context)
        query.edit_message_text(text='Etsitään artikkeleita...')
    elif query.data == 'c2':
        media_tag(update, context)
        query.edit_message_text(text='Etsitään mediaa...')


# Antaa artikkelivaihtoehdot tägeinä
def articles_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Politiikka", callback_data='a1'),
            InlineKeyboardButton("Urheilu", callback_data='a2'),
            InlineKeyboardButton("Kulttuuri", callback_data='a3'),
            InlineKeyboardButton("Viihde", callback_data='a4'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Mitä artikkeleita haluat lukea?', reply_markup=reply_markup)


# Kuuntelee articles_tag ja tekee valinnan mukaisen haun
def handle_articles_tag(update, context):
    query = update.callback_query

    if query.data == 'a1':
        query.edit_message_text(text='Etsitään politiikan artikkeleita...')
        tag_search_articles(update, context, 'politiikka')
    elif query.data == 'a2':
        query.edit_message_text(text='Etsitään urheilu artikkeleita...')
        tag_search_articles(update, context, 'urheilu')
    elif query.data == 'a3':
        query.edit_message_text(text='Etsitään kulttuuri artikkeleita...')
        tag_search_articles(update, context, 'kulttuuri')
    elif query.data == 'a4':
        query.edit_message_text(text='Etsitään kulttuuri artikkeleita...')
        tag_search_articles(update, context, 'viihde')


# Antaa mediavaihtoehdot tägeinä
def media_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Radio", callback_data='m1'),
            InlineKeyboardButton("TV", callback_data='m2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Etsitkö radio- vai tv-ohjelmia?', reply_markup=reply_markup)


# Kuuntelee media_tag komentoa ja tekee valinnan mukaisen haun
def handle_media_tag(update, context):
    query = update.callback_query

    if query.data == 'm1':
        radio_tag(update, context)
        query.edit_message_text(text='Etsitään radio-ohjelmia...')
    elif query.data == 'm2':
        tv_tag(update, context)
        query.edit_message_text(text='Etsitään tv-ohjelmia...')


# Antaa radiovaihtoehdot
def radio_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Musiikki", callback_data='r1'),
            InlineKeyboardButton("Kuunnelmat", callback_data='r2'),
            InlineKeyboardButton("Uutiset", callback_data='r3'),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Etsitkö musiikkia, podcasteja vai ajankohtaisohjelmia?', reply_markup=reply_markup)


# Kuuntelee radio_tag komentoa ja tekee valinnan mukaisen haun
def handle_radio_tag(update, context):
    query = update.callback_query

    if query.data == 'r1':
        music_tag(update, context)
        query.edit_message_text(text='Etsitään musiikkia...')
    elif query.data == 'r2':
        tag_search_media(update, context, 'radioprogram', '5-215')
        query.edit_message_text(text='Etsitään kuunnelmia...')
    elif query.data == 'r3':
        tag_search_media(update, context, 'radioprogram', '5-226')
        query.edit_message_text(text='Etsitään uutiset...')


# Antaa musiikki vaihtojehtoja
def music_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Klassinen", callback_data='k1'),
            InlineKeyboardButton("Pop ja rock", callback_data='k2'),
            InlineKeyboardButton("Iskelmä", callback_data='k3'),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Etsitkö musiikkia, podcasteja vai ajankohtaisohjelmia?', reply_markup=reply_markup)


# Kuuntelee radio_tag komentoa ja tekee valinnan mukaisen haun
def handle_music_tag(update, context):
    query = update.callback_query

    if query.data == 'k1':
        tag_search_media(update, context, 'radioprogram', '5-209')
        query.edit_message_text(text='Etsitään klassista...')
    elif query.data == 'k2':
        tag_search_media(update, context, 'radioprogram', '5-205')
        query.edit_message_text(text='Etsitään popmusiikkia...')
    elif query.data == 'k3':
        tag_search_media(update, context, 'radioprogram', '5-207')
        query.edit_message_text(text='Etsitään iskelmää...')


# Antaa tv vaihtoehtoja
def tv_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Sarjat", callback_data='t1'),
            InlineKeyboardButton("Elokuvat", callback_data='t2'),
            InlineKeyboardButton("Urheilu", callback_data='t3')

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Etsitkö sarjoja, elokuvia vai urheilua?', reply_markup=reply_markup)


# Kuuntelee tv_tag komentoa ja tekee valinnan mukaisen haun
def handle_tv_tag(update, context):
    query = update.callback_query

    if query.data == 't1':
        series_tag(update, context)
        query.edit_message_text(text='Etsitään sarjoja...')    
    elif query.data == 't2':
        movie_tag(update, context)
        query.edit_message_text(text='Etsitään elokuvia...')
    elif query.data == 't3':
        tag_search_media(update, context, 'tvprogram', '5-164')
        query.edit_message_text(text='Etsitään urheilua...')

# Antaa sarja vaihtoehtoja
def series_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Kotimaiset sarjat", callback_data='b1'),
            InlineKeyboardButton("Ulkomaiset sarjat", callback_data='b2')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Etsitkö kotimaisia vai ulkomaisia sarjoja?', reply_markup=reply_markup)


# Kuuntelee series_tag komentoa ja tekee valinnan mukaisen haun api-rajapintaan
def handle_series_tag(update, context):
    query = update.callback_query

    if query.data == 'b1': 
        tag_search_media(update, context, 'tvprogram', '5-133')
        query.edit_message_text(text='Etsitään kotimaisia sarjoja...')
    elif  query.data == 'b2':
        tag_search_media(update, context, 'tvprogram', '5-134')
        query.edit_message_text(text='Etsitään ulkomaisia sarjoja...')


# Antaa elokuva vaihtoehtoja
def movie_tag(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Historia", callback_data='f1'),
            InlineKeyboardButton("Jännitys", callback_data='f2'),
            InlineKeyboardButton("Dokumentit", callback_data='f3'),
            InlineKeyboardButton("Komedia", callback_data='f4')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Mitä elokuvia etsit?', reply_markup=reply_markup)


# Kuuntelee movie_tag komentoa ja tekee valinnan mukaisen haun api-rajapintaan
def handle_movie_tag(update, context):
    query = update.callback_query

    if query.data == 'f1':
        tag_search_media(update, context, 'tvprogram', '5-157')
        query.edit_message_text(text='Etsitään tuloksia: historia')
    elif query.data == 'f2':
        tag_search_media(update, context, 'tvprogram', '5-137')
        query.edit_message_text(text='Etsitään tuloksia: jännitys')
    elif query.data == 'f3':
        tag_search_media(update, context, 'tvprogram', '5-148')
        query.edit_message_text(text='Etsitään tuloksia: dokumentti')
    elif query.data == 'f4':
        tag_search_media(update, context, 'tvprogram', '5-136')
        query.edit_message_text(text='Etsitään tuloksia: komedia')
    

# Komento artikkelin haulle hakusanalla
def hae_artikkeli(update, context):
    search(update, context, "fi", '', 0)
    

# Komento artikkelin haulle ruotsiksi
def sok(update, context):
    search(update, context, "sv", '', 0)


# Komento tuntemattomalle komentosyötteelle
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="Anteeksi, en ymmärrä mitä tarkoitat. Kokeile esimerkiksi /hae.")


def unknown_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Anteeksi, en ymmärrä mitä tarkoitat.")


# handlers 

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

category_handler = CommandHandler('hae', category)
dispatcher.add_handler(category_handler)

search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

hae_handler = CommandHandler('artikkeli', hae_artikkeli)
dispatcher.add_handler(hae_handler)

sok_handler = CommandHandler('sok', sok)
dispatcher.add_handler(sok_handler)

search_tv_handler = CommandHandler("tv", search_tv)
dispatcher.add_handler(search_tv_handler)

search_radio_handler = CommandHandler("radio", search_radio)
dispatcher.add_handler(search_radio_handler)

daily_fact_handler = CommandHandler("fakta", daily_fact)
dispatcher.add_handler(daily_fact_handler)

#Tuntemattoman komennon handler
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), unknown_message)
dispatcher.add_handler(echo_handler)


updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_show_more, pattern='s'))

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

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_series_tag, pattern='b'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_movie_tag, pattern='f'))

updater.dispatcher.add_handler(
    CallbackQueryHandler(handle_music_tag, pattern='k'))


if __name__ == "__main__":
    main()
