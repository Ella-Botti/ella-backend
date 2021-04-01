import json
import urllib.request
from dotenv import load_dotenv
import os
from pathlib import Path
from urllib.parse import quote


#.env käyttöön tarvittavat konfiguraatiot
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv('API_KEY')
API_ID = os.getenv('API_ID')


def get_media(keyword, type) :
    #korvataan välilyönnin käyttö %20
    keyword = quote(keyword)
    with urllib.request.urlopen(f'https://external.api.yle.fi/v1/programs/items.json?q={keyword}&type={type}&app_key={API_KEY}&app_id={API_ID}') as response:
        data = response.read()

    media = json.loads(data)

    filteredList = []

    #luodaan media-olio ja lisätään listaan
    for item in media['data']:
        media_item = f'{item["title"]["fi"]} - http://areena.yle.fi/{item["id"]}'   
        filteredList.append(media_item)

    return filteredList

get_media('avara luonto', 'tvprogram')

def get_tag(type, category):
    with urllib.request.urlopen(f'https://external.api.yle.fi/v1/programs/items.json?type={type}&category={category}&app_key={API_KEY}&app_id={API_ID}') as response:
        data = response.read()

    media = json.loads(data)
   
    filteredList = []

    #luodaan media-olio ja lis  t    n listaan
    for item in media['data']:
        media_item = f'{item["title"]} - http://areena.yle.fi/{item["id"]}'   
        filteredList.append(media_item)
   
    return filteredList

 
get_tag('tvprogram', '5-131')