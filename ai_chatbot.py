import nltk
import tensorflow
import tflearn
import random
import numpy as np
import json
import pickle
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.python.framework import ops

stemmer = LancasterStemmer()

with open("intents.json") as file:
    data=json.load(file)
try:
    with open("data.pickle","rb") as f:
        words, labels, training, output=pickle.load(f)

except:
    words = []
    labels = []
    docsx = []
    docsy = []

    for intent in data["intents"]: #loops through dict intents
        for pattern in intent["patterns"]:  # this is stemming it takes each word in pater and waters it down to the root word
            # example of stemming "what's up" -> "what"
            wrds = nltk.word_tokenize(pattern) # list of the words
            words.extend(wrds)
            docsx.append(wrds)
            docsy.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words =sorted(list(set(words)))

    labels = sorted(labels)
    training = []  # will store multiple bags of words!
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docsx):
        bag=[]
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docsy[x])]=1

        training.append(bag)
        output.append(output_row)


    training = np.array(training)
    output = np.array(output)
    with open("data.pickle","wb") as f:
        pickle.dump( (words, labels, training,output),f)

ops.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])]) #definies input shape we are expecting
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training,output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(words.lower()) for words in s_words]

    for sen in s_words:
        for i, w in enumerate(words):
            if w==sen:
                bag[i]=1
    return np.array(bag)


def chat():
    response_str = ""
    print("talk to the bot type quit to stop")
    while True:
        inp=input("player: ")
        if inp.lower() == "quit":
            break
        results = model.predict([bag_of_words(inp,words)])
        result_index = np.argmax(results)
        tag = labels[result_index]
        for tg in data["intents"]:
            if tg["tag"] == tag:
                respones = tg["responses"]
        response_str += random.choice(respones)
        print(random.choice(respones))
