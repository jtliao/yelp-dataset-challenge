setwd("~/yelp/yelp-dataset-challenge/ml-group")

install.packages("sqldf")
library(sqldf)

install.packages("jsonlite")
library(jsonlite)

business <- stream_in(file("yelp_academic_dataset_business.json", "r"))
review <- stream_in(file("yelp_academic_dataset_review.json", "r"))

business <- business[,-c(3,5,14,9)]
review <- review[,-1]

# 5 subset tables
x1 <- sqldf("SELECT business_id, user_id FROM review")
review_text <- sqldf("SELECT business_id, stars, text FROM review")

# create fcn to extract certain subsets
extract <- function(extract_col_indices, data){
  return(data[,extract_col_indices])
}


install.packages("plyr")
library(plyr)

review_text["length"] <- sapply(review_text["text"], FUN = nchar)

d <- density(review_text[,"length"])
plot(d)

review_text["log length"] <- sapply(review_text["length"], FUN = log)
dlog <- density(review_text[,"log length"])
plot(dlog)


most_reviewed_business <- sqldf("SELECT b.business_id, r.stars, r.text, r.length from business b, review_text r where r.business_id==b.business_id and b.review_count==(SELECT MAX(review_count) from business)")
plot(density(most_reviewed_business[,"stars"]))


