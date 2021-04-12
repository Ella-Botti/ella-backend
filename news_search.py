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
    
    lista = cur.fetchall()
    print(lista)
    print("search succesful")
    #tärkeää!
    #suljetaan tietokantayhteys, sillä yhteyksiä voi olla vain rajallisesti!
    conn.close()

    filtered_list = []

    for item in lista:
        
        filtered_list.append(item[0] + " - " + item[1])

    return filtered_list
        


search_keyword('hund', 'sv')
