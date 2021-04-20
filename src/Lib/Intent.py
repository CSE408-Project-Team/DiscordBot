
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import pandas as pd
import pickle
import random
import json
from typing import List


stemmer = LancasterStemmer()

with open("./src/Lib/Intents.json") as file:
    data = json.load(file)


words = []
labels = []
docs = []
ignoreWords = ["?"]

# Prepare the data into their corresponding lists
for intent in data['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        docs.append((w, intent['tag']))

        if intent['tag'] not in labels:
            labels.append(intent['tag'])


# Stem words (get root of word)
words = [stemmer.stem(w.lower()) for w in words if w not in ignoreWords]

# Remove duplicates
words = sorted(list(set(words)))
labels = sorted(list(set(labels)))

print (len(docs), "documents")
print (len(labels), "labels", labels)
print (len(words), "unique stemmed words", words)


# Create the training set
training = []
outputEmpty = [0] * len(labels)

for doc in docs:
    bag = []
    patternWords = doc[0]

    # Stem (root word) of every word
    patternWords = [stemmer.stem(word.lower()) for word in patternWords]
    for w in words:
        bag.append(1) if w in patternWords else bag.append(0)
    
    outputRow = list(outputEmpty)
    outputRow[labels.index(doc[1])] = 1
    
    training.append([bag, outputRow])

random.shuffle(training)
training = numpy.array(training)
trainX = list(training[:,0])    # Patterns
trainY = list(training[:,1])    # Intents 


# Create a Model with 3 layers
model = Sequential()
model.add(Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
# Softmax is conventionally used as the last activation function of a neural network
model.add(Dense(len(trainY[0]), activation='softmax'))

# Optimizer for model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(numpy.array(trainX), numpy.array(trainY), epochs=200, batch_size=5, verbose=1)


def clean(text: str):
    """
    Receives text and returns the tokenized and stemmed version of the text
    """
    sentenceWords = nltk.word_tokenize(text)
    sentenceWords = [stemmer.stem(word.lower()) for word in sentenceWords]
    return sentenceWords


def bagOfWords(text: str, words: List[str]):
    """
    Return the bagOfWords array for every word in the original bag that exists
    within the input text
    """
    sentenceWords = clean(text)
    bag = [0]*len(words)  
    for s in sentenceWords:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1

    return(numpy.array(bag))


def classifyText(text: str):
    
    inputData = pd.DataFrame([bagOfWords(text, words)], dtype=float, index=['input'])
    results = model.predict([inputData])[0]
    results = [[i,r] for i,r in enumerate(results) if r > 0.25]

    results.sort(key=lambda x: x[1], reverse=True)
    returnList = []
    for r in results:
        returnList.append((labels[r[0]], str(r[1])))
    
    return returnList


def getResponse(text: str):
    returnList = classifyText(text)
    print(returnList)
    responses = []
    
    for tag in data["intents"]:
        if tag["tag"] == returnList[0][0]:
            responses = tag["responses"]

    return random.choice(responses), float(returnList[0][1])

    




