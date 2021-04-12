import csv
import json


def make_json(csv_file_path, json_file_path):
    data = {}

    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for rows in csv_reader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['AID']
            data[key] = rows

        # Open a json writer, and use the json.dumps()
        # function to dump data
        with open(json_file_path, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

# Driver Code


# Decide the two file paths according to your
# computer system
csv_file_path = r'/csv/articles.csv'
json_file_path = r'/json/articles.json'

# Call the make_json function
make_json(csv_file_path, json_file_path)


with open(json_file_path) as f:
    datajson = json.load(f)

print(datajson['7-1266481'])
