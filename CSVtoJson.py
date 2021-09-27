import csv
import json


def make_json(csvFilePath, jsonFilePath):
    data = {}

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:

            key = rows['ID']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Decide the two file paths according to your
# computer system
csvFilePath = "./UserData/LitOnderzoek.csv"
jsonFilePath = "./UserData/QandAData.json"

# Call the make_json function
make_json(csvFilePath, jsonFilePath)
