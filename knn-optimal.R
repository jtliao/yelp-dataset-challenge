library(parallel)
# optimizing knn

#Create a distance matrix
fit <- fields::rdist(train[,c(3,4)])
star <- pitt$stars

#Computed a row-sorted matrix out of the fit
ind <- apply(fit, 1, FUN = function(x){
  row <- sort(x, index.return =T)$ix
})
colnames(ind) <- seq(1:nrow(train))
rownames(ind) <- colnames(ind)
rm(fit)
ind <- ind[-1,]

#For given k-neighbor parameter, choose the first k+1 columns
#and take their stars and takes a mean
knear <- function(k){
  x <- as.data.frame(t(ind[c(1:99),]))
  x <- apply(x, 2, FUN = function(x){
    star[x]
  })
  if(is.numeric(dim(x))){ 
    x <- apply(x,1, FUN = mean) 
    return(x)
  }
  else {
    return(x)
  }
}

#Do it over 1 to 1000
val_acc <- c(20:50)
n_core <- detectCores()-1
cl <- makeCluster(n_core)
clusterExport(cl, "ind")
clusterExport(cl, "star")
clusterEvalQ(cl, "knear()")
val_acc <- parSapply(cl, val_acc, FUN = knear)
stopCluster(cl)
rm(n_core)

for(i in 1:nrow(train)){
  val_acc[i,] <- 1-abs((val_acc[i,] - star[i])/star[i])
}

plot(c(20:50), colMeans(val_acc),'b')


