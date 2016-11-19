library(jsonlite)
setwd("~/Yelp")
business <- stream_in(file("business.json"))
extract <- function(data,attribute){
  if(!is.character(attribute) | is.null(data[[attribute]])) return("Error:check ur att input")
  else
    table <- cbind(data[["business_id"]], data[[attribute]])
  table <- as.data.frame(table)
  names(table)[1] <- "business_id"
  return(table)
}

bz_hours <- extract(data = business, attribute = c("hours"))
bz_attributes <- extract(data = business, attribute="attributes")

stream_out(extract(data = business, attribute = "categories"), file("categories"))
   
# isolate categories into a separate matrix
cat    <- unlist(business$categories)
unicat <- unique(cat)
catmat <- matrix(ncol = length(unicat), nrow = nrow(business))
for(i in 1: nrow(catmat)){
  catmat[i,which(is.element(unicat,business$categories[[i]]))] <- T
}
catmat[is.na(catmat)] <- F
catmat <- as.data.frame(catmat)
names(catmat) <- unicat
rm(i, unicat, cat)

catmat <- apply(catmat, 2, as.numeric)
catmat <- as.data.frame(catmat)
catmat <- cbind(business$business_id, catmat)
names(catmat)[1] <- "business_id"
