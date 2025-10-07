#Chat Bot V2
'''
Natural Language Processing
- Keyword Groups matched to Responses from Learner
'''
import pickle
import string
from collections import Counter
from itertools import combinations
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')

class ChatBot:
    #Function: Find appropriate Response
    def getResponse(userMSG,knowledge):
        userMSG = ChatBot.tokenize_stopwords(userMSG)
        pos = 0
        stemmer = PorterStemmer()
        for i in userMSG:
            userMSG[pos] = userMSG[pos].lower()
            userMSG[pos] = stemmer.stem(userMSG[pos])
            pos += 1

        userMSG = ChatBot.getKeywordCombinations(userMSG)
        userMSG = sorted(userMSG,key=len,reverse=True)
        possibleResponses = []
        for group in userMSG:
            g = tuple(i for i in group)  
            if len(g) > 0:
                if g in knowledge:
                    possibleResponses += knowledge[g]
        if len(possibleResponses) == 0:
            return "NONE"
        
        mostFrequentResponse = max(set(possibleResponses), key=possibleResponses.count)
        
        return mostFrequentResponse


    #Functions: Get Combinations of Keywords
    def getKeywordCombinations(keywords):
        combs = []
        for i in range(1,len(keywords)+1):
            c = list(combinations(keywords,i))
            for j in c:
                if len(j) > 0:
                    j = sorted(j)
                    combs.append(j)
        return combs

    #Function: Load Stored Knowledge Dictionary
    def loadKnowledge():
        filename = "chatbotV3Storage.pk"
        with open(filename,"rb") as load:
            known = pickle.load(load)
        return known

    #Function: Load Secondary Knowledge
    def loadSecondary():
        filename = "chatbotV3StorageSecondary.pk"
        with open(filename,"rb") as load:
            known = pickle.load(load)
        return known

    #Function: Tokenize User Message and Remove Stop Words
    def tokenize_stopwords(message):
        message = message.translate(str.maketrans('', '', string.punctuation))
        message = message.split()

        pos = 0
        stop_words = ChatBot.getStopWords()

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
        knowledge = ChatBot.loadKnowledge()
        #secondary = ChatBot.loadSecondary()
        while True:
            userMSG = str(input())
            userMSG = userMSG.strip()
            if userMSG == "2023":
                print("Quitting")
                break
            
            response = ChatBot.getResponse(userMSG,knowledge)

            '''
            if response == "NONE":
                response = ChatBot.getResponse(userMSG)
                if response == "NONE":
                    print("Sorry, I didn't understand that.")
                    break
            '''
            if response == "NONE":
                print("I'm sorry, could you try rephrasing your question another way?")
            else:
                print(response)
        return


ChatBot.init()
