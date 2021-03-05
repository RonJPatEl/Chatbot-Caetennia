import nltk
import numpy as np
import random
import string

import bs4 as bs
import urllib.request
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from spacy.lang.nl.stop_words import STOP_WORDS as nl_stop

# for specific stopword languages
stopword_list = list(nl_stop)

corpus = ""

with open('Text/Corpus.txt') as f:
    temp_corpus = f.readlines()

for element in temp_corpus:
    corpus += element

corpus = corpus.lower()
corpus = re.sub(r'\[[0-9]*\]', ' ', corpus)
corpus = re.sub(r'\s+', ' ', corpus)

corpus_sentences = nltk.sent_tokenize(corpus)
corpus_words = nltk.word_tokenize(corpus)

wnlemmatizer = nltk.stem.WordNetLemmatizer()

def perform_lemmatization(tokens):
    return [wnlemmatizer.lemmatize(token) for token in tokens]


punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

def get_processed_text(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))


greeting_inputs = ("hey", "hallo", "yo", "alles wel", "hi")
greeting_responses = ["Welkom, ik ben een test chatbot"]

def generate_greeting_response(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs:
            return random.choice(greeting_responses)


def generate_response(user_input):
    chatrobo_response = ''
    corpus_sentences.append(user_input)

    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words=stopword_list)
    all_word_vectors = word_vectorizer.fit_transform(corpus_sentences)
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        chatrobo_response = chatrobo_response + "Sorry, ik begrijp je niet..."
        return chatrobo_response
    else:
        chatrobo_response = chatrobo_response + corpus_sentences[similar_sentence_number]
        return chatrobo_response


continue_dialogue = True
print("Hallo, dit is een test-bot, vraag me iets over het onderwerp:")
while(continue_dialogue == True):
    human_text = input()
    human_text = human_text.lower()
    if human_text != 'dag':
        if human_text == 'bedankt' or human_text == 'heel erg bedankt' or human_text == 'dankjewel':
            continue_dialogue = False
            print("TestRobo: graag gedaan")
        else:
            if generate_greeting_response(human_text) != None:
                print("TestRobo: " + generate_greeting_response(human_text))
            else:
                print("TestRobo: ", end="")
                print(generate_response(human_text))
                corpus_sentences.remove(human_text)
    else:
        continue_dialogue = False
        print("TestRobo: Vaarwel")





