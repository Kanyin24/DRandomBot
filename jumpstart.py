import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()



import tensorflow
import tflearn
import random
import numpy as np
import json

from tensorflow.python.framework import ops


with open("intents.json") as file:
    data=json.load(file)

words = []
labels = []
docsx = []
docsy = []

for intent in data["intents"]: #loops trough dict intents
    for pattern in intent["patterns"]:  # this is stemming it takes each word in pater and waters it down to the root word
        # example of stemming "what's up" -> "what"
        wrds = nltk.word_tokenize(pattern) # list of the words
        words.extend(wrds)
        docsx.append(wrds)
        docsy.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
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

ops.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])]) #definies input shape we are expecting
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training,output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")