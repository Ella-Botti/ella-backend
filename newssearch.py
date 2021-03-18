import json
import re
import psycopg2

# language can either be fi or se



def search_keyword(queryString, language):

    conn = psycopg2.connect("dbname=assa user=mikko")

    cur = conn.cursor()

    print("connection succesful")

    
    #ajetaan tietokantakomento cursori.execute() metodilla. huomaa että tämä avaa automaattisesti transaktion, joka pitää vielä myöhemmin commitoida
    SQL = f"SELECT title, url FROM articles WHERE title LIKE %s AND language='{language}';"
    like_pattern = '%{}%'.format(queryString)
    cur.execute(SQL,(like_pattern,))
    #commitoidaan, jotta muutokset jäävät pysyväksi. kuten kaikissa transaktioissa, koodiin voi myös lisätä rollback-funktion
    lista = cur.fetchall()
    print(lista)
    print("search succesful")
    #tärkeää!
    #suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filteredList = []

    for item in lista:
        
        filteredList.append(item[0] + " - " + item[1])

    return filteredList
        


search_keyword('hund', 'sv')
