from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
from random import randint, choice
from news_search import search_keyword
from dotenv import load_dotenv
import os
from pathlib import Path
from fact_of_the_day import search_fact
from tag_search import search_tag
from api_search_media import get_media, get_tag
from replies import *
import time

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
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
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

    context.bot.send_message(chat_id=update.effective_chat.id, text="""Hej, jag är Boten-Ella. Du kan söka från Yle Arkivet med befallning /sok *slagord*.
Till exempel med \"/sok hund\" får du hundartiklar.
Tyvärr fungerar bara artikelsökningen just nu på svenska.
""")

    notifikaatio_lista = search_fact()

    # Tarkistaa onko kello 12.00, jos on, lähettää päivän faktan
    while True:
        localtime = time.localtime()
        seconds_str = time.strftime("%S", localtime)
        minutes_str = time.strftime("%M", localtime)
        hours_str = time.strftime("%H", localtime)
        seconds_int = int(seconds_str)
        minutes_int = int(minutes_str)
        hours_int = int(hours_str)

        if seconds_int == 0 and minutes_int == 0 and hours_int == 12:
            context.bot.send_message(chat_id=update.effective_chat.id, text=choice(notifikaatio_lista))
            time.sleep(2)



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
            global_user_list[update.effective_chat.id] = [
                word, language, position]

        # Jos hakusanaa ei ole funktiokutsussa tai komennon mukana tuoduissa argumenteissa
        elif not word and not context.args:
            print(global_user_list[update.effective_chat.id])

        # Hakee hakusanaa komennon mukana tulleissa argumenteissa
        elif not word:
            print(context.args)
            global_user_list[update.effective_chat.id] = [
                context.args[0], language, position]

        # Juokseva luku artikkeleille
        i = position

        # Jos hakusana ei ole tyhjä, hakee tietokannasta
        if len(global_user_list[update.effective_chat.id][0]) > 1:
            results = search_keyword(
                global_user_list[update.effective_chat.id][0], language)

            # Jos hakutuloksia ei löydy
            if len(results) == 0:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=no_results[randint(0, (len(no_results) - 1))])

            # Palauttaa seuraavat viisi tulosta
            else:
                i = global_user_list[update.effective_chat.id][2]
                for i in range(i, i+5):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=results[i])
                    global_user_list[update.effective_chat.id][2] = i+1
                show_more(update, context, 's1')
            print(update.effective_chat.id)

 # Kehoittaa käuyyäjää syöttämään haulle hakusanan
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_search_word[randint(0, (len(no_search_word) - 1))])
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_more_results[randint(0, (len(no_more_results) - 1))])


# Antaa käyttäjälle napin jolla voi pyytää lisää hakutuloksia
def show_more(update: Update, context: CallbackContext, mode):
    keyboard = [
        [
            InlineKeyboardButton("Näytä lisää", callback_data=mode)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Haluatko lisää tuloksia?", reply_markup=reply_markup)
                             


# Kuuntelee show_more nappia ja kutsuu hakua
def handle_show_more(update: Update, context: CallbackContext) -> None:
    query = update.callback_query 
    if query.data == 's1':
        search(update, context, global_user_list[update.effective_chat.id]
               [1], "", global_user_list[update.effective_chat.id][2])
    elif query.data == 's2':
        search_tv(update, context, global_user_list[update.effective_chat.id][0], global_user_list[update.effective_chat.id][2])
    elif query.data == 's3':
        search_radio(update, context, global_user_list[update.effective_chat.id][0], global_user_list[update.effective_chat.id][2])
    elif query.data == 's4':
        tag_search_articles(update, context, global_user_list[update.effective_chat.id][0], global_user_list[update.effective_chat.id][2])
    elif query.data == 's5':
        tag_search_media(update, context, global_user_list[update.effective_chat.id][3], global_user_list[update.effective_chat.id][0], global_user_list[update.effective_chat.id][2])


# Hakee artikkeleita tägien perusteella tietokannasta
def tag_search_articles(update, context, tag, position):
    try:
        global global_user_list
        global_user_list[update.effective_chat.id] = [tag, '', position]
        results = search_tag(tag)
        if len(results) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=no_results[randint(0, (len(no_results) - 1))])
        elif len(results) > 0:
            i = position
            for i in range(i, i+5):
                context.bot.send_message(chat_id=update.effective_chat.id, text=results[i])
                global_user_list[update.effective_chat.id][2] = i+1
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tee uusi haku /hae")
            show_more(update, context, "s4")

    # Jos tulokset loppuvat, botti antaa replies.py:stä vastauksen
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,text=no_more_results[randint(0, (len(no_more_results) - 1))])

    # Jos käyttäjä ei tarjoa hakusanaa, botti antaa replies.py:stä vastauksen
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_search_word[randint(0, (len(no_search_word) - 1))])


# Hakee mediaa api rajapinnasta tagin (tyyppi ja kategoria) perusteella
def tag_search_media(update, context, type, category, position):
    try:
        global global_user_list
        global_user_list[update.effective_chat.id] = [category, '', position, type]
        results = get_tag(type, category)
        if len(results) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=no_results[randint(0, (len(no_results) - 1))])
        elif len(results) > 0:
            i = position
            for i in range(i, i+5):
                context.bot.send_message(chat_id=update.effective_chat.id, text=results[i])
                global_user_list[update.effective_chat.id][2] = i+1
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tee uusi haku /hae")
            show_more(update, context, "s5")


    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_more_results[randint(0, (len(no_more_results) - 1))])

    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_search_word[randint(0, (len(no_search_word) - 1))])


# Hakee tv sisältöä api rajapinnasta hakusanan perusteella
def search_tv(update, context, word, position):
    try:
        global global_user_list

        if word:
            global_user_list[update.effective_chat.id] = [word, '', position]

        elif context.args[0]:
            global_user_list[update.effective_chat.id] = [context.args[0], '', position]
        
        results = get_media(global_user_list[update.effective_chat.id][0], 'tvprogram')
        
        if len(results) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=no_results[randint(0, (len(no_results) - 1))])
        
        else:         
            i = position
        
            for i in range(i, i+5):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=results[i])
                global_user_list[update.effective_chat.id][2] = i+1
            show_more(update, context, 's2')

    
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_search_word[randint(0, (len(no_search_word) - 1))])
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_more_results[randint(0, (len(no_more_results) - 1))])


# Hakee radio sisältöä api rajapinnasta hakusanan perusteella
def search_radio(update, context, word, position):
    try:
        global global_user_list

        if word:
            global_user_list[update.effective_chat.id] = [word, '', position]

        elif context.args[0]:
            global_user_list[update.effective_chat.id] = [context.args[0], '', position]
        
        results = get_media(global_user_list[update.effective_chat.id][0], 'radioprogram')
        
        if len(results) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=no_results[randint(0, (len(no_results) - 1))])
        
        else:         
            i = position
            for i in range(i, i+5):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=results[i])
                global_user_list[update.effective_chat.id][2] = i+1
            show_more(update, context, 's3')

    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_search_word[randint(0, (len(no_search_word) - 1))])
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=no_more_results[randint(0, (len(no_more_results) - 1))])


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

    elif query.data == 'c2':
        media_tag(update, context)



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
        tag_search_articles(update, context, 'politiikka', 0)
    elif query.data == 'a2':
        tag_search_articles(update, context, 'urheilu', 0)
    elif query.data == 'a3':
        tag_search_articles(update, context, 'kulttuuri', 0)
    elif query.data == 'a4':
        tag_search_articles(update, context, 'viihde', 0)


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
    elif query.data == 'm2':
        tv_tag(update, context)


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
    elif query.data == 'r2':
        tag_search_media(update, context, 'radioprogram', '5-215', 0)
    elif query.data == 'r3':
        tag_search_media(update, context, 'radioprogram', '5-226', 0)


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
        tag_search_media(update, context, 'radioprogram', '5-209',0)
    elif query.data == 'k2':
        tag_search_media(update, context, 'radioprogram', '5-205', 0)
    elif query.data == 'k3':
        tag_search_media(update, context, 'radioprogram', '5-207', 0)


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
    elif query.data == 't2':
        movie_tag(update, context)
    elif query.data == 't3':
        tag_search_media(update, context, 'tvprogram', '5-164', 0)


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
        tag_search_media(update, context, 'tvprogram', '5-133', 0)
    elif query.data == 'b2':
        tag_search_media(update, context, 'tvprogram', '5-134', 0)


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
        tag_search_media(update, context, 'tvprogram', '5-157', 0)
    elif query.data == 'f2':
        tag_search_media(update, context, 'tvprogram', '5-137', 0)
    elif query.data == 'f3':
        tag_search_media(update, context, 'tvprogram', '5-148', 0)
    elif query.data == 'f4':
        tag_search_media(update, context, 'tvprogram', '5-136', 0)



# Päivän_fakta -komento
def daily_fact(update, context):
    lista = search_fact()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=choice(lista))


# Komento artikkelin haulle hakusanalla
def hae_artikkeli(update, context):
    search(update, context, "fi", '', 0)

# Komento artikkelin haulle ruotsiksi
def sok(update, context):
    search(update, context, "sv", '', 0)

# Komento tv haulle hakusanalla
def hae_tv(update, context):
    search_tv(update, context, '', 0)

# Komento radion haulle hakusanalla
def hae_radio(update, context):
    search_radio(update, context, '', 0)

# Komento tuntemattomalle komentosyötteelle
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=unknown_command[randint(0, (len(unknown_command) - 1))])

def unknown_message(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=unknown_command[randint(0, (len(unknown_command) - 1))])


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

hae_tv_handler = CommandHandler("tv", hae_tv)
dispatcher.add_handler(hae_tv_handler)

hae_radio_handler = CommandHandler("radio", hae_radio)
dispatcher.add_handler(hae_radio_handler)

daily_fact_handler = CommandHandler("fakta", daily_fact)
dispatcher.add_handler(daily_fact_handler)

# Tuntemattoman komennon handler
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

echo_handler = MessageHandler(
    Filters.text & (~Filters.command), unknown_message)
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
