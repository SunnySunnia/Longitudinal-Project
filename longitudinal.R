##Longitudinal analysis

###packages
#install.packages("crimCV")
library(crimCV)
library(reshape2)
library(dplyr)


###Import
setwd("C:/Longitudinal-Project")
concussion <- read.csv("C:/Longitudinal-Project/concussion.csv", stringsAsFactors=FALSE)
concussion = concussion[,1:33]

###Cleaning
concussion[,4:33] = apply(concussion[,4:33],2, as.numeric)
concussion$Date = as.Date(concussion$Date)
concussion$Injury.date = as.Date(concussion$Injury.date)
concussion = mutate(concussion, days_aft_injury = as.numeric(Date - Injury.date))
concussion = mutate(concussion, week = ceiling(days_aft_injury/7))

#Exploratory
length(unique(concussion$ID))      #number of distinct subjects
nrow(unique(concussion[,c(1,3)]))   #number of subject-injury records

d1= dcast(concussion[,1:7], ID + `Injury.date` + Age + Gender + Race~Date)
#d_a1 = dcast(concussion[,c(1:3,10)], ID + `Injury.date` ~Date)
my_mean = function(x){
  res = mean(x, na.rm = T)
}
d_a1 = dcast(concussion[,c(1,3,35,10)], ID + `Injury.date` ~week, my_mean)
plot(x=0:56,y=d_a1[82,3:59])

concussion = as.matrix(concussion)

out1 = crimCV(apply(concussion[1:3000,10:33],2,as.numeric),2)
plot(out1)

out_a1 = crimCV(apply(as.matrix(d_a1)[1:300,3:30],2,as.numeric),2)
plot(out_a1)



##Example
data("TO1adj")
outex = crimCV(TO1adj,2,dpolyp = 3, rcv = T)
plot(outex)
summary(outex)
