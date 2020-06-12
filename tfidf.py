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
    def __init__(self, articlePath, stopWordsPath):
        self.punctuation = set(['.', '?', '!'])
        self.symbols = set([':', ';', ',', '-'])
        self.fullTextAsString = readFile(articlePath)
    

        # Used at the end during summarization
        self.originalSentencesList = self.splitIntoSentences(self.fullTextAsString, self.symbols)


        # Used to calculated sentence and word scores
        self.sentencesList = self.lowerCaseSentences(self.originalSentencesList)
        self.allWordsList = self.splitIntoWords(self.sentencesList, self.symbols)

        self.stopWordsList = self.stopWordsIntoList(stopWordsPath)
        self.nonStopWordsList = self.getNonStopWords(self.allWordsList, self.stopWordsList)
        


    # Method called to summarize document
    def summarize(self): 
        tfDict = self.calculateTF(self.sentencesList, self.nonStopWordsList)
        idfDict = self.calculateIDF(self.nonStopWordsList, self.sentencesList)
        tfidfDict = self.multiplyTFIDF(self.nonStopWordsList, tfDict, idfDict)
        sentenceScoresDict = self.scoreSentences(self.sentencesList, self.nonStopWordsList, tfidfDict)
        averageScore = self.averageSentScores(sentenceScoresDict)
        self.printSummary(averageScore, sentenceScoresDict, self.sentencesList, self.originalSentencesList)

    # Returns an array containing the text split into sentences. First letter capitalization is retained. 
    def splitIntoSentences(self, fullText, symbols):
        sentences = re.split(r'\. |\; |\;|\! |\!|\? |\?|\.', fullText)
        for sentence in sentences:
            if sentence != '':
                sentence = self.cleanWord(sentence, symbols)
        sentences.pop() # Remove last element which is an empty string 
        return sentences

    # Returns an array containing the text split into sentences. All sentences in lower case. 
    def lowerCaseSentences(self, originalSentence):
        sentencesLowered = list()
        for sentence in originalSentence: 
            sentence = sentence.lower()
            sentencesLowered.append(sentence)
        return sentencesLowered

    # Cleans and returns the individual word without unneccessary punctuation
    def cleanWord(self, word, symbols):
        charList = list(word)
        newCharList = []
        for char in charList:
            if char not in symbols:
                newCharList.append(char)
        word = ''.join(newCharList)
        return word

    # Returns an array containing every word in the full text
    def splitIntoWords(self, sentences, symbols):
        words = list()
        for sent in sentences:
            # Split by : Also because otherwise this is leading to problems in idf calculation
            wordsInSent = re.split(r'\:|\: |\s+', sent)
            for w in wordsInSent: 
                w = self.cleanWord(w, symbols) 
                words.append(w)

        return words

    # Converts the data in stop_words.txt to a string and returns them as a list of individual stop words
    def stopWordsIntoList(self, stopWordsPath):
        stopwordsString = readFile(stopWordsPath)
        return stopwordsString.split()

    # Returns a list of all the words in lower case in the text that are not stop words
    def getNonStopWords(self, allWords, stopWords): 
        nonStopWords = list()
        for word in allWords: 
            if word not in stopWords:
                nonStopWords.append(word)
        return nonStopWords

    # Calculates and returns a dictionary for the TF of each word in the text
    # TF of each word = (number of times word appears in its sentence) / (total number of words in the sentence)
    def calculateTF(self, sentences, nonStopWords):
        sentenceTfScores = dict()
        for sent in sentences:   
            # Used above function to split based on other punctuation not only spaces
            temp = list()
            temp.append(sent)
            wordsInSent = self.splitIntoWords(temp, self.symbols)
            for word in wordsInSent:
                # Added this condition to make sure there is no divide by 0 issue when the word is a stop word
                if (word in nonStopWords): 
                    sentenceTfScores[word] = (sentenceTfScores.get(word, 0)) + (wordsInSent.count(word)/len(wordsInSent))
        
        # Average the TF of each word based on the number of occurences of each word in a sentence
        for key in sentenceTfScores:
            sentenceTfScores[key] = (sentenceTfScores.get(key, 0)) / (nonStopWords.count(key))

        return sentenceTfScores

    # Calculates and returns a dictionary for the IDF 
    # IDF of each word = (number of sentences) / (number of sentences that contain the word in document)
    def calculateIDF(self, nonStopWords, sentences): 
        documentIdfScores = dict()
        wordCount = 0
        for word in nonStopWords:
            for sent in sentences: 
                # Used above function to split based on other punctuation not only spaces
                temp = list()
                temp.append(sent)
                wordsInSent = self.splitIntoWords(temp, self.symbols)
                wordCount += wordsInSent.count(word)

            documentIdfScores[word] = math.log10((len(sentences))/wordCount)
            wordCount = 0

        # Average the TF of each word based on the number of occurences of each word in the document
        for key in documentIdfScores:
            documentIdfScores[key] = (documentIdfScores.get(key, 0)) / (nonStopWords.count(key))

        return documentIdfScores

    def multiplyTFIDF(self, words, tf, idf):
        tfidf = dict()
        for word in words:
            tfidf[word] = tf[word] * idf[word]
        return tfidf
            
    def scoreSentences(self, sentences, nonStopWords, tfidf):
        sentenceScores = dict()
        for sentence in sentences:
            sentScore = 0
            # Used above function to split based on other punctuation not only spaces
            temp = list()
            temp.append(sentence)
            wordsInSent = self.splitIntoWords(temp, self.symbols)
            for word in wordsInSent: 
                # Added this condition to make sure there is no divide by 0 issue for TF when the word is a stop word 
                if (word in nonStopWords):
                    sentScore += tfidf[word]

            sentenceScores[sentence] = sentScore / len(wordsInSent)
            sentScore = 0
        return sentenceScores

    def averageSentScores(self, sentenceScoresDict): 
        sum = 0
        for key in sentenceScoresDict: 
            sum += sentenceScoresDict[key]
        average = sum / len(sentenceScoresDict)
        return average

    def printSummary(self, averageScore, sentScoresDict, scoringSentences, originalSentences): 
        counter = 0
        for sent in scoringSentences: 
            if (sentScoresDict[sent] >= averageScore):
                print(originalSentences[counter])
            counter += 1

NLPDemo = PracticeNLP('test_text.txt', 'stop_words.txt')
NLPDemo.summarize()