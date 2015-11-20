###############################################################
## Library for tedlab: linguistic acceptability rating surveys on Mechanical Turk
## October 2009 Steve Piantadosi
## July, August, September 2010 Ted Gibson
###############################################################

library(languageR)

mean.na.rm <- function(x) { mean(x,na.rm=T) }

# This reads in a turk file, and transforms it. It takes columns whose header names end in numbers, and lines 
# up the columns by their number and all other column info to create a new row. So for each
# column ending in a number, it makes a row of those columns. 

# This function applies to a data.file as input

read.turk.rating.file <- function(filename) {

	data.file <- read.csv(filename, header=T) # csv file with header

	## Reconfigure all of the data:	
	# a list of extracted item numbers--the last number in each header (assuming there are less than 3 or 4)
	item.numbers <- as.numeric(gsub("[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]+", "", names(data.file), perl=T))

	data <- data.frame(NULL)

	# loop over each item number
	for(i in min(item.numbers, na.rm=T):max(item.numbers, na.rm=T)) {
		# extract all 
		row <- data.file[,(item.numbers==i)  # keep columns with the right number
			     | is.na(item.numbers)  #or no number
				] # a block of rows, one for each participant in the experiment
				
		row$PresentationOrder <- i
		row$Participant <- data.file$WorkerId
		names(row) <- gsub("[0-9]+$", "", names(row), perl=T) # remove item numbers from row
		# sort these row elements by their column name, minus the numbers, so we add to data correctly
		row <- row[,order(names(row))] 
		data <- rbind(data, row)
		names(data) <- names(row)[order(names(row))] # save this. Slightly inefficient. 
	}

	data$ListNumber <- data$Input.list
	data
}

	
read.itm.file <- function(f) {

	tmp <- read.csv(f, header=T) # csv file with header
	
	## Reconfigure all of the data:	
	# a list of extracted item numbers--the last number in each header (assuming there are less than 3 or 4)
	item.numbers <- as.numeric(gsub("[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]*[0-9]*[^0-9]+", "", names(tmp), perl=T))

	data <- data.frame(NULL)

	# loop over each item number
	for(i in min(item.numbers, na.rm=T):max(item.numbers, na.rm=T)) {
		# extract all 
		row <- tmp[,(item.numbers==i)  # keep columns with the right number
			     | is.na(item.numbers)  #or no number
				] # a block of rows, one for each participant in the experiment
				
		row$PresentationOrder <- i
		names(row) <- gsub("[0-9]+$", "", names(row), perl=T) # remove item numbers from row
		# sort these row elements by their column name, minus the numbers, so we add to data correctly
		row <- row[,order(names(row))] 
		data <- rbind(data, row)
		names(data) <- names(row)[order(names(row))] # save this. Slightly inefficient. 
	}
	data$ListNumber <- data$list
	data
	}


## The three lines below need to be edited so that they include the appropriate file names instead of "xxxxx"
## The turk output file is called "Batch_xxxxxx_result.csv"
## with each line representing a different participant / list (each one with a different random order)
## The file "xxx.decode.csv" is the file with the condition codes for items in each list
## The file "xxx.correct.csv" is the file with the correct answers for the comprehension questions

# turk.output.file <- "Batch_xxxxxx_result.csv"
# decode.file <- "xxx.decode.csv" 
# correct.file <- "xxx.correct.csv"
turk.output.file <- "Batch_301654_result.csv"
decode.file <- "PrPatReference_Linger.decode.csv" 
correct.file <- "PrPatReference_Linger.correct.csv"

## WARNING: Approve/Reject should be removed from the header for the turk.output.file, or else R won't read it

mydata <- read.turk.rating.file(turk.output.file) 

dropped.columns <- c("HITId", "HITTypeId","Title", "Description", "Keywords", "Reward", "CreationTime", "MaxAssignments", 	"RequesterAnnotation", "AssignmentDurationInSeconds", "AutoApprovalDelayInSeconds", "Expiration", "NumberOfSimilarHITs", 	"LifetimeInSeconds", "AssignmentId", "AcceptTime", "SubmitTime", "AutoApprovalTime", "ApprovalTime", "RejectionTime", 	"RequesterFeedback", "WorkerId", "Input.list")

mydata <- mydata[, setdiff(names(mydata), dropped.columns)]

###############################################################
## Read in the item files

itm.data <- read.itm.file(decode.file)

###############################################################
## Read in the correct 

correct.answers <- read.csv(correct.file, header=FALSE)
names(correct.answers) <- c("Experiment", "Item", "Condition", "CorrectAnswer")

#################################################################
## Merge itm.data, data, and correct answers

# merge these together
mydata <- merge(mydata, itm.data, by=c("PresentationOrder", "ListNumber"))
mydata <- merge(mydata, correct.answers, by=c("Item", "Condition", "Experiment"))

#################################################################
## Fix missing data

mydata$Answer.YNQ[mydata$Answer.YNQ==""] <- NA

#################################################################
## Now add correct answers and condition information

# count NA as incorrect
mydata$Correct <- (as.character(mydata$CorrectAnswer) == as.character(mydata$Answer.YNQ))

#################################################################
## Filter participants 

# get percent accuracies for each participant
participant.summary.info <- aggregate(mydata$Correct, by=list(mydata$Participant), mean.na.rm)
names(participant.summary.info) <- c("Participant", "Accuracy")

mydata <- merge(mydata, participant.summary.info, by=c("Participant"))

# get percent of NAs for each participant
participant.nas <- aggregate(is.na(mydata$Answer.YNQ), by=list(mydata$Participant), mean)
names(participant.nas) <- c("Participant", "NAPercent")
participant.summary.info <- merge(participant.summary.info, participant.nas, by=c("Participant"))
mydata <- merge(mydata, participant.nas, by=c("Participant"))

# total response count
participant.responsecount <- aggregate(mydata$Answer.YNQ, by=list(mydata$Participant), length)
names(participant.responsecount) <- c("Participant", "ResponseCount")
participant.summary.info <- merge(participant.summary.info, participant.responsecount, by=c("Participant"))
mydata <- merge(mydata, participant.responsecount, by=c("Participant"))

participant.summary.info <- merge(participant.summary.info, unique(mydata[,c("Participant", "Answer.country", "Answer.English")]), by=c("Participant"))

mydata <- mydata[mydata$Answer.country == "USA" &
		mydata$Answer.English == "yes" &
		mydata$Accuracy > 0.75 &
		mydata$NAPercent < 0.10 & 
		mydata$ResponseCount <= max(mydata$PresentationOrder) # you didn't do more than the number of items in one list
		,]

