import re
<<<<<<< HEAD
import math


# Convert data in file to a string
def readFile(path):
    with open(path, "rt") as f:
        text = f.read()
    return text

# Class to summarize text
class PracticeNLP(object):
    # Constructor to initialize variables
    def __init__(self, path):
        print("HIIIIIIIIIIIIIII")

        self.path = path
        self.text = readFile(self.path)
        self.punctuation = set(['.', '?', '!'])
        self.symbols = set([':', ';', ',', '-'])
        self.stopWords = self.stopWordsIntoList()
        self.sentList = self.splitIntoSentences(self.text, self.symbols)
        self.wordsList = self.splitIntoWords(self.sentList, self.symbols)
        self.nonStopWords = self.getNonStopWords(self.wordsList, self.stopWords)
        
    # Converts the data in stop_words.txt to a string and returns them as a list of individual stop words
    def stopWordsIntoList(self):
        print("STOP WORDS INTO LIST")
        stopwordString = readFile('stop_words.txt')
        return stopwordString.split()

    # Cleans and returns the individual word
    def cleanWord(self, word, symbols):
        word = word.lower()
        charList = list(word)
        newCharList = []
        for char in charList:
            if char not in symbols:
                newCharList.append(char)
        word = ''.join(newCharList)
        return word

    # Returns and array containing the text split into sentences
    def splitIntoSentences(self, fullText, symbols):
        print("SENTENCE SPLIT")

        sentences = re.split(r'\. |\! |\? |\.|\n', fullText)
        for elem in sentences:
            if elem != '':
                elem = self.cleanWord(elem, symbols)
        return sentences

    # Returns an arry containing every word in the full text
    def splitIntoWords(self, sentences, symbols):
        print("Words SPLIT")

        words = list()
        for sent in sentences:
            words = sent.split()
            for w in words: 
                self.cleanWord(w, symbols)
                words.append(w)
        return words

    # Returns a list of all the words in the text that are not stop words
    def getNonStopWords(self, words, stopWords): 
        print("NON ")
        nonStopWords = list()
        for word in words: 
            if word not in stopWords:
                nonStopWords.append(word)
        return nonStopWords

    # Calculates and returns a dictionary for the TF of each word in the text
    # TF of each word = (number of times word appears in its sentence) / (number of words in the sentence)
    def tfCalc(self, sentences):
        sentenceTfScores = dict()
        for sent in sentences:   
            wordList = sent.split()
            for word in wordList:
                sentenceTfScores[word] = wordList.count(word)/len(wordList)
        return sentenceTfScores

    # Calculates and returns a dictionary for the IDF 
    # IDF of each word = (number of sentences) / (number of sentences that contain the word)
    def idfCalc(self, words, sentences): 
        documentIdfScores = dict()
        wordCount = 0
        for word in words:
            for sent in sentences: 
                wordList = sent.split()
                wordCount += wordList.count(word)
            documentIdfScores[word] = math.log10(sentences.len()/wordCount)
            wordCount = 0
        return documentIdfScores

NLPDemo = PracticeNLP('test_text.txt')

NLPDemo.tfCalc(NLPDemo.sentList)
NLPDemo.idfCalc(NLPDemo.wordsList, NLPDemo.sentList)
=======
#tf = (frequency of the term in the doc/total number of terms in the doc)
#normalization of tf(average of duplicate tf scores/absolute word count in all docs)
#idf = ln(total number of docs/number of docs with term in it)
#info on tfidf from http://www.tfidf.com/ but all functions written by me

def readFile(path):
    with open(path, "rt") as f:
        text = f.read()
    return text

class PracticeNLP(object):
    def __init__(self, path):
        self.path = path
        self.text = readFile(self.path)
        self.punctuation = set(['.', '?', '!'])
        self.textList = []
        self.symbols = set([':', ';', ',', '-'])
    
    def removeStopwords(self):
        stopwordString = readFile('stop_words.txt')
        self.stopwordsList = stopwordString.split()

    def cleanWord(self, word):
        word = word.lower()
        charList = list(word)
        newCharList = []
        for char in charList:
            if char not in self.symbols:
                newCharList.append(char)
        word = ''.join(newCharList)
        return word

    def splitIntoSentences(self):
        dirtyList = re.split('\. |\! |\? |\.|\n', self.text)
        for elem in dirtyList:
            if elem != '':
                elem = self.cleanWord(elem)
                self.textList.append(elem)
    
    def tfCalc(self, sentence):
        sentenceTfScores = dict()
        wordList = sentence.split()
        for word in wordList:
            sentenceTfScores[word] = wordList.count(word)/len(wordList)
        return sentenceTfScores

NLPDemo = PracticeNLP('test_text.txt')
NLPDemo.removeStopwords()
NLPDemo.splitIntoSentences()
for sentence in NLPDemo.textList:
    print(NLPDemo.tfCalc(sentence))



>>>>>>> bdaaeda9dbc60e8434492f06b45b38f2db7e5c9b
