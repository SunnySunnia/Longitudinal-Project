##Longitudinal analysis

###packages
#install.packages("crimCV")
library(crimCV)
library(reshape2)
library(dplyr)
#install.packages("mi)
library(mi)

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

##Missing data method 1
d_a1 = dcast(concussion[,c(1,3,35,10)], ID + `Injury.date` ~week, my_mean)
d_a1[,3:59]=apply(d_a1[,3:59],2,as.numeric)

d_a1$`0`=ifelse(is.na(d_a1$`0`),d_a1$`1`,d_a1$`0`)
for(j in 4:59){
  for(i in 1:nrow(d_a1)){
    d_a1[i,j]=ifelse(is.na(d_a1[i,j]),mean(c(d_a1[i,j-1],d_a1[i,j+1]),na.rm=T),d_a1[i,j])
  }
}

##Missing data method 2:  
d2_a1 = dcast(concussion[,c(1,3,35,10)], ID + `Injury.date` ~week, my_mean)
d2_a1[,3:59]=apply(d2_a1[,3:59],2,as.numeric)
x = 0:56
df4fit = rbind(d2_a1[8,3:59],x)
df4fit = data.frame(t(df4fit))
colnames(df4fit)=c("y","x")
plot(y~x, data = df4fit, type="l")
fit1 = lm(y~x, data = df4fit[1:5,])
for(i in 1:nrow(d2_a1)){
  na_index = which(is.na(d2_a1[i,]))
  fit_index = i:i+4
  fit = lm()
}


test = missing_data.frame(d2_a1[,3:59])
test = missing_data.frame(test)

plot(x=0:56,y=d_a1[1,3:59],type="l",ylim=c(-1,7))
colors=rainbow(199)
for(i in 2:200){
  points(x=0:56, y=d_a1[i,3:59],type="l", col=colors[i])
}


concussion = as.matrix(concussion)

out1 = crimCV(apply(concussion[1:3000,10:33],2,as.numeric),2)
plot(out1)

out_a1 = crimCV(apply(as.matrix(d_a1)[1:300,3:59],2,as.numeric),2)
plot(out_a1)

out_a1 = crimCV(apply(as.matrix(d_a1)[1:300,3:59],2,as.numeric),2)
plot(out_a1)

##Example
data("TO1adj")
outex = crimCV(TO1adj,2,dpolyp = 3, rcv = T)
plot(outex)
summary(outex)
