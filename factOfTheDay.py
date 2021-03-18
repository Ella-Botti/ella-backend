from datetime import date
import psycopg2




def search_fact():
    conn = psycopg2.connect("dbname=assa user=assa")

    cur = conn.cursor()

    print("connection succesful")

    #ajetaan tietokantakomento cursori.execute() metodilla.

    todays_date = date.today()
    SQL = f"SELECT paiva, kuukausi, vuosi, tapahtuma FROM calendar WHERE kuukausi = {todays_date.month} AND paiva = {todays_date.day} ;"
    cur.execute(SQL)
    events = cur.fetchall()
    print(events)
    print("Search succesful")

    #tärkeää!
    #suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filteredEvents = []

    for item in events:
        event = f"Tänään {item[0]}.{item[1]}, vuonna {item[2]} {item[3]}"
        filteredEvents.append(event)
        
    print(filteredEvents)
    return filteredEvents
    