import json
from sentence_transformers import SentenceTransformer, util

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

# Alle generatie logic wordt ook in een specifieke functie gestopt
def generate_response(encoded_input_question, encoded_questions, questions, answers):
    '''Generate a response from the chatbot'''

    hits = util.semantic_search(encoded_input_question, encoded_questions, top_k=5)
    hits = hits[0]  # Get the hits for the first query

    print("\nDe volgende vragen zijn gematcht met jouw vraag:\n")
    for i, hit in enumerate(hits):
        print(questions[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))

        if i == 0:
            top_scoring_question = questions[hit['corpus_id']]

    # get the index of the top-scoring question
    target_idx = questions.index(top_scoring_question)

    # return the answer matching the top-scoring question
    answer = f'\nCaetennia: {answers[target_idx]}'

    return answer

# Deze functie staat direct in contact met de Flask Front-end
def returnResponse(user_input):
    user_txt = user_input.lower()

    if user_txt == "hallo":
        return "Welkom bij de demo, stel hier jouw vraag!"
    elif user_input == "doei":
        return "Fijn om je vragen te beantwoorden!"
    else:
        response = generate_response(encoded_input_question, encoded_questions, questions, answers)
        return response

def test():
    embedding_model = initEmbeddings()
    qa_data = initQAData()

    # Load questions and answers from the QA json file
    questions = [info['Vraag'] for info in qa_data.values()]
    answers = [info['Antwoord'] for info in qa_data.values()]

    # Encode the questions into vectors
    encoded_questions = embedding_model.encode(questions)

    # start conversation
    continue_dialogue = True

    while continue_dialogue:

        # get user input
        input_question = (input("\nStel een vraag aan Caetennia: "))

        # encode user question
        encoded_input_question = embedding_model.encode(input_question)

        # generate response from chatbot
        print(generate_response(encoded_input_question, encoded_questions, questions, answers))

if __name__ == "__main__":
    test()