import json
import re
import psycopg2


def search_tag(queryTag):

    conn = psycopg2.connect("dbname=assa user=mikko")

    cur = conn.cursor()

    print("connection succesful")

    # ajetaan tietokantakomento cursori.execute() metodilla. huomaa että tämä avaa automaattisesti transaktion, joka pitää vielä myöhemmin commitoida
    SQL = f"SELECT a.title, a.url, a.aid FROM articles a JOIN article_tags at ON a.aid=at.aid WHERE at.label = '{queryTag}';"
    cur.execute(SQL,)
    # commitoidaan, jotta muutokset jäävät pysyväksi. kuten kaikissa transaktioissa, koodiin voi myös lisätä rollback-funktion
    lista = cur.fetchall()
    print(f"Found {len(lista)} articles")
    print("search succesful")
    # tärkeää!
    # suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filtered_list = []

    for item in lista:

        filtered_list.append(item[0] + " - " + item[1])

    return filtered_list
