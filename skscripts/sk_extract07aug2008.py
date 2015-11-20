#!/usr/bin//python

# Some comments to describe file's purpose.

from sys import stdin, stderr

import re

REPLACES = dict([("\x02\x05", "("),
                 ("\x02\x06", ")")])

HEADERS = ("CHILD_ID", 
           "SPEAKER",
           "TARGET_SENTENCE",
           "TARGET_VERB",
           "FILE_NAME",
           "LINE_ID",
           "CONTEXT",
           )

print "\t".join(HEADERS)

contextDict = dict()

fileprops = dict()
printlist = []

#file1 = open("chi.2.0.2.6.get.txt")
#file1 = open(stdin)


##
# contstructs total context - which extracts all lines starting with
#'*' or '@' and makes a hugh list of the lines.
##

context = []
localContext = []

#x = 7
#y = 24
x = 1     # needs to be changed according to the input file
y = 12

for line in stdin:
    line = line.strip() 
    lineSplited = line.split("\x15") #This removes the movie tag info.
    line = lineSplited[0]
    line = line.replace("\t", " ")

    if line.startswith('*'):
    	context.append(line)
    else:
    	if line.startswith('@'):
    		context.append(line)
    	else:
    		if len(context) > 0:
    			tmpList = context.pop()
    			tmpList += line
    			context.append(tmpList)
    # HAVE TO DEAL WITH @END CASE!!!	


for line in context:
    line = line.strip()    

    ##
    # Extracts directory info, file name, and line number of target code
    ##
    if re.findall(r"\*\*\*\s[A-Z]", line):
        fileprops = dict()
        filepath = line
        directory = filepath.split("\\")
        #childName = directory[4]
                
        fileinfo = directory[4].split(":")
        fileName = fileinfo[0].replace("\"", "")
        lineInfo = fileinfo[1].replace(".", "").replace(" l", "l")
        fileprops["FILE_NAME"] = fileName
        fileprops["LINE_ID"] = lineInfo
        
    # Defines the body as the part of the file that has a speaker tag
    # (MOT:, CHI:). 
    ##
        	
    if re.findall(r"^\*[A-Z]", line):
        speakerAndUtterance = line.split(":",1)
        
        speaker = speakerAndUtterance[0]
        utterance = speakerAndUtterance[1]

        #utterance = speakerAndUtterance[1].split("\x15") #This removes the movie tag info.
        #utterance = utterance[0]
        
        #if len(re.findall(r"\(\d\)", utterance)) > 1:
        #    stderr.write("More than one verb "+utterance+"\n")
        if len(re.findall(r"\(\d\)", utterance)) > 0:
            
            fields = dict(fileprops)  # we copy the file props into the new fields
            fields["CHILD_ID"] = fileName
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
            #x += 18
            #y += 18
            x += 11
            y += 11
            
            #print localContext

            #if fields["LINE_ID"] not in contextDict:
                #contextDict[fields["TARGET_SENTENCE"]] = localContext
            #else: 
            	#contextDict[fields["TARGET_SENTENCE"]] = localContext
            fields["CONTEXT"] = localContext

						
            #for verbMark in re.findall(r"\(\(\d\)\)", utterance):
            #    for verbStart in utterance.split(verbMark)[1:]: #omit pre-verb
            #    	currFields = dict(fields) # reduplicate all fields
            # 		currFields["TARGET_VERB"] = verbStart.split()[0]
            #    	printlist.append(currFields)	
            verbStart = utterance
            for verbMark in re.findall(r"\(\(\d\)\)", utterance):
            	verbStart = verbStart.split(verbMark, 1)[1]
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
    #fields["CONTEXT"] = contextDict[fields["TARGET_SENTENCE"]]
    print "\t".join(str(fields[h]) for h in HEADERS)
