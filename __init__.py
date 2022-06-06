from flask import Flask, render_template, request, jsonify, send_file
from logging import FileHandler,WARNING

import time
import random
import datetime
import json
import os
import nltk 

import chatbot

app = Flask(__name__, template_folder="templates")


message = []
response = []
triggers = ["grafaltaar", "school", "caettenia"]

DATA_FILENAME = "./data/ChatLog.txt"

imageFolder = os.path.join('static', 'images')
app.config["UPLOAD_FOLDER"] = imageFolder

imgname = None

introText = """Stel een vraag aan Caetennia: """



@app.route('/')
def index():
    # Dit reset de chatLog wanneer de sessie geinitialiseerd wordt.
    #open('data/ChatLog.txt', 'w').close()
    
    return render_template('index.html')


@app.route('/', methods=['POST'])


@app.route("/getLogData")
def getLogData():
    return send_file('data/ChatLog.txt',
                     mimetype='text/plain',
                     attachment_filename='ChatLog.txt',
                     as_attachment=True)


@app.route("/getResponse")
def get_bot_response():
    userText = request.args.get('msg')
    logMessage(userText, 0)

    chatbot_response = chatbot.returnResponse(userText)
    logMessage(chatbot_response, 1)

    time.sleep(random.uniform(0.5, 1))
    return str(chatbot_response[1])

@app.route("/getImage")
def getImage():
    userText = request.args.get('msg')
    imagePath = checkSubString(userText)
    FormatImagePath = str(imagePath)
    print(FormatImagePath)
    return FormatImagePath


def logMessage(response, mode):
    timestamp = datetime.datetime.now()

    file_object = open(DATA_FILENAME, "a")

    if mode == 1:
        for hits in response[0]:
            file_object.write(str(timestamp) + " CHATBOT: " + hits)
            file_object.write("\n")

        file_object.write(str(timestamp) + " CHATBOT: " + response[1])
        file_object.write("\n")
    if mode == 0:
        file_object.write(str(timestamp) + " USER: " + response)
        file_object.write("\n")
        
    file_object.close()


def checkSubString(user_input):
    global imgname

    formattedString = user_input.lower()

    for items in triggers:
        if items in formattedString:
            imgname = os.path.join(app.config["UPLOAD_FOLDER"], (items + ".png"))
            return imgname
        else:
            imgname = ""


if __name__ == '__main__':
    app.run(use_reloader=False)
