import os
import os
import string
import collections

stopWords = ('ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 
    'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 
    'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 
    'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 
    'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 
    'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 
    'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 
    'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all',
    'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have',
    'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because',
    'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he',
    'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
    'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if',
    'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how',
    'further', 'was', 'here', 'than', '')

lexicon = dict()
with open('./src/Lib/wordWithStrength.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        words = line.split()
        if (len(words) == 2):
            lexicon[words[0]] = words[1]

def splitWords(wordlist):
    wordlist = list(wordlist.split())
    return list(map(lambda word: word.replace("/", " "), wordlist))

def parseWords(wordlist):
    out = "".join(c for c in str(wordlist) if c not in (string.punctuation))
    query = out.lower().split()
    return list(filter(lambda word: word not in stopWords, query))

def removeIntegers(wordlist):
    return list(filter(lambda word: not word.isdigit(), wordlist))

def bagify(wordlist):
    cleaned = removeIntegers(parseWords(splitWords(wordlist)))
    return list(filter(lambda word: word in lexicon, cleaned))

def sumScores(text):
    bow = bagify(text)
    score = 0
    for word in bow:
        score = score + float(lexicon[word])

    return score


def main():
    sumScores("sad depressing anger encephalitis terrible horrible")

if __name__ == "__main__":
    main()
