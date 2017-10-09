library(lmtest)
base_path <- "C:\\Users\\sasce\\Desktop\\dataset\\points"
file_name <- "Y_POINTS_3_3_A.csv"
file_path <- file.path(base_path, file_name)



window_size <- 4

raw_points = read.csv(file_path, sep = " ", dec = ".", stringsAsFactors = FALSE, header = FALSE)
num_samples <- NROW(raw_points)
num_persons <- NCOL(raw_points)
y_points_demean <- raw_points - colMeans(raw_points)

r <- grangertest(y_points_demean[16], y_points_demean[17], order = window_size)
r1 <- grangertest(y_points_demean[16], y_points_demean[17], order = window_size)[2, 4]

results <- data.frame(matrix(num_persons, num_persons))


for (i in range(1, num_persons)) {
    for (j in range(1, num_persons)) {
        if (i == j) {
            next
        }
        r <- grangertest(y_points_demean[i], y_points_demean[j], order = window_size)
        results[i, j] = 0
    }
}