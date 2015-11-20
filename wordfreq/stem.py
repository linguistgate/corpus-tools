#!/usr/bin/python2.5

from nltk.stem.porter import PorterStemmer
from sys import stdin, argv

if len(argv) == 2:
    splitby = eval(argv[1])
else:
    splitby = '\t'

porter = PorterStemmer()

for line in stdin:
    words = line.rstrip("\n").rstrip("\r").rstrip("\n").split(splitby)

    append = []

    for i in range(len(words)):
        append.append(porter.stem(words[i]))

    print splitby.join(words + append)
            

