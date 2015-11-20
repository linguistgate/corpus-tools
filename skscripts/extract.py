#!/usr/bin//python

# Some comments to describe file's purpose.

from sys import stdin, stderr

import re

REPLACES = dict([("\x02\x05", "("),
                 ("\x02\x06", ")")])

HEADERS = ("CHILD_ID", 
           "SPEAKER"
           "TARGET_SENTENCE",
           "TARGET_VERB",
           "FILE_NAME",
           "LINE_ID",
           "CONTEXT",
           )

print ",".join(HEADERS)

contextDict = dict()

fileprops = dict()
printlist = []

file1 = open("naima_get_all.txt")
file2 = open("naima_get_all.txt")

context = []
localContext = []
x = 8
y = 23

for line in file1:
    line = line.strip() 
    context.append[line]



for line in file2:
    line = line.strip()    
    
    ##
    # Extracts directory info, file name, and line number of target code
    ##
    if re.findall(r"\*\*\*\s[A-Z]", line):
        fileprops = dict()
        filepath = line
        directory = filepath.split("\\")
        childName = directory[4]
                
        fileinfo = directory[5].split(":")
        fileName = fileinfo[0].replace("\"", "")
        lineInfo = fileinfo[1].replace(".", "").replace(" l", "l")
        fileprops["FILE_NAME"] = fileName
        fileprops["LINE_ID"] = lineInfo

    # Defines the body as the part of the file that has a speaker tag
    # (MOT:, CHI:). 
    ##
    if re.findall(r"^\*[A-Z]", line):
        speakerAndUtterance = line.split("\t")
        
        speaker = speakerAndUtterance[0]
        
        #This is the part I'm concerned about in terms of splitting.
        #I use \x15, which uniquely identifies the beginning of the media tag
        #which SK wants removed -- but I don't think this is a good thing to
        #target.
        utterance = speakerAndUtterance[1].split("\x15") #This removes the movie tag info.
        utterance = utterance[0]
        
        #if len(re.findall(r"\(\d\)", utterance)) > 1:
        #    stderr.write("More than one verb "+utterance+"\n")
        if len(re.findall(r"\(\d\)", utterance)) > 0:
            #DICTIONARY CRAP
            fields = dict(fileprops)  # we copy the file props into the 
                                      # new fields
    
            fields["CHILD_ID"] = childName
	    fields["SPEAKER"] = speaker
            # done by the duplication:
            # fields["FILE_NAME"] = fileName 

            for rep in REPLACES:
                #print rep, REPLACES[rep], utterance
                utterance = utterance.replace(rep, REPLACES[rep])
                #print utterance

            targetFull = re.sub(r"\(\(\d\)\)", "", utterance)
            fields["TARGET_SENTENCE"] = targetFull 
	    
            localContext = context[x:y]
            x += 18
            y += 18

            if fields["TARGET_SENTENCE"] not in contextDict:
                contextDict[fields["TARTET_SENTENCE"]] = localContext
            else:
                contextDict[fields["TARTET_SENTENCE"]] = localContext

            for verbMark in re.findall(r"\(\(\d\)\)", utterance):
                for verbStart in utterance.split(verbMark)[1:]: #omit pre-verb
                    currFields = dict(fields) # reduplicate all fields
                    currFields["TARGET_VERB"] = verbStart.split()[0]
                    printlist.append(currFields)
            
            #print targetSentence
            # Here's where we need to be able to extract the verb from the
            # tagrget sentence
            
#    
            #printlist.append(fields)
#        
#
for fields in printlist:
    fields["CONTEXT"] = contextDict[fields["TARTET_SENTENCE"]]
    #print repr(fields)
    print "/t".join(str(fields[h]) for h in HEADERS)