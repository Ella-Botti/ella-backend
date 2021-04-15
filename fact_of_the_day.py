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
    print(f"Found {len(events)} events for today")
    print("Search succesful")

    #tärkeää!
    #suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filtered_events = []

    for item in events:
        event = f"Tänään {item[0]}.{item[1]}, vuonna {item[2]} {item[3]}"
        filtered_events.append(event)
    return filtered_events
    