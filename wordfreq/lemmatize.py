#!/usr/bin/python2.5

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus.reader import VERB
from nltk.corpus.reader import NOUN
from sys import stdin, argv

if len(argv) == 2:
    splitby = eval(argv[1])
else:
    splitby = '\t'

lemmatizer = WordNetLemmatizer()

#
# we assume the file is built of pos/word pairs, optionally followed by a number
#

for line in stdin:
    words = line.rstrip().split(splitby)
    poswords = list((words[2*i], words[2*i+1]) for i in range(len(words)/2))

    append = []

    for (pos, word) in poswords:
        if pos.lower().startswith("v"):
            append.append(lemmatizer.lemmatize(word, VERB))
        elif pos.lower().startswith("n"):
            append.append(lemmatizer.lemmatize(word, NOUN))
        else:
            append.append(word)

    if len(words) > (len(words) / 2) * 2:
        append.append(words[-1])
        words = words[:-1]

    print splitby.join(words + append)
            

