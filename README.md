# Chatbot-Caetennia
Chatbot project ICLON - OU - Rijksmuseum van Oudheden

This repository contains code to interact with a chatbot that was developed for the Rijksmuseum van Oudheden in Leiden.

**Scripts**

*chatbot.py*
--> Generates a dialogue with the chatbot.

*json-formatting.py*
--> Converts tab-separated .txt-file into json-format, which the chatbot takes as input.

**Folders**

*data*
--> This folder contains two files:
  - "LitOnderzoek.txt": a database of questions and answers, categorized by topic.
  - "QandAdata.json": the same content as the file above, but converted into JSON format using the script json-formatting.py.

*word-embeddings*
--> Users should create this folder and place a Dutch word embedding model in it, which can be retrieved from https://github.com/clips/dutchembeddings. We use "wikipedia-160.txt".
