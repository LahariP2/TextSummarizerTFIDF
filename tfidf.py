import re
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



