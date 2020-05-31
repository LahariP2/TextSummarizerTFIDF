import re
text_file = open("test_text.txt", "r")

s = text_file.read()


def split_by_sentence():
    print(s)
    p = s.replace('\n', '')
    print(p)
    re.split(r'. |, |! |? ', p)
    

split_by_sentence()

