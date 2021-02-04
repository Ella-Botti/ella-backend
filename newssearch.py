import json
import re


def search_keyword(queryString):
    with open('./articles.json') as json_file:
        results = []
        filteredResults = []
        data = json.load(json_file)
        for i,j in data.items():
            results.append(str(j))
        
        for i in range(len(results)):
            if queryString in results[i]:
                result = re.search("'TITLE':(.*), 'PUBLISHED'", results[i])
                filteredResults.append(result.group(1) + "  -  " +re.search("(?P<url>https?://[^\s]+)", results[i]).group("url"))
    return(filteredResults)         