from datetime import date
import psycopg2
from random import randint


def search_fact():
    conn = psycopg2.connect("dbname=assa user=assa")

    cur = conn.cursor()

    print("connection succesful")

    # avataan vastausvaihtoehdot

    content = ["Kävin läpi kenkälaatikkoani ja löysin tämän faktan...", "Pyyhkiessäni pölyjä komerossa tämä tippui päähäni...", "Sohvalla makoillessani tämä juolahti mieleeni...",
               "Vietettyäni vuoden neljän seinän sisällä, muistelin tätä useasti...", "Vaaribot muisteli tätä eilen keinutuolissa...", "Tätä saattaa joskus tarvita tietovisassa...", "TRIVIA TIME!", "Tämä hiiren nakertama fakta löytyi mökiltä..."]
    reply_number = randint(0, (len(content) - 1))

    # ajetaan tietokantakomento cursori.execute() metodilla.

    todays_date = date.today()
    SQL = f"SELECT paiva, kuukausi, vuosi, tapahtuma FROM calendar WHERE kuukausi = {todays_date.month} AND paiva = {todays_date.day} ;"
    cur.execute(SQL)
    events = cur.fetchall()
    print(f"Found {len(events)} events for today")
    print("Search succesful")

    # tärkeää!
    # suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filtered_events = []

    for item in events:
        event = f"{content[reply_number]} Tänään {item[0]}.{item[1]}, vuonna {item[2]} {item[3]}."
        filtered_events.append(event)
    return filtered_events
