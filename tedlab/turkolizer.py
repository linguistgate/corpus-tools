#! env python

#
#
#

import random, sys, csv


FILENAME = raw_input("Please enter the name of the text file: ")
# raw_input("Please enter the name of the text file: ")
# "itemsNewBigExpt3.txt"
# "itemsInFlow3.txt"
# "items.txt"
# "linger-test.txt"
# "items_SemPredNew.txt"

N = input("Please enter the desired number of lists: ") # multiple of Lcm
F = input("Please enter the desired number of in-between trials: ")  # number of in-between trials
Y = input("Please enter the desired number of fillers in the beginning of each list: ")

# ^*^*^ - creating a name for csv files from FILENAME - ^*^*^
FNAME = FILENAME.split("/")[-1]
FNAME = FNAME.split(".")[0]




#			     <<<<<<<< CLASSES >>>>>>>>>

class Trial:
    """contains the information about one trial as one string"""

    def __init__(self, trial):
	"""constructor"""
	self.allstring = trial
	self.lines = trial.splitlines()
	self.header = self.lines[0].split()
	self.exp  = self.header[0]
	self.item = self.header[1]
	self.cond = self.header[2]
	self.quest = []
	self.body  = []
	for line in self.lines[1:]:
	    if line[0] == '?':
		self.quest.append(line)
	    else:
		self.body.append(line)

    def get_all(self):
	"""returns the whole string"""
	return self.allstring

    def get_header(self):
	return self.header

    def get_body(self):
	"""returns the body of the trial (with line breaks included)"""
	body = ""
	for i in range(len(self.body)):
	    if i == len(self.body) - 1:
		body = body + self.body[i]
		break
	    body = body + self.body[i] + "<br/>"

	return body
	#return self.body

    def write_body(self, File):
	File.write('"')
	for i in range(len(self.body)):
	    File.write(self.body[i])
	    if i == len(self.body) - 1:
		continue
	    File.write("\n")

	File.write('",')
	return

    def get_lines(self):
	"""returns the trial as the list of lines"""
	return self.lines

    def get_quest(self):
	"""returns the list of questions and answers
	(each such cuple is a list)"""
	Q_list = []
	for Q_string in self.quest:
	    Q_string  = Q_string.strip("?")
	    Q_string  = Q_string.strip()
	    Q_string  = Q_string.split("?")
	    oneQ=[]
	    for string in Q_string:
		string = string.strip()
		oneQ.append(string)
	    Q_list.append(oneQ)
	return Q_list

    def get_exp(self):
	"""returns the name of the experiment
	this trial is from"""
	return self.exp

    def get_item(self):
	"""returns the iten this trial is from"""
	return self.item

    def get_cond(self):
	"""returns the name of condition of this trial"""
	return self.cond

    def get_keys(self):
	"""returns the key of this trial (item+condition),
	by this key the trial is stored in the dictionary-experiment"""
	return self.item + self.cond

class Experiment:
    """contains all the trials of one experiment as a dictionary,
    key for each trial is item + cond"""

    def __init__(self, trials):
	"""constructor"""
	self.trials = trials

	conditions = []
	for t in self.trials.keys():
	    if self.trials[t].get_cond() not in conditions:
		conditions.append(self.trials[t].get_cond())
	conditions.sort()
	self.conditions = conditions

	items = []
	for t in self.trials.keys():
	    if self.trials[t].get_item() not in items:
		items.append(self.trials[t].get_item())
	items.sort()
	self.items = items

    def get_trials(self):
	"""returns the whole dictionary of trials"""
	return self.trials

    def get_questNumb(self):
	"""returns the number of questions in a trial
	for the given experiment"""
	for trialKey in self.trials.keys():
	    return len(self.trials[trialKey].get_quest())
	    break

    def get_trialNumb(self):
	"""returns the number of trials in the experiment"""
	return len(self.trials)

    def get_condNumb(self):
	"""returns the number of conditions in the experiment"""
	return len(self.conditions)

    def get_itemNumb(self):
	"""returns the number of items in the experiment"""
	return len(self.items)

    def get_conds(self):
	"""returns the names of conditions in the experiment"""
	return self.conditions

    def get_items(self):
	"""returns the items of the experiment"""
	return self.items


#			<<<<<<<< FUNCTIONS >>>>>>>>>

#^*^*^*^ from primes.py ^*^*^
def gcd(a,b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
	a, b = b, a % b
    return a

def lcm(a,b):
    """Return lowest common multiple."""
    return (a*b)/gcd(a,b)

def LCM(terms):
    "Return lcm of a list of numbers."
    return reduce(lambda a,b: lcm(a,b), terms)
#^*^*^*^*^*^*^*^*^*^*^*^*^*^*^

#^*^*^*^ From Kevin Parks's recipe by korakot ^*^*^*
def w_choice(lst):
    n = random.uniform(0, 1)
    for item, weight in lst:
	if n < weight:
	    break
	n = n - weight
    return item
#^*^*^*^*^*^*^*^*^*^*^*^*^*^*^

# ^*^*^*^*^*^*^*^*^*^*^*^*^*^ finds out if a string contains another string
# ^*^*^*^*^*^*^*^*^*^*^*^*^*^ returns a boolean
def isThere(where, what):
    if where.find(what) == -1:
	return False
    return True





# ^*^*^*^*^*^*^*^*^*^*^*^*^ removes  the duplicates from the list ^*^*^*^*^*^
def clean_list(list):
    for item in list:
	value = item
	for i in range(list.count(value) - 1):
	    list.remove(value)
    return list

# ^*^*^*^*^*^*^*^*^*^*^*^*^ writes into the given file the elements of a given list ^*^*^
#			    separated by a comma and with a line break at the end   ^*^*^
def write_row(List, File):
    for i in range(len(List)):
	if i + 1 == len(List):
	    File.write(List[i]+"\n")
	else:
	    File.write(List[i]+",")
    return

#^*^*^*^*^*^*^*^*^*^*^*^*^ "rotates" a given list: puts the last value first ^*^*^*^
def rotate(L):
    value = L.pop()
    L.insert(0, value)
    return L

#^*^*^*^*^*^*^*^*^*^*^*^*^ generates keys for the trials from a given list ^*^*^
#			   of items and conditions			   ^*^*^
def generate_keys(items, conds) :
    keys = []
    ratio = len(items)/len(conds)
    for i in range(ratio):
	for j in range(len(conds)):
	    index = j + i*len(conds)
	    keys.append(items[index] + conds[j])
    return keys

# ^*^*^*^*^*^*^*^*^*^*^*^*^ returns a dict of exp (keys - names of  ^*^*^*^*^
#			    experiments, elements - dictionaries of ^*^*^*^*^
#			    trails with 'item number'+'cond number' ^*^*^*^*^
#			    as keys and trial-objects as elements:  ^*^*^*^*^
def getdata(filename):
    file = open(filename)
    all_string = file.read()
    trials = all_string.split("#")
    #^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^ gets rid of extra spaces:
    for i in range(len(trials)):
	trials[i] = trials[i].strip()
    #^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^ creates a list of trial-objects:
    trial_obj = []
    for trial in trials:
	try:
	    trial_obj.append( Trial(trial))
	except IndexError:
	    continue
    #^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^ creates a non-repeating list
    exp_names = []		#^*^*^ of exp names
    for t in trial_obj:
	exp_names.append(t.get_exp())
    exp_names = clean_list(exp_names)
    #^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^ creates the all inclusive dict itself:
    all_data = {}
    for exp in exp_names:
	exp_trials = {}
	for t in trial_obj:
	    if t.get_exp() == exp:
		exp_trials[t.get_item() + t.get_cond()] = t
	Expt = Experiment(exp_trials)
	all_data[exp] = Expt

    # ^*^*^ - creating .correct.csv file - ^*^*^
    TURK_CORRECT = open(FNAME + ".correct.csv", 'w')

    for trial in trial_obj:
	row = []
	for element in trial.get_header():
	    row.append(element)
	for quest, ans in trial.get_quest():
	    row.append(ans)
	write_row(row, TURK_CORRECT)
    TURK_CORRECT.close()
    #	    - ^*^*^ -

    return all_data

#^*^*^*^*^*^*^*^*^*^*^*^*^ creates a latin square lists from the ^*^*^
#			   whole dictionary			 ^*^*^
def LatSquareLists(Dict):
    lists = {}
    for expt in Dict.keys():
	exp_list = []
	D = Dict[expt]
	items = D.get_items()
	conds = D.get_conds()
	for i in range(D.get_condNumb()):
	    L = []
	    GenKeys = generate_keys(items, conds)
	    for j in GenKeys:
		try:
		    L.append(D.get_trials()[j])
		except KeyError:
		    print "Found the missing trial:"
		    print "	item", j[0] + ", condition", j[1:]
		    print "	in", expt, "experiment"
		    sys.exit()
	    exp_list.append(L)
	    conds = rotate(conds)
	lists[expt] = exp_list
    return lists

#^*^*^*^*^*^*^*^*^*^*^*^*^ creates LCM lists given latin square lists, ^*^*^
#			   LCM and the dictionary with all data	       ^*^*^
def LCMlists(Dict, LatSq, Lcm):
    #^*^*^ makes lcm empty lists:
    LISTS = []
    for i in range(Lcm):
	LISTS.append([])

    for expt in Dict.keys():
	number = Lcm/Dict[expt].get_condNumb()
	for i in range(number):
	    for j in range(len(LatSq[expt])):
		index = j + i*len(LatSq[expt])
		LIST = LatSq[expt][j]
		LIST_copy = LIST[:]
		LISTS[index].append(LIST_copy)
    return LISTS

#^*^*^*^*^*^*^*^*^*^*^*^*^ randomizes the given list using the ^*^*^
#			   algorithm			       ^*^*^
def Randomize(L):
    global F
    global Y
    NEW = []
    ExpNUM = len(L)
    OLD = L[:]
    MinRatio = F

    #	--- creating the first fillers ---
    if Y != 0:
	for i in range(len(OLD)):
	    if isThere(OLD[i][0].get_exp(), "filler"):
		FILL = i
	FILLERS = []
	for i in range(Y):
	    Random_Index = random.choice(range(len(OLD[FILL])))
	    FILLERS.append(OLD[FILL][Random_Index])
	    OLD[FILL].pop(Random_Index)
    #	----	  ----	    ----

    #^*^*^ - calculating initial proportions - ^*^*^
    PROPs = {}
    total = 0
    for exp in OLD:
	total += len(exp)
    #print "total:", total
    for exp in OLD:
	PROPs[exp[0].get_exp()] = len(exp)/float(total)
    #print PROPs
    count = 0
    while True:
	#print "count:", count, "-----------------------------"
	if OLD ==[]:
	    break
	exp_to_use = range(len(OLD)) # <-- indexes of all exp
	RATIOS = {}
	EXPS = exp_to_use[:]
	for exp in EXPS:	     # <-- removes the filler sub expt	from EXPS
	    if isThere(OLD[exp][0].get_exp(), "filler"):
		EXPS.remove(exp)
	if EXPS == []:
	    IsCloseSqueeze = False
	else:
	    for i in EXPS:
		expts = exp_to_use[:]
		expts.remove(i)
		len_all = 0
		for index in expts:
		    len_all += len(OLD[index])
		RATIOS[float(len_all)/len(OLD[i])] = i
	    SmallestRatio = min(RATIOS.keys())
	    IsCloseSqueeze =	MinRatio > SmallestRatio


	#^*^*^ actual placing one of the trials in the NEW list:
	if IsCloseSqueeze:
	    trial_to_place = random.choice(OLD[RATIOS[SmallestRatio]])
	    NEW.insert(0, trial_to_place)
	    OLD[RATIOS[SmallestRatio]].remove(trial_to_place)

	else:
	    Len_total = 0
	    for i in exp_to_use:
		Len_total += len(OLD[i])

	    #^*^*^ remove from the exp_to_use exp that were used last F times
	    LastUsed = [] # <-- names of last used exps
	    for trial in NEW[:F]:
		expName = trial.get_exp()
		if expName in LastUsed:
		    continue
		LastUsed.append(expName)
	    for index in EXPS:
		if OLD[index][0].get_exp() in LastUsed:
		    exp_to_use.remove(index)

	    #^*^*^ creates weighted random choice:
	    weights = []
	    #print "exp_to_use:", exp_to_use

	    fillerIndex = None
	    for i in exp_to_use:
		Experiment = OLD[i][0].get_exp()
		if isThere(Experiment, "filler"):
		    fillerIndex = i
		    continue
		if count< F:
		    k = count
		else:
		    k = F
		#print "k:", k
		weight = round( ((PROPs[Experiment]) / (1 - k * PROPs[Experiment])), 2)
		#print "PROPs[Experiment]:", PROPs[Experiment]
		#print "weight:", weight
		weights.append((i, weight))

	    totalW = 0
	    for i, w in weights:
		totalW += w
	    #print "totalW:", totalW
	    if fillerIndex != None:
		weights.append((fillerIndex, round(1-float(totalW), 2)))
	    #print "weights:", weights


	    randIndex = w_choice(weights) # weighted
	    trial_to_place = random.choice(OLD[randIndex])
	    NEW.insert(0, trial_to_place)
	    OLD[randIndex].remove(trial_to_place)

	#^*^*^ removes empty exp lists
	try:
	    OLD.remove([])
	except ValueError:
	    pass

	count += 1
    # ---- Adding first fillers ----
    if Y != 0:
	for f in FILLERS:
	    NEW.insert(0, f)

    return NEW

#^*^*^*^*^*^*^*^*^*^*^*^*^ randomizes each experiment list, from them ^*^*^
#			   creates final versions of the lists of the ^*^*^
#			   trials-objects			      ^*^*^
def Finalize(lists):
    for L in lists:  # <--- randomize each experiment
	expNUM = len(L)
	for i in range(expNUM):
	    random.shuffle(L[i])
    FINAL = []
    for L in lists:
	FINAL.append(Randomize(L))
    return FINAL




#			     <<<<<<<< MAIN FUNCTION >>>>>>>>>

def main():
    print
    print "Processing the text file..."
    print
    print "-------"
    Dict = getdata(FILENAME)
    print "Number of experiments:", len(Dict)
    for expt in Dict.keys():
	print
	print "Experiment:", expt
	print "	  -", Dict[expt].get_itemNumb(), "items"
	print "	  -", Dict[expt].get_condNumb(), "conditions"
	print "	  -", Dict[expt].get_trialNumb(), "trials"
	print "	  - number of questions:", Dict[expt].get_questNumb()
	print "	  - conditions:"
	print Dict[expt].get_conds()
    print "-------"
    print

    print "Performing a check of the parameters..."
    # ^*^*^*^*^ CHECK ^*^*^*^*^*^
    # ^*^ number of trials should be a multiple of number of conditions: ^*^
    for expt in Dict.keys():
	isTrialNumbError = Dict[expt].get_condNumb() \
	* Dict[expt].get_itemNumb() != Dict[expt].get_trialNumb()
	if isTrialNumbError:
	    print "Error in the text file:"
	    print "	trials are missing for some of the conditions"
	    print "	in", expt, "experiment"
	    print "	(might be something wrong with the headings of the trials)"

	# ^*^ number of items should be a multiple of number of conditions: ^*^
	if float(Dict[expt].get_itemNumb()) % Dict[expt].get_condNumb() != 0:
	    print "Error in the text file:"
	    print "	Number of items is not a multiple of number of conditions"
	    print "	in", expt, "experiment"
	    sys.exit()

    # ^*^ input number of lists should be a multiple of LCM of conditions: ^*^

    # finds out number of conditions for each experiment, puts them in a list
    COND_NUMB = []
    for expt in Dict.keys():
	COND_NUMB.append(Dict[expt].get_condNumb())
    Lcm = LCM(COND_NUMB)

    # Checking...
    IsNumbListsError = float(N)%Lcm != 0
    if IsNumbListsError:
	print "Input Error:"
	print "	 number of lists requested,", str(N) + ", is not a multiple of"
	print "	 LCM of conditions,", Lcm
	sys.exit()


    # ^*^ checking F (number of in-between trials): ^*^
    ALL = Dict.keys()[:]
    NoFillers = True
    for thing in ALL:
	if isThere(thing, "filler"):
	    ALL.remove(thing)
	    NoFillers = False

    if NoFillers:
	print "WARNING:"
	print "	    fillers are missing or there are problems"
	print "	    with their format in the text file."
	print "		    (e.g. the experiment title of fillers"
	print "		must include the word 'filler')"
    for expt in ALL:   # <--- all experiments except fillers
	ALLexpt = Dict.keys()[:]
	ALLexpt.remove(expt)
	ALL_length = 0	   #  --    All_length - total length of all other experiments	  --
	for E in ALLexpt:
	    ALL_length += Dict[E].get_itemNumb()
	# ^*^ < All_length always includes fillers and first Y fillers are not used in
	#	the algorithm with F, so we should consider (ALL_length - Y) > ^*^
	if ALL_length - Y < F*Dict[expt].get_itemNumb():
	    print "WARNING:"
	    print "	there might not be enough items to have", F
	    print "	trials from other experiments and fillers"
	    print "	between trials of", expt, "experiment."
	    print "	please choose a smaller value for the number of"
	    print "	in-between trials / decrese the number of"
	    print "	    fillers in the beginning of each list"
	    print "	or add more fillers."


    # ^*^ checking the number of questions (should be the same for all the experiments):
    quest_numbers = []
    for expt in Dict.keys():
	quest_numbers.append(Dict[expt].get_questNumb())
    for i in range(len(quest_numbers)):
	if quest_numbers[i] != quest_numbers[i-1]:
	    print "Error in the text file:"
	    print "	the number of questions in trials"
	    print "	in different experiments"
	    print "	is not the same"
	    sys.exit()

    #		       ---- finished checking ----

    print
    print "Creating a latin square..."


    #^*^*^ creates latin-square list of lists for all experiments
    #	   (each experiment is a list of n lists, n - number of conditions)
    #	   3 levels embedded lists

    LatSq = LatSquareLists(Dict)


    print
    print "Creating LCM (", Lcm, ") lists..."

    LCM_lists = LCMlists(Dict, LatSq, Lcm)

    print
    print "Creating", N, "lists..."

    N_lists = []
    Repeat = N/Lcm
    for i in range(Repeat):
	for List in LCM_lists:
	    exp_list = []
	    for expt in List:
		expt_copy = expt[:]
		exp_list.append(expt_copy)
	    N_lists.append(exp_list)

    print
    print"Randomizing each list..."
    FINAL = Finalize(N_lists)

    #********************* TO CHECK THE RANDOMIZING: *****************
    #for newlist in FINAL:
    #	expments = []
    #	[expments.append(trial.get_exp()) for trial in newlist]
    #	print "-------", expments



    print
    print "Creating two csv files..."



    # ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^* creating the two csv files: ^*^*^
    TURK_CSV = open(FNAME + '.turk.csv', 'w')

    # ^*^ creating header rows (as lists) for both csv files ^*^
    header = []
    header2 = []
    header.append("list")
    header2.append("list")
    for i in range(len(FINAL[0])):
	header.append("trial_" + str(i+1))
	header2.append("Experiment"+ str(i+1))
	header2.append("Condition"+ str(i+1))
	header2.append("Item"+ str(i+1))
	number_of_questions = len(FINAL[0][i].get_quest())
	for j in range(number_of_questions):
	    header.append("question_" + str(j+1) + "_" + str(i+1))


    # writing the header to TURK.csv
    write_row(header, TURK_CSV)

    # writing the main part of TURK.csv
    for i in range(len(FINAL)):
	newrow = []
	newrow.append(str(i+1))
	for trial in FINAL[i]:
	    newrow.append('"' + trial.get_body() + '"')
	    try:
		for quest, ans in trial.get_quest():
		    newrow.append('"'+quest+'?"')
	    except ValueError:
		print "Error in the text file:"
		print " there is something wrong with question"
		print " and/or answer in the trial of", trial.get_exp(), "experiment,"
		print " item:", trial.get_item(), ", condition:", trial.get_cond()
		sys.exit()
	write_row(newrow, TURK_CSV)






    # ^*^ 2) TURK_DECODE ^*^
    TURK_DECODE = open(FNAME +'.decode.csv', 'w')

    # writing the header to TURK_DECODE
    write_row(header2, TURK_DECODE)

    # writing the main part of TURK_DECODE
    for i in range(len(FINAL)):
	newrow = []
	newrow.append(str(i+1))
	for trial in FINAL[i]:
	    newrow.append(trial.get_exp())
	    newrow.append(trial.get_cond())
	    newrow.append(trial.get_item())
	write_row(newrow, TURK_DECODE)

    TURK_CSV.close()
    TURK_DECODE.close()

    print
    print "------- DONE! -------"
    print

main()














