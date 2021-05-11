library(epitopes)
library(microbenchmark)
library(data.table)
ncores <- 4

files <- dir("./", pattern = ".csv")

res <- vector("list", length(files))
names(res) <- files

for (i in seq_along(files)){
  x <- as.data.table(read.csv(files[i], header = TRUE))
  class(x) <- c(class(x), "windowed_epit_dt")
  x$Info_sourceOrg_id <- NA
  x$Info_protein_id   <- NA
  x$Info_epitope_id   <- NA
  x$Info_center_pos   <- NA
  res[[i]] <- microbenchmark(Test = calc_features(x, max.N = 2, ncpus = 4), 
                             times = 3, unit = "s")
}

# Join results
results <- do.call(rbind, lapply(res, function(z) as.data.frame(print(z))))

print(results)
