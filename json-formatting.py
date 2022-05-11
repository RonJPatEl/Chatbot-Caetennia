import csv
import json

def make_json(input_filepath, json_filepath):

    dictionaries = []
    saved_topics = []

    with open(input_filepath, encoding='latin-1') as infile:
        lines = infile.readlines()

        for i, line in enumerate(lines):

            # Skip the header
            if i > 0:

                # Split the line into a list of items
                items = line.strip('\n').split('\t')

                # Retrieve topic and response
                topic = items[3]
                response = items[2]

                # Fix quotes in responses
                if response.startswith('"'):
                    response = response.strip('"')
                    response = response.replace('""', '"')
                
                # For the first occurrence of a topic, create a new dictionary
                if topic not in saved_topics:
                    topic2response = {'topic': topic, 'responses': [response]}
                    dictionaries.append(topic2response)
                    saved_topics.append(topic)

                else:
                    # For the remaining lines, look up the topic first, then add the response
                    for d in dictionaries:
                        if topic == d['topic']:
                            d['responses'].append(response)

    data = dict()
    data['intents'] = dictionaries

    # Open a json writer, and use the json.dumps() function to dump data
    with open(json_filepath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# Decide the two file paths according to your computer system
input_filepath = "data/LitOnderzoek.txt"
json_filepath = "data/QandAData.json"

# Call the make_json function
make_json(input_filepath, json_filepath)
