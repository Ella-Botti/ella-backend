import json
import re

# language can either be fi or se


def search_keyword(queryString, language):
    with open('./json/articles.json') as json_file:
        results = []
        filteredResults = []
        data = json.load(json_file)
        for i, j in data.items():
            results.append(str(j))

        # filters out swedish articles
        if language == "fi":
            for i in range(len(results)):
                if queryString in results[i]:
                    result = re.search("'TITLE':(.*), 'PUBLISHED'", results[i])
                    url = re.search("(?P<url>https?://\S+)",
                                    results[i]).group("url")
                    if not "svenska" in url:
                        filteredResults.append(result.group(1) + "  -  " + url)
        # filters out finnish articles
        else:
            for i in range(len(results)):
                if queryString in results[i]:
                    result = re.search("'TITLE':(.*), 'PUBLISHED'", results[i])
                    url = re.search("(?P<url>https?://\S+)",
                                    results[i]).group("url")
                    if not "https://yle" in url:
                        filteredResults.append(result.group(1) + "  -  " + url)

    print(filteredResults)
    return(filteredResults)
