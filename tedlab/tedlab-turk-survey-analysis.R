#################################################################
### Make new columns, recoding Condition

### this example set of factors assumes two factors: Factor1 and Factor2
### The values for Factor1 are Factor1_Value1 and Factor1_Value2
### The values for Factor2 are Factor2_Value1, Factor2_Value2, and Factor2_Value3

mydata$Factor1 <- NA
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value1",]$Factor1 <- "Factor1_Value1"
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value2",]$Factor1 <- "Factor1_Value1"
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value3",]$Factor1 <- "Factor1_Value1"

mydata[mydata$Condition == "Factor1_Value2_Factor2_Value1",]$Factor1 <- "Factor1_Value2"
mydata[mydata$Condition == "Factor1_Value2_Factor2_Value2",]$Factor1 <- "Factor1_Value2"
mydata[mydata$Condition == "Factor1_Value2_Factor2_Value3",]$Factor1 <- "Factor1_Value2"

# set the order of factors for the regression (first is the baseline)
mydata$Factor1 <- factor(as.character(mydata$Factor1), levels=c("Factor1_Value1", "Factor1_Value1"))

mydata$Factor2 <- NA
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value1",]$Factor2 <- "Factor2_Value1"
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value2",]$Factor2 <- "Factor2_Value2"
mydata[mydata$Condition == "Factor1_Value1_Factor2_Value3",]$Factor2 <- "Factor2_Value3"

mydata[mydata$Condition == "Factor1_Value2_Factor2_Value1",]$Factor2 <- "Factor2_Value1"
mydata[mydata$Condition == "Factor1_Value2_Factor2_Value2",]$Factor2 <- "Factor2_Value2"
mydata[mydata$Condition == "Factor1_Value2_Factor2_Value3",]$Factor2 <- "Factor2_Value3"

# set the order of factors for the regression (first is the baseline)
mydata$Factor1 <- factor(as.character(mydata$Factor1), levels=c("Factor2_Value1", "Factor2_Value1", "Factor2_Value3"))

#################################################################
## Analysis using the conditions created above

# histogram of all ratings
hist(mydata$Answer.Rating, breaks=20)

# print a table of means
with(mydata, tapply(Answer.Rating, list(Factor1, Factor2), mean, na.rm=TRUE))

# DO an lmer model:
l <- lmer( Answer.Rating ~ Factor1 * Factor2 + (1 | Participant) + (1 | Item), data=mydata)

# qqnorm(residuals(l)): see if the data are normal.  If they are, the qqplot will be a straight line
# pvals.fnc(l) # as long as the graphs that are returned aren't jagged, then the pvals are meaningful; otherwise add an argument "nsim=50000" (default = 10000)

# ignoring the interactions
# l <- lmer( Answer.Rating ~ Factor1 + Factor2 + (1 | Participant) + (1 | Item), data=mydata)

