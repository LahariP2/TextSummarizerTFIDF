import re
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
        self.path = path
        self.text = readFile(self.path)
        self.punctuation = set(['.', '?', '!'])
        self.symbols = set([':', ';', ',', '-'])
        self.fullText = readFile(path)
    
        self.stopWords = self.stopWordsIntoList()
        self.sentList = self.splitIntoSentences(self.text, self.symbols)
        self.wordsList = self.splitIntoWords(self.sentList, self.symbols)
        self.nonStopWords = self.getNonStopWords(self.wordsList, self.stopWords)
        
    # Converts the data in stop_words.txt to a string and returns them as a list of individual stop words
    def stopWordsIntoList(self):
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
        sentences = re.split(r'\. |\! |\!|\? |\?|\.|\n', fullText)
        for elem in sentences:
            if elem != '':
                elem = self.cleanWord(elem, symbols)
        return sentences

    # Returns an arry containing every word in the full text
    def splitIntoWords(self, sentences, symbols):
        words = list()
        for sent in sentences:
            words_in_sent = sent.split()
            for w in words_in_sent: 
                w = self.cleanWord(w, symbols)
                words.append(w)
        return words

    # Returns a list of all the words in the text that are not stop words
    def getNonStopWords(self, words, stopWords): 
        nonStopWords = list()
        for word in words: 
            if word not in stopWords:
                nonStopWords.append(word)
        return nonStopWords

    # Calculates and returns a dictionary for the TF of each word in the text
    # TF of each word = (number of times word appears in its sentence) / (total number of words in the sentence)
    def tfCalc(self, sentences):
        sentenceTfScores = dict()
        for sent in sentences:   
            wordList = sent.split()
            wordList = [element.lower() for element in wordList]
            for word in wordList:
                sentenceTfScores[word] = (sentenceTfScores.get(word, 0)) + (wordList.count(word)/len(wordList))
        
        for key in sentenceTfScores:
            sentenceTfScores[key] = (sentenceTfScores.get(key, 0)) / (self.wordsList.count(key))
        print(sentenceTfScores)
        return sentenceTfScores

    # Calculates and returns a dictionary for the IDF 
    # IDF of each word = (number of sentences) / (number of sentences that contain the word in document)
    def idfCalc(self, words, sentences): 
        documentIdfScores = dict()
        wordCount = 0
        for word in words:
            for sent in sentences: 
                wordList = sent.split()
                wordList = [element.lower() for element in wordList]
                wordCount += wordList.count(word)
            documentIdfScores[word] = math.log10((len(sentences))/wordCount)
            wordCount = 0

        for key in documentIdfScores:
            documentIdfScores[key] = (documentIdfScores.get(key, 0)) / (self.wordsList.count(key))
        print(documentIdfScores)
        return documentIdfScores

    def tfidfCalc(self, tf, idf):
        tfidf = dict()
        for word in self.wordsList:
            tfidf[word] = tf[word] * idf[word]
        print(tfidf)
        return tfidf
            

NLPDemo = PracticeNLP('test_text.txt')
tf_dict = NLPDemo.tfCalc(NLPDemo.sentList)
idf_dict = NLPDemo.idfCalc(NLPDemo.wordsList, NLPDemo.sentList)
NLPDemo.tfidfCalc(tf_dict, idf_dict)
