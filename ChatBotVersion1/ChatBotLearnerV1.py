import random
import pickle
import string
import fileinput
from itertools import combinations
import nltk
from nltk.tokenize import word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


#Function: Learn from Training Data
def learnData():
    r = open("chatbotTrainingDataV2","r")
    data = []
    curData = []
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

    newKnowledge = {}
    newSecondary = {}
    for convo in data:
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
        for group in userMSG:
            if word in nouns or word in adj_adv:
                if word in newKnowledge:
                    newKnowledge[word].append(botMSG)
                else:
                    newKnowledge[word] = [botMSG]
            elif word in others:
                if word in newSecondary:
                    newSecondary[word].append(botMSG)
                else:
                    newSecondary[word] = [botMSG]
     
    known = loadKnowledge()
    known = known | newKnowledge
    saveKnowledge(known)

    secondary = loadSecondary()
    secondary = secondary | newSecondary
    saveSecondary(secondary)
    print("Data Processed")
            
#Functions: Get Combinations of Keywords
def getKeywordCombinations(keywords):
    combs = []
    for i in range(len(keywords)+1):
        c = [combinations(keywords,i)]
        for j in c:
            j.sort()
            combs.append(j)
    return combs


#Function: Learn Conversation Through Talking
def learner():
    newKnowledge = {}
    basicGreetings = ["Hi","Hello!"]
    while True:
        toSend = random.randint(0,len(basicGreetings)-1)
        print(basicGreetings[toSend])
        userMSG = str(input())
        if userMSG == "2023":
            known = loadKnowledge()
            known = known | newKnowledge
            saveKnowledge(known)
            print("Saved. Quitting.")
            return
        if userMSG.strip() not in basicGreetings:
            basicGreetings.append(userMSG.strip())
        if basicGreetings[toSend] in newKnowledge:
            newKnowledge[basicGreetings[toSend]].append(userMSG.strip())
        else:
            newKnowledge[basicGreetings[toSend]] = [userMSG.strip()]
        
        botMSG = basicGreetings[toSend]
        POS_tagging(botMSG)
        botMSG = tokenize_stopwords(botMSG)
        
        for word in botMSG:
            if word in newKnowledge:
                newKnowledge[word].append(userMSG)
            else:
                newKnowledge[word] = [userMSG]

#Function: Part-Of-Speech Tagging
def POS_tagging(sentence):
    # Tokenize the input sentence
    tokens = word_tokenize(sentence)
    
    # Perform POS tagging
    pos_tags = nltk.pos_tag(tokens)
    
    # Create an empty dictionary to store the results
    pos_dict = {}
    
    # Iterate through the POS tagged words
    for word, pos in pos_tags:
        # Add the word to the corresponding list for its POS tag
        if pos in pos_dict:
            pos_dict[pos].append(word)
        else:
            pos_dict[pos] = [word]
    
    return pos_dict
  



#Function: Save Knowledge
def saveKnowledge(toSave):
    filename = "chatbotV1Storage.pk"
    with open(filename, 'wb') as save:
        pickle.dump(toSave, save)
    return

#Function: Save Secondary
def saveSecondary(toSave):
    filename = "chatbotV1StorageSecondary.pk"
    with open(filename,'wb') as save:
        pickle.dump(toSave,save)
    return

#Function: Load Knowledge
def loadKnowledge():
    filename = "chatbotV1Storage.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Load Secondary
def loadSecondary():
    filename = "chatbotV1StorageSecondary.pk"
    with open(filename,"rb") as load:
        known = pickle.load(load)
    return known

#Function: Show Learning
def showLearning():
    filename = "chatbotV1Storage.pk"
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
    filename = "chatbotV1Storage.pk"
    with open(filename, 'wb') as save:
        pickle.dump({}, save)

    filename = "chatbotV1StorageSecondary.pk"
    with open(filename, 'wb') as save:
        pickle.dump({}, save)
    return

def backUpCurrentKnowledge(toSave):
    filename = "chatbotV1StorageBackup.pk"
    with open(filename, 'wb') as save:
        pickle.dump(toSave, save)
    return

learnData()
print(loadKnowledge())
print(loadSecondary())
