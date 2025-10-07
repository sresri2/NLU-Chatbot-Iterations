#Chat Bot V1
import pickle
import string
from collections import Counter
from itertools import combinations


#Function: Find appropriate Response
def getResponse(userMSG,knowledge):
    userMSG = tokenize_stopwords(userMSG)
    possibleResponses = []
    for word in userMSG:
        if word in knowledge:
            possibleResponses += knowledge[word]
    if len(possibleResponses) == 0:
        return "NONE"
    mostFrequentResponse = max(set(possibleResponses), key=possibleResponses.count)
    return mostFrequentResponse



#Function: Group Keywords:
#Functions: Get Combinations of Keywords
def getKeywordCombinations(keywords):
    combs = []
    for i in range(len(keywords)+1):
        c = [combinations(keywords,i)]
        for j in c:
            j.sort()
            combs.append(j)
    return combs



#Function: Load Stored Knowledge Dictionary
def loadKnowledge():
    filename = "chatbotV1Storage.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Load Secondary Knowledge
def loadSecondary():
    filename = "chatbotV1StorageSecondary.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Tokenize User Message and Remove Stop Words
def tokenize_stopwords(message):
    message = message.translate(str.maketrans('', '', string.punctuation))
    message = message.split()

    pos = 0
    stop_words = getStopWords()

    while pos < len(message):
        if len(message) == 0 or pos>= len(message):break
        if message[pos] in stop_words:
            del(message[pos])
        else:
            pos += 1
    return message
        

#Function: Read Stop Words from File
def getStopWords():
    r = open("stop_words","r")
    stop_words = set()
    while len(stop_words) < 162:
        word = r.readline()
        word = word.strip()
        stop_words.add(word)
    return stop_words


#Function: main
def init():
    print("Starting Conversation:")
    knowledge = loadKnowledge()
    secondary = loadSecondary()
    while True:
        userMSG = str(input())
        userMSG = userMSG.strip()
        if userMSG == "2023":
            print("Quitting")
            break
        
        response = getResponse(userMSG,knowledge)
        if response == "NONE":
            response = getResponse(userMSG,secondary)
            if response == "NONE":
                print("Couldn't get Response.")
                break
        print(response)
    return


init()


