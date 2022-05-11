# Code inspired by https://stackabuse.com/python-for-nlp-creating-a-rule-based-chatbot/

import nltk
import numpy as np
import random
import string
import re
import json

from collections import defaultdict
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_qa(qa_path):
    '''Read in JSON file with topics and corresponding responses'''
    with open(qa_path, encoding='utf8') as f:
        qa_data = json.load(f)
    return qa_data

def perform_lemmatization(tokens):
    '''Return lemmas of a list of tokens'''
    return [wnlemmatizer.lemmatize(token) for token in tokens]

def get_processed_text(document):
    '''Tokenize, lemmatize and remove punctuation from a document of text'''
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

def get_similar_words(embedding_model, input_question, num_similar_words=5):
    '''Enrich an input question with similar words for better keyword detection'''
    
    tokens = get_processed_text(input_question)
    similar_words = defaultdict(set)
    
    for token in set(tokens):
        # Add the token itself to the dictionary
        similar_words[token].add(token)
        
        # Try getting similar words if the vector for the given token is found in the embedding vocabulary
        try:
            word_neighborhood = embedding_model.most_similar(positive=[token], topn=num_similar_words)
            # Add neighbor words to enrich the message
            for item in word_neighborhood:
                word = item[0].lower()
                similar_words[word].add(token)

        except KeyError as e:
            pass
            #print("token '%s' not in embedding vocabulary" % token)

    return similar_words

def generate_response(user_input, qa_data, similar_words):
    '''Generate a response from the chatbot'''

    # initialize chatbot response and topic
    chatrobo_response = "Wat leuk dat je dat wil weten, maar wat bedoel je precies? Kun je je vraag herformuleren?"
    topic = ''
    
    for i in qa_data['intents']:
        
        # get the lemmas of the keywords for a given topic
        lemmatized_keywords = perform_lemmatization(i['keywords'])

        # compare enriched user input & keywords, find overlapping words
        word_intersection = list(set(similar_words.keys()) & set(lemmatized_keywords))
        #print("WORD INTERSECTION:", word_intersection)

        # if a match is found...
        if len(word_intersection) > 0:

            # assign the topic
            topic = i['topic']
            #print("TOPIC:", topic)

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
                chatrobo_response = "Wat leuk dat je dat wil weten, maar wat bedoel je precies? Kun je je vraag herformuleren?"
            # if a match is found, respond with the matching sentence
            else:
                chatrobo_response = '' + i['responses'][similar_sentence_number]

            # remove user input from list of responses
            i['responses'].remove(user_input)

            return chatrobo_response

        # if no match is found between the input words and keywords, continue to the next json intent
        else:
            continue

    return chatrobo_response

# load Dutch embedding model (Wikipedia-160, from https://github.com/clips/dutchembeddings)
print("Loading embedding model...")
embedding_model = KeyedVectors.load_word2vec_format('word-embeddings/wikipedia-160.txt')

# instantiate lemmatizer
wnlemmatizer = nltk.stem.WordNetLemmatizer()

# instantiate punctuation removel
punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

# read in the JSON file with topics and responses
qa_data = read_qa("data/QandAdata.json")

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

# start conversation
continue_dialogue = True

responses = []
prompts == ['Het lijkt erop dat ik je vragen niet kan beantwoorden. Waarom vraag je niet iets over mijn schooltijd?',
            "Het lijkt erop dat ik je vragen niet kan beantwoorden. Waarom vraag je niet iets over mijn hobby's?"]

while continue_dialogue:

    # get user input
    input_question = (input("\nStel een vraag aan Caetennia: ")).lower()

    # enrich user input with similar words for better keyword detection
    similar_words = get_similar_words(embedding_model, input_question)
    #print("ENRICHED MESSAGE:", similar_words)

    # generate response from chatbot
    print("\nCaetennia: ", end="")
    response = generate_response(input_question, qa_data, similar_words)
    print(response)
    responses.append(response)

    # Check which responses were generated after 3 user inputs
    if len(responses) == 3:

        # If the chatbot could not generate a proper response three times in a row, generate a prompt
        if responses.count("Wat leuk dat je dat wil weten, maar wat bedoel je precies? Kun je je vraag herformuleren?") == 3:
            print(random.choice(prompts))

            # Refresh list of responses
            responses = []