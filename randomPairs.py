#!/usr/bin/python
# M.E. Adams, 5 Aug 2011

# Creates set of questionnaire files. Use NFORMS variable to
# change this number. Ensures that each questionnaire will have
# a random sampling (without replacement) from input files. Zero
# overlap between conditions on any one questionnaire.

import os
from random import choice, sample, shuffle
from fopen import fopen

target_dir = './questionnaires'

try:
    os.makedirs('./questionnaires')
except OSError:
    pass

NFORMS = 20

synthetic = [line.strip() for line in fopen("boyd-stimuli_1.txt")]
analytic = [line.strip() for line in fopen("boyd-stimuli_2.txt")]
fillers = [line.strip() for line in fopen("fillers1.txt")]

syntheticDict = {}
for ind, item in enumerate(synthetic):
    syntheticDict[item] = ind
analyticDict = {}
for ind, item in enumerate(analytic):
    analyticDict[item] = ind

for i in range(NFORMS):
    i += 1
    filename = str("questionnaire" + str(i) + ".txt")
    fullname = os.path.join(target_dir,filename)
    print "Writing to file %s" % fullname
    
    stimuli = []
    avalues = []
    
    randAnalytic = sample(analytic, 9) # without replacement

    file = open(fullname, 'w')
    for a in randAnalytic:
        avalues.append(str(analyticDict[a]))
        stimuli.append(a)
    for s in synthetic:
        if str(syntheticDict[s]) not in avalues:
            stimuli.append(s)
    for f in fillers:
        stimuli.append(f)
    shuffle(stimuli)
    file.write("\n".join(stimuli))
    file.close()

# May want to modify so that fillers are evenly interspersed
# between A and S.
