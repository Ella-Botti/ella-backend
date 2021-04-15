import re
import psycopg2

# language can either be fi or se



def search_keyword(queryString, language):

    conn = psycopg2.connect("dbname=assa user=assa")

    cur = conn.cursor()

    
    #ajetaan tietokantakomento cursori.execute() metodilla. huomaa että tämä avaa automaattisesti transaktion, joka pitää vielä myöhemmin commitoida
    SQL = f"SELECT title, url FROM articles WHERE title LIKE %s AND language='{language}';"
    like_pattern = '%{}%'.format(queryString)
    cur.execute(SQL,(like_pattern,))
    
    lista = cur.fetchall()
    print(f"Found {len(lista)} articles")
    #tärkeää!
    #suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filteredList = []

    for item in lista:
        
        filteredList.append(item[0] + " - " + item[1])

    return filteredList