import csv
import json


def make_json(csvFilePath, jsonFilePath):
    data = {}

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['PID']
            data[key] = rows

        # Open a json writer, and use the json.dumps()
        # function to dump data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

# Driver Code


# Decide the two file paths according to your
# computer system
csvFilePath = r'./csv/program.csv'
jsonFilePath = r'./json/program.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)


with open(jsonFilePath) as f:
    datajson = json.load(f)

print(datajson['26-2-24366'])