df <- read.csv("mturk-sample-uncolumnized.csv", F)
matrix(df[,1], ncol=3, byrow=TRUE) -> dfout
write.csv(dfout, "mturk-sample-input-columnized.csv", row.names=F)
