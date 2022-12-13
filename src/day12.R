library(tidyverse)

aoc_12 <- read_lines(file("data/data_12.txt"))
rown <- length(aoc_12)
q_map <- c()

get_number <- function(char) {
    if (char == "S") {
        return(0)
    }
    if (char == "E") {
        return(27)
    }
    return(utf8ToInt(char) - utf8ToInt("a") + 1L)
}

for (line in aoc_12) {
    coln <- length(unlist(strsplit(line, split = "")))
    q_map <- c(q_map, sapply(unlist(strsplit(line, split = "")), get_number))
}
tr_mat <- matrix(q_map, nrow = rown, byrow = T)
check_mat <- matrix(10000, nrow = rown, ncol = coln)
find_x <- which(tr_mat == 0, arr.ind = T)[1]
find_y <- which(tr_mat == 0, arr.ind = T)[2]
check_mat[find_x, find_y] <- 0
surround_list <- list(c(find_x, find_y))

while (TRUE) {
    old_list <- surround_list
    surround_list <- list()
    for (item in old_list) {
        x <- item[1]
        y <- item[2]
        if ((x + 1) %in% 1:rown) {
            if ((tr_mat[x + 1, y] - tr_mat[x, y]) %in% 0:1){
            check_mat[x + 1, y] <- check_mat[x, y] + 1
            surround_list <- c(surround_list, list(c(x + 1, y)))
        }}
        if ((x - 1) %in% 1:rown){
            if ((tr_mat[x - 1, y] - tr_mat[x, y]) %in% 0:1) {
            check_mat[x - 1, y] <- check_mat[x, y] + 1
            surround_list <- c(surround_list, list(c(x - 1, y)))
        }}
        if ((y + 1) %in% 1:coln){
            if ((tr_mat[x, y + 1] - tr_mat[x, y]) %in% 0:1) {
            check_mat[x, y + 1] <- check_mat[x, y] + 1
            surround_list <- c(surround_list, list(c(x, y + 1)))
        }}
        if ((y - 1) %in% 1:coln) {
            if ((tr_mat[x, y - 1] - tr_mat[x, y]) %in% 0:1) {
            check_mat[x, y - 1] <- check_mat[x, y] + 1
            surround_list <- c(surround_list, list(c(x, y - 1)))
        }}
        print(check_mat)
    }
    if (length(surround_list) == 0) break()
}
