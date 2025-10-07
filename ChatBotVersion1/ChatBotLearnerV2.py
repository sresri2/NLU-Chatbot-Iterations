import random
import pickle
import string
import fileinput
from itertools import combinations
import nltk
import spacy

from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


#Function: Learn from Training Data
def learnData():
    r = open("chatbotTrainingDataV3","r")
    data = []
    curData = []
    prev = ""
    c = 1
    while True:
        line = r.readline().strip()
        if line == "":
            if curData == []:
                break
            data.append(curData)
            curData = []
        else:
            if len(curData) == 0:
                line = line[6:]
                curData.append(line)
            elif len(curData) == 1:
                line = line[9:]
                curData.append(line)
        prev = line
        print(c)
        c+=3

    newKnowledge = {}
    newSecondary = {}
    c = 1
    for convo in data:
        print(c)
        userMSG = convo[0]
        botMSG = convo[1]

        pos_tag = POS_tagging(userMSG)
        nouns = set()
        adj_adv = set()
        others = set()
        mainKeywords = []

        for words in list(pos_tag.keys()):
            if words[0] == "N":
                for word in pos_tag[words]:
                    nouns.add(word)
                    mainKeywords.append(word)
            elif words[0] == 'A':
                for word in pos_tag[words]:
                    adj_adv.add(word)
                    mainKeywords.append(word)
            else:
                for word in pos_tag[words]:
                    others.add(word)


        userMSG = tokenize_stopwords(userMSG)
        pos = 0
        stemmer = PorterStemmer()
        for i in userMSG:
            userMSG[pos] = userMSG[pos].lower()
            userMSG[pos] = stemmer.stem(userMSG[pos])
            pos += 1

        userMSG = getKeywordCombinations(userMSG)
        for group in userMSG:
            g = tuple(i for i in group)
            if g in newKnowledge:
                newKnowledge[g].append(botMSG)
            else:
                newKnowledge[g] = [botMSG]
        
        c += 1
     
    known = loadKnowledge()
    known = known | newKnowledge
    saveKnowledge(known)

    #secondary = loadSecondary()
    #secondary = secondary | newSecondary
    #saveSecondary(secondary)
    print("Data Processed")
            
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

#Function: Part-Of-Speech Tagging
def POS_tagging(sentence):
    # Tokenize the input sentence
    tokens = word_tokenize(sentence)
    
    # Perform POS tagging
    pos_tags = pos_tag(tokens)
    
    # Initialize empty lists for nouns and adjectives
    nouns = []
    adjectives = []
    
    # Iterate through the POS tagged words
    for word, pos in pos_tags:
        if pos.startswith('N'):  # Noun POS tags start with 'N'
            nouns.append(word)
        elif pos.startswith('J'):  # Adjective POS tags start with 'J'
            adjectives.append(word)
    
    return nouns, adjectives
  



#Function: Save Knowledge
def saveKnowledge(toSave):
    filename = "chatbotV3Storage.pk"
    with open(filename, 'wb') as save:
        pickle.dump(toSave, save)
    return

#Function: Save Secondary
def saveSecondary(toSave):
    filename = "chatbotV3StorageSecondary.pk"
    with open(filename,'wb') as save:
        pickle.dump(toSave,save)
    return

#Function: Load Knowledge
def loadKnowledge():
    filename = "chatbotV3Storage.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Load Secondary
def loadSecondary():
    filename = "chatbotV3StorageSecondary.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Show Learning
def showLearning():
    filename = "chatbotV3Storage.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    print(known) 
    return

#Function: Tokenize String and Remove Stop Words
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
    
def cleanUp(knowledge):
    for i in list(knowledge.keys()):
        newList = []
        [newList.append(x) for x in knowledge[i] if x not in newList]
        knowledge[i] = newList.copy()
        newList = []

def resetKnowledge():
    filename = "chatbotV3Storage.pk"
    with open(filename, 'wb') as save:
        pickle.dump({}, save)

    filename = "chatbotV3StorageSecondary.pk"
    with open(filename, 'wb') as save:
        pickle.dump({}, save)
    return

def backUpCurrentKnowledge(toSave):
    filename = "chatbotV3StorageBackup.pk"
    with open(filename, 'wb') as save:
        pickle.dump(toSave, save)
    return

resetKnowledge()
learnData()
#print(loadKnowledge())
#print(loadSecondary())
