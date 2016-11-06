library(lubridate)
library(animation)
library(ggplot2)
library(ggmap)
library(parallel)


extractyr <- function(year, month){
  if(!is.element(month, c(1:12))) return("ERROR00")
  if(!is.element(year,c(2004:2016))) return("ERROR")
  else{
    output <- filter(pitt_review[,-c(2,7)], year(date) == year & month(date)==month)
    return(output)
  }
}
pitt_review <- review[is.element(review$business_id, pitt$business_id),]
pitt_review <- merge(pitt_review, pitt[,c(1,10,13)], by ='business_id', all.x = T)
pitt_map <- qmap("Pittsburgh", zoom = 14, maptype="roadmap")
annual <- extractyr(2016,4)

test <- function(date){
  x <-pitt_map+geom_point(data=annual[which(annual$date==date),], aes(x=longitude, y=latitude, size = stars), alpha = 0.5)+
      ggtitle(paste(date,":",nrow(annual[which(annual$date==date),]), sep=" "))
  x
}
unidate <- sort(unique(annual$date))
ani <- function(){
  lapply(unidate, FUN = function(x){
    print(test(x))
    ani.pause(ani.options(interval = 1))
  })  
}
saveHTML(ani(), autoplay=F,  loop = FALSE, verbose = FALSE, outdir = "images/animate/new",
single.opts = "'controls': ['first', 'previous', 'play', 'next', 'last', 'loop', 'speed'], 'delayMin': 0")

