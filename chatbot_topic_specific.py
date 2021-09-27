import nltk
import numpy as np
import random
import string
import re
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from spacy.lang.nl.stop_words import STOP_WORDS as nl_stop

def read_qa(qa_path):
    '''Read in JSON file with topics and corresponding responses'''
    with open(qa_path) as f:
        qa_data = json.load(f)

    return qa_data

# instantiate lemmatizer
wnlemmatizer = nltk.stem.WordNetLemmatizer()

def perform_lemmatization(tokens):
    '''Return lemmas of a list of tokens'''
    return [wnlemmatizer.lemmatize(token) for token in tokens]

# instantiate punctuation removel
punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

def get_processed_text(document):
    '''Tokenize, lemmatize and remove punctuation from a document of text'''
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

def generate_response(topic, user_input, qa_data):
    '''Generate a response given a topic, input message from the user, and a json file containing responses'''

    # initialize chatbot response
    chatrobo_response = ''
    
    for i in qa_data['intents']:

        # look for topic match
        if topic == i['topic']:

            # add user input to list of responses
            i['responses'].append(user_input)

            # remove special characters and empty spaces from sentences
            for sentence in i['responses']:
                sentence = sentence.lower()
                sentence = re.sub(r'\[[0-9]*\]', ' ', sentence)
                sentence = re.sub(r'\s+', ' ', sentence)

            # initialize word vectorizer
            word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text)

            # transform all sentences into vectors
            all_word_vectors = word_vectorizer.fit_transform(i['responses'])

            # calculate cosine similarity of last vector (user input) and the other vectors
            similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)

            # get the vector with the highest similarity
            similar_sentence_number = similar_vector_values.argsort()[0][-2]
            matched_vector = similar_vector_values.flatten()
            matched_vector.sort()
            vector_matched = matched_vector[-2]

            # if no match is found (i.e. the cosine similarity is 0), respond with "I don't understand"
            if vector_matched == 0:
                chatrobo_response = chatrobo_response + "Wat leuk dat je dat wil weten, maar wat bedoel je precies? Kun je je vraag herformuleren?"
            # if a match is found, respond with the matching sentence
            else:
                chatrobo_response = chatrobo_response + i['responses'][similar_sentence_number]

            # remove user input from list of responses
            i['responses'].remove(user_input)

            return chatrobo_response

# read in the JSON file with topics and responses
qa_data = read_qa("qa_caetennia.json")

# print initial message 
print("""Ik ben Caetennia en zoals op mijn grafsteen staat ben ik 10 jaar oud geworden.
Ik ben geboren in de tijd van Trajanus en ik kom uit een rijke familie.
Toen ik 10 was werd ik uitgehuwelijkt aan een andere rijke familie om onze politieke banden te verbeteren.
Ik wilde niet trouwen met deze man. Ongeveer 2 weken voordat we zouden gaan trouwen gingen we samen 
water halen uit een put die net buiten het dorpje lag. Daar kregen we ruzie over de trouwerij en de 
welvaart van onze families. Hij werd heel boos en wist niet meer wat hij deed en struikelde over een 
losse steen op de grond. Voordat ik wist wat er aan de hand was viel hij achterover over de rand van 
de put en viel erin. Ik was bang voor wat er zou gebeuren als mijn familie hier achterkwam dus ben ik weggerend. 
Je kijkt nu naar mijn grafsteen.""")

continue_dialogue = True
stay_within_topic = True
verb = "beginnen"

while continue_dialogue:

    ask_question = input(f"\nCaetennia: Wil je het gesprek {verb}? \n")
    verb = "voortzetten"

    # make input from user lowercase
    ask_question = ask_question.lower()

    if 'ja' in ask_question:
        # let user choose topic
        topic = input("\nCaetennia: Leuk! Over welk onderwerp zou je meer willen weten?\n")
        
        # make input from user lowercase
        topic = topic.lower()

        # print additional information based on chosen topic
        if 'kindersterfte' in topic or 'ziekte' in topic:
            topic = 'kindersterfte in de oudheid'
        elif 'huwelijk' in topic or 'trouwen' in topic:
            topic = 'het huwelijk'
        elif 'grafsteen' in topic or 'altaar' in topic:
            topic = 'het grafaltaar'

        while stay_within_topic:

            # get input question from user
            human_text = input(f"\nCaetennia: Ik ben benieuwd naar je vraag over {topic}! Wat zou je willen weten?\n")
            human_text = human_text.lower()
            
            # generate response from chatbot
            print("\nCaetennia: ", end="")
            print(generate_response(topic, human_text, qa_data))
            print()
                        
            # ask user if they want to change the topic
            another_question = input(f"Caetennia: Wil je nog iets vragen over {topic}?\n")
            
            # make input from user lowercase
            another_question = another_question.lower()
            if 'nee' in another_question:
                break
    else:
        print("\nCaetennia: Ok, leuk je gesproken te hebben!")
        break
