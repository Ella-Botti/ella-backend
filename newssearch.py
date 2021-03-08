import json
import re

# language can either be fi or se


def search_keyword(queryString, language):
    with open('./json/articles.json') as json_file:
        filteredResults = []
        data = json.load(json_file)
        for key in data:
            #the function's parameter defines the language used in the search
            if language == 'fi':
                #finnish articles conveniently have a different URL-property than their swedish counterparts
                #we can use this to check for language and only return finnish or swedish articles
                if 'https://yle' in data[key]['URL']:
                    if queryString in data[key]['TITLE']:
                        #matching articles get appended to a list, which gets returned in the end
                        filteredResults.append(f"{data[key]['TITLE']} - {data[key]['URL']}")
            elif language == 'se':
                if 'svenska' in data[key]['URL']:
                    if queryString in data[key]['TITLE']:                  
                        filteredResults.append(f"{data[key]['TITLE']} - {data[key]['URL']}")
        print(filteredResults)
        return(filteredResults)

search_keyword('hund', 'se')
