import json
import re
with open('./articles.json') as json_file:
    arr = []
    keyword1 = "'TITLE':"
    keyword2 = ", 'PUBLISHED'"
    data = json.load(json_file)
    #queryString = 'Matchine queries: '
    #query = input("Query parameters: ")
    for i,j in data.items():
        arr.append(str(j))
    print("Data added to array, ready to search:")
    queryString=input("Articles that contain the query:")
    
    for i in range(len(arr)):
        if queryString in arr[i]:
            #print(re.search("(?P<url>https?://[^\s]+)", arr[i]).group("url"))
            result = re.search("'TITLE':(.*), 'PUBLISHED'", arr[i])
            print(result.group(1) + "  -  " +re.search("(?P<url>https?://[^\s]+)", arr[i]).group("url") )
            