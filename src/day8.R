library(tidyverse)

aoc_8 <- read_lines(file("data/data_8.txt"))
rown <- length(aoc_8)
trees <- c()
for (line in aoc_8){
    coln <- length(unlist(strsplit(line, split = "")))
    trees <- c(trees, c(as.numeric(unlist(strsplit(line, split = "")))))
    }
tr_mat <- matrix(trees, nrow = rown, byrow =  T)
logic_mat <- matrix(nrow = rown, ncol = coln)

# Question 1
for (i in 1:rown){
    for (j in 1:coln){
        number <- tr_mat[i, j]
        if ( i %in% c(1,rown) | j %in% c(1,coln)){
            logic_mat[i,j] <- T
            } else {
                # find upper
                upper <- all(number - tr_mat[1:(i - 1), j] > 0)
                # find down
                down <- all(number - tr_mat[(i + 1):rown, j] > 0)
                # find right
                right <- all(number - tr_mat[i, (j + 1):coln] > 0)
                # find left
                left <- all(number - tr_mat[i, 1: (j - 1)] > 0)
                logic_mat[i,j] <- any(c(upper, down, right, left))
            }
    }
}

view_mat <- matrix(nrow = rown, ncol = coln)
# Question 2
for (i in 1:rown){
    for (j in 1:coln){
        number <- tr_mat[i, j]
        if ( i %in% c(1,rown) | j %in% c(1,coln)){
            view_mat[i,j] <- 0
            } else {
                # find upper
                upper <- 0
                while (i - upper > 1) {
                    upper <- upper + 1
                    if (number <= tr_mat[(i - upper), j]) break()
                }
                # find down
                down <- 0
                while (i + down < rown) {
                    down <- down + 1
                    if (number <= tr_mat[(i + down), j]) break()
                }
                # find left
                left <- 0
                while (j - left > 1) {
                    left <- left + 1
                    if (number <= tr_mat[i, (j - left)]) break()
                }
                # find right
                right <- 0
                while (j + right < coln) {
                    right <- right + 1
                    if (number <= tr_mat[i, (j + right)]) break()
                }
                view_mat[i,j] <- upper * down * right * left
            }
    }
}
