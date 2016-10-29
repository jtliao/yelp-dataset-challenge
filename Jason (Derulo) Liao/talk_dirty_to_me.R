setwd("~/Yelp")
library(ggmap)
library(leaflet)
library(ggplot2)
library(MASS)
library(reshape2)
library(plyr)
library(dplyr)
library(parallel)
library(sqldf)
library(jsonlite)

business <- stream_in(file("business.json","r"))
review <- stream_in(file("review.json", "r"))
# dataset <- stream_in(file("dataset.json","r"))
# tip     <- stream_in(file("tip.json","r"))

# take only pittsburgh data
pitt <- business[which(business$city=="Pittsburgh"),]

### Relational database
#extracting function if the attribute is a table
extract <- function(data,attribute){
  if(!is.character(attribute) | is.null(data[["business_id"]])) return("Error:check ur att input")
  else
    table <- cbind(data[["business_id"]], data[[attribute]])
  table <- as.data.frame(table)
  names(table)[1] <- "business_id"
  return(table)
}

#Extract hours,attributes, and for review, text and vote
bz_hours <- extract(data = business, attribute = "hours")
bz_attributes <- extract(data = business, attribute = "attributes")

review_text <- review$text
review_text <- cbind(review$business_id, review_text)
review <- review[,-6]

vote <- extract(review,"votes")
vote <- cbind(vote, review$date)
names(vote)[5] <- "date"

#Extract categories and makes into a dataset
cat    <- unlist(pitt$categories)
catmat <- matrix(ncol = length(unique(cat)), nrow = nrow(pitt))
catmat <- as.data.frame(catmat)
names(catmat) <- unique(cat)
unicat <- unique(cat)
for(i in 1: nrow(catmat)){
  catmat[i,which(is.element(unicat,pitt$categories[[i]]))] <- T
}
catmat[is.na(catmat)] <- F

rm(i)
catmat <- apply(catmat[1:521], 2, as.numeric)
catmat <- as.data.frame(catmat)
catmat <- cbind(pitt$business_id, catmat)
names(catmat)[1] <- "business_id"


# function to join things with the originial
# Given numeric vector of indices, join it with the category matrix
yelpcat <- function(colindices){
  if(is.element(c(1), colindices)) return("CHECK YOUR INDICES")
  else merge(pitt[,c(1,colindices)], catmat)
}

# create a star - categories join
cierra <- yelpcat(which(names(pitt)=="stars"))

# linear regression model of categories
fit <- lm(stars ~ ., data = cierra[2:523])
pvalue  <- summary(fit)$coefficient[,c(1,4)]
x <- rownames(pvalue)
colinear<- names(fit$coefficients[is.na(fit$coefficients)])
for(i in 1:2){
  colinear <- as.data.frame(colinear)
  x <- as.data.frame(x)
  x <- apply(x,1, FUN = function(x){sub("`","", x)})
  colinear <- apply(colinear,1, FUN = function(x){sub("`","", x)})
}
rownames(pvalue) <- x
rm(x)
pvalue <- merge(as.data.frame(colSums(catmat[2:522])), pvalue, by = "row.names")
pvalue  <- pvalue[which(pvalue[,4] <= 0.05),]
names(pvalue)[2] <- "frequency"
x <- as.matrix(colSums(catmat[2:522]))
colinear <- t(x[is.element(rownames(x),colinear),])
rm(x)

# pvalue is the matrix of stars, coefficients and p-values for attributes that are statistically significant
# colinear is the vector of categories that have no significance whatsoever in the linear regression.

#Finding out average stars for different attributes
staravg <- sapply(colnames(cierra[2:522]), FUN = function(x) {
  mean(cierra$stars[which(cierra[[x]]==1)])
} )
staravg <- cbind(staravg, colSums(cierra[2:522]))
staravg <- as.data.frame(staravg)
staravg[,3] <- rownames(staravg)
names(staravg)[3] <- "Row.names"

pvalue <- merge(pvalue, staravg[,c(1,3)], by = "Row.names")
fit2 <- lm(stars~.,data = select(cierra, one_of(c("stars",pvalue$Row.names))))

#Votes analysis
mean_vote <- sqldf("SELECT business_id, AVG(funny), STDEV(funny), AVG(useful), STDEV(useful), AVG(cool), STDEV(cool) FROM vote GROUP BY business_id")
vote_date <- plyr::count(vote, vars = "date")
vote_id   <- plyr::count(vote, vars = "business_id")
mean_vote <- merge(mean_vote, vote_id, by = "business_id")




str(p <- plot_ly(vote_date, x = vote_date$date, y = vote_date$freq))
p %>%
  add_trace(y = fitted(loess(vote_date$freq  ~ as.numeric(vote_date$date)))) %>%
  layout(title = "Median frequency",
         showlegend = FALSE) 
# %>%
# dplyr::filter(uempmed == max(uempmed)) %>%
# layout(annotations = list(x = date, y = uempmed, text = "Peak", showarrow = T))


# Map Visualizations
diffstar <- function(x){
  pitt_map <- qmap(location ="Pittsburgh", zoom = 12)
  f<- pitt_map + geom_point(data = output[which(output$stars==x),], aes(x = longitude,y = latitude), stat = 'density2d' ,alpha = 1 )
  f
}
intstars <- function(x){
  leaflet(output[which(output$stars == x),]) %>%
    setView(lng=-79.995888, lat=40.440624, zoom =12) %>%
    addTiles() %>%
    addCircles(lng = ~longitude, lat = ~latitude, color = ~stars, radius=~stars, popup= ~stars)
}







