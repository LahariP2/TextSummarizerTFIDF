import re
text_file = open("test_text.txt", "r")

s = text_file.read() 
p = s.replace('\n', '')

def split_by_sentence():

    all_sent = re.split(r'\. |\, |\! |\? |\.', p)
    all_sent.pop()

    return all_sent

def split_into_words():
    all_wrds = re.split(r'\. |\, |\! |\? |\.|\s+', p)
    all_wrds.pop()

    return all_wrds

def get_stop_words_into_list():
    with open('stop_words.txt') as f:
        stop_wrds = f.read().splitlines()
    return stop_wrds

def get_non_stop(all_wrds, stop_wrds): 
    non_stop_wrds = list()
    for s in all_wrds: 
        if s not in stop_wrds:
            non_stop_wrds.append(s)
    return non_stop_wrds
        

all_sentences = split_by_sentence()
print(all_sentences)
all_words = split_into_words()
print(all_words)

#stop_words = get_stop_words_into_list()
#non_stop_words = get_non_stop(all_words, stop_words)
#print(non_stop_words)
