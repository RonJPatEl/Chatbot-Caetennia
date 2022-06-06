import json
import string
from sentence_transformers import SentenceTransformer, util

import spacy
nlp = spacy.load("nl_core_news_sm")

def read_qa(qa_path):
    '''Read in JSON file with topics and corresponding responses'''
    with open(qa_path, encoding='utf8') as f:
        qa_data = json.load(f)
    return qa_data

def initQAData():
    return read_qa("./data/QandAdata.json")

def initEmbeddings():
    print("Loading embedding model...")
    return SentenceTransformer('distiluse-base-multilingual-cased-v1')

def lemmatize(sentence):
    doc = nlp(sentence)
    lemmas = [word.lemma_ for word in doc]
    lemmatized_sentence = ' '.join(lemmas)
    return lemmatized_sentence

def preprocess(question):
    # lowercasing
    question = question.lower()
    # punctuation removal
    question = question.translate(str.maketrans('', '', string.punctuation))
    # lemmatization
    question = lemmatize(question)
    return question

# Alle generatie logic wordt ook in een specifieke functie gestopt
def generate_response(encoded_input_question, encoded_questions, questions, answers):
    '''Generate a response from the chatbot'''

    answer = []

    hits = util.semantic_search(encoded_input_question, encoded_questions, top_k=5)
    hits = hits[0]  # Get the hits for the first query

    # print("\nDit zijn de top 5 matches voor jouw vraag:\n")
    hitList = []
    for i, hit in enumerate(hits):
        # print(questions[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
        hitList.append(questions[hit['corpus_id']] + "(Score: {:.4f})".format(hit['score']))

        if i == 0:
            top_scoring_question = questions[hit['corpus_id']]
            top_score = hit['score']

    # get the index of the top-scoring question
    target_idx = questions.index(top_scoring_question)

    answer.append(hitList)

    if top_score > 0.4:
        # return the answer matching the top-scoring question
        answer.append( f'\nCaetennia: {answers[target_idx]}')
        # answer[0] = f'\nCaetennia: {answers[target_idx]}'
    else:
        answer.append( f'\nCaetennia: Ik heb daar helaas geen antwoord op. Heb je nog andere vragen?')
        # answer[0] = f'\nCaetennia: Ik heb daar helaas geen antwoord op. Heb je nog andere vragen?'

    return answer


embedding_model = initEmbeddings()
qa_data = initQAData()

# Load questions and answers from the QA json file
questions = [info['Vraag'] for info in qa_data.values()]
answers = [info['Antwoord'] for info in qa_data.values()]

clean_questions = [preprocess(q) for q in questions]

# Encode the questions into vectors
encoded_questions = embedding_model.encode(clean_questions)


# Deze functie staat direct in contact met de Flask Front-end
# TODO: Statische berichten verwerken binnen generate_response functie
def returnResponse(user_input):

    # if user_txt == "hallo":
    #     return "Caetennia: Welkom bij de demo, stel hier jouw vraag!"
    # elif user_input == "doei":
    #     return "Caetennia: Fijn om je vragen te beantwoorden!"
    # else:

    # encode user question
    encoded_input_question = embedding_model.encode(preprocess(user_input))

    response = generate_response(encoded_input_question, encoded_questions, questions, answers)
    return response


# def test():
#     embedding_model = initEmbeddings()
#     qa_data = initQAData()
#
#     # Load questions and answers from the QA json file
#     questions = [info['Vraag'] for info in qa_data.values()]
#     answers = [info['Antwoord'] for info in qa_data.values()]
#
#     clean_questions = [preprocess(q) for q in questions]
#
#     # Encode the questions into vectors
#     encoded_questions = embedding_model.encode(clean_questions)
#
#     # start conversation
#     continue_dialogue = True
#
#     while continue_dialogue:
#
#         # get user input
#         input_question = (input("\nStel een vraag aan Caetennia: "))
#
#         # encode user question
#         encoded_input_question = embedding_model.encode(preprocess(input_question))
#
#         # generate response from chatbot
#         answer = generate_response(encoded_input_question, encoded_questions, questions, answers)
#         print(answer)
