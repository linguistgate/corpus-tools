# try reparsing wsjtrees in a simpler way. 
from sys import stdin, stderr

def getId(tree):
    return tree[0]

def setId(tree, id):
    tree[0] = id

def getParent(tree):
    return tree[2]

def getDaughters(tree):
    return tree[1]

LATEX = {"[":"[", 
         "]":"]", 
         "T[":"]", 
         "T]":"]", 
         "box[":"\mbox{",
         "box]":"}",
         "protect[":"$",
         "protect]":"$",
         "\n":"\n",
         }

MRG = {"[":"(", 
       "]":")", 
       "T[":"", 
       "T]":"", 
       "box[":"", 
       "box]":"", 
       "protect[":"", 
       "protect]":"",
       "\n":"\n",
       }


def printTree(tree, indent="", annot=LATEX):

    def protect(name):
        if name.find("_") > 0:
            subs = name.split("_")
            name = subs[0]
            for sub in subs[1:]:
                name = "{"+name+"}_{"+sub+"}"
        return "".join([annot["box["], annot["protect["], 
                        name, 
                        annot["protect]"], annot["box]"]])



    if tree is None:
        return ""
    retlist = []
    if len(tree[1]) == 0:
        retlist += [indent, annot["T["], annot["box["], tree[0], annot["box]"], annot["\n"]]
        retlist.append(annot["T]"])
    else:
        retlist += [indent, annot["["], protect(tree[0]), annot["\n"]]
        retlist += [printTree(daughter, indent+" ", annot) for daughter in tree[1]]
        retlist.append(annot["]"])
    retlist.append(annot["\n"])
    #retlist = [indent, tree[0], " "]
    return "".join(retlist).replace(annot["\n"]+annot["]"], annot["]"])
        

def parseTreeFile(file=stdin):
    curr = None

    def startTree(word, curr):
        curr = ["", [], curr]
        #print " returning:", printTree(curr).replace("\n", "")
        #print >>stderr, "starting a tree"
        return curr

    def endTree(word, curr):
        #print >>stderr, "ending a tree", curr[0]
        curr[0] = "".join(curr[0])
        if not curr[2] is None:
            curr[2][1].append(curr)
        curr = curr[2]
        return curr

    def setName(word, curr):
        curr[0] += word
        #.rstrip("-0123456789")
        return curr

    terminal = False
    
    words = (word for word in "".join(line for line in file if not line.startswith("*") ) \
            .replace("(", " ( ").replace(")", " ) ").split())
    #words = list(words)
    #print >>stderr, words

    for word in words:
        #print >>stderr, "the word is", word, "and curr is", curr

        if word == "(":
            curr = startTree(word, curr)
            terminal = False                 # the next word is not a terminal
 
        elif word == ")":
            save = curr
            if terminal:
                curr = endTree(word, curr)   # it's a terminal so we should end it
            curr = endTree(word, curr)
            if curr is None:                 # we're at the top level so we should yield
                #print >>stderr, "we're at the top level, yielding" 
                if save[0] is "":
                    setName("ROOT", save)
                #print >>stderr, "start untrace", repr(save)
                untrace(save)
                #print >>stderr, repr(save)
                yield save
                save = None
            terminal = False                 # the next word is not a terminal

        else:
            if not terminal:
                terminal = True
            else:
                curr = startTree(word, curr) # it is a terminal: create a terminal node
            curr = setName(word, curr)
           
#tree = ("S", [("NP",[("John",[])]), ("VP",[("walks",[])])])
#print printTree(tree,"")

def untrace(tree):
    #print >>stderr, "untracing", repr(tree)
    for d in tree[1]:
        untrace(d)

    if len(tree[1]) > 0:
        tree[0] = tree[0].rstrip("-0123456789")
    elif len(tree[1]) == 0 and tree[0].startswith("*"):
        try:
            tree[2][1].remove(tree)
            if len(tree[2][1]) == 0:
                tree[2][0] = "*"
        except TypeError:
            print >>stderr, tree[0], repr(tree[2])
            raise TypeError("trying to remove a tree that has nothing but traces")
        

def binarize(tree, heads={"S":["NP-SBJ"], "ADJP":["JJ"]}):
    
    if len(tree[1]) == 0:
        return

    if len(tree[1]) > 2:
        head = -1
        daughterIndex = -1
        for daughter in tree[1]:
            daughterIndex += 1
            if tree[0] in heads:
                if daughter[0] in heads[tree[0]]:
                    head = daughterIndex
                    break
            else:
                if daughter[0][0] == tree[0][0]:
                    head = daughterIndex
                    break

        if head == -1:
            print >>stderr, "applying default rule for '"+tree[0]+"'", \
                "daugheters", " ".join(d[0] for d in tree[1])
            head = 0
        #head = tree[1][head]
                                  

        barename = tree[0].split("_")[0]
        if head > 0:
            newtree = ["".join(["",
                                barename,
                                "_",
                                ",".join([tree[1][1][0], 
                                          tree[1][head][0]
                                          ]),
                                ""]), 
                       tree[1][1:],
                       tree]
            tree[1] = [tree[1][0], newtree]
        else:
            newtree = ["".join(["",
                                barename,
                                "_"+
                                ",".join([tree[1][head][0], tree[1][-2][0]]),
                                ""]), 
                       tree[1][:-1],
                       tree]
            tree[1] = [newtree, tree[1][-1]]

    for daughter in tree[1]:
        binarize(daughter)

    if len(tree[1]) == 1 and len(tree[1][0][1]) > 0:
        tree[0] = tree[0] + ">" + tree[1][0][0]
        tree[1] = tree[1][0][1]


def debinarize(tree):
    
    def reunarize(tree):
        firstBranch = tree[0].find(">")
        if firstBranch > -1:
            newtree = [tree[0][firstBranch+1:], tree[1], tree]
            tree[1] = [newtree]
            tree[0] = tree[0][:firstBranch]

        for daughter in tree[1]:
            reunarize(daughter)

    def multirize(tree): 
        for daughterI in range(len(tree[1])):
            daughter = tree[1][daughterI]
            multirize(daughter)
            if daughter[0].find("_") > -1:
                tree[1] = tree[1][:daughterI] + \
                    daughter[1][:] + \
                    tree[1][daughterI+1:]
            


    reunarize(tree)
    multirize(tree)


def duplicate(tree):
    ret = [tree[0], []]
    for daughter in tree[1]:
        ret[1].append(duplicate(daughter))
        ret[1][-1].append(ret)
    if tree[2] is None:
        ret.append(None)
    return ret


def equal(tree1, tree2):
    ret = tree1[0] == tree2[0] and \
        len(tree1[1]) == len(tree2[1])

    for d1, d2 in ((tree1[1][i], tree2[1][i]) \
                       for i in range(len(tree1[1])) if ret):
        ret &= equal(d1, d2)

    return ret

def terminals(tree):
    if len(tree[1]) == 0:
        yield tree[0]
    else:
        for daughter in tree[1]:
            for terminal in terminals(daughter):
                yield terminal

def preterminals(tree):
    if len(tree[1]) == 0:
        pass
    elif len(tree[1][0][1]) == 0:
        yield tree[0]
    else:
        for daughter in tree[1]:
            for preterminal in preterminals(daughter):
                yield preterminal


if __name__ == "__main__":


    print "\\documentclass{article}"
    print "\\usepackage[margin=0.5in,landscape]{geometry}"
    print "\\usepackage{synttree}"
    print "\\begin{document}"
    for tree in parseTreeFile():
        #tree = tree[1][0]
        print "\\synttree"+printTree(tree)
        print " "

        binTree = duplicate(tree)
        print >>stderr, "dup=orig?", equal(binTree, tree)
        binarize(binTree)
        print >>stderr, "bin=orig?", equal(binTree, tree)
        print "\\synttree"+printTree(binTree)
        print " "

        unTree = duplicate(binTree)
        debinarize(unTree)
        print >>stderr, "unbin=bin?", equal(binTree, unTree)
        print >>stderr, "unbin=orig?", equal(unTree, tree)
        print "\\synttree"+printTree(unTree)
        print " "
    print "\\end{document}"
