rm(list = ls())
library(dplyr)

subcollection <- "robust"

dir_list_all <- list.dirs(path = paste0("../../data_near_duplicate/",subcollection,"/lsh_results",
                                        collapse = ""))
dir_list = dir_list_all[2:length(dir_list_all)]

out_folder <- paste0("../../data_near_duplicate/",subcollection, "/",
                     collapse = "")

index_rel_name = "index.csv"
sign_sim_rel_name = "signature_sim.csv"

# Constants ---------------------------------------------

SHARED_BUCK_METRIC_NAME <- "metrics_shared_buckets_number.csv"
SIGN_METRIC_NAME <- "metrics_signature_similarity.csv"

SIGN_SIM_NAME = "signature_similarity"
SHARED_BUCK_NAME = "shared_buckets_number"

# Plotting ----------------------------

plot_dir <- paste0("../../data_near_duplicate/",subcollection,"/plots",
                   collapse = "")

HEIGHT <- 800
WIDTH <- 1000

PCH_PRECISION = 16
PCH_RECALL = 8
PLOT_TYPE = "b"

PRECISION_NAME = "precision"
RECALL_NAME = "recall"

TRUE_DUPLICATES_COL = rgb(0, 0, 1, 0.3)
FALSE_DUPLICATES_COL = rgb(1, 0, 0, 0.3)

# Parameters sets --------------------------------------

NOISE_QUANT_NAME <- "noise quantity"
DUPLICATES_PERCENT_NAME <- "duplicates percent"
SIGL_NAME <- "signature length"
NBA_NAME <- "bands number"
NBU_NAME <- "buckets times number"


NOISE_QUANT_PREFIX <- "noise_"
NOISE_QUANT <- c("no", "small", "mid") # small noise 2%, mid 5%

DUPLICATE_PREFIX <- "per_"
DUPLICATES_PERCENT = c(1, 5, 10, 25)

SIGL_PREFIX <- "sigl_"
SIGL <- c(100, 200)

NBA_PREFIX <- "nba_"
NBA <- c(10, 20)

NBU_PREFIX <- "nbu_"
NBU <- c(2, 5, 10)

PREFIX_LIST <- setNames(
  list(NOISE_QUANT_PREFIX,
       DUPLICATE_PREFIX,
       SIGL_PREFIX,
       NBA_PREFIX,
       NBU_PREFIX),
  c(NOISE_QUANT_NAME,
    DUPLICATES_PERCENT_NAME,
    SIGL_NAME,
    NBA_NAME,
    NBU_NAME)
)

EMPTY_PARAMS_LIST <- setNames(
  list(NA, NA, NA, NA, NA),
  c(NOISE_QUANT_NAME,
    DUPLICATES_PERCENT_NAME,
    SIGL_NAME,
    NBA_NAME,
    NBU_NAME)
)

# Function ----------------------------------------------

# first join the metric dataset with the index of true duplicates
JoinMetricsIndex <- function(metrics_df, index_df){
  index_df = cbind(index_df, rep(1, nrow(index_df)))
  colnames(index_df) = c(colnames(index_df)[1:2], "is_duplicate")
  temp_df <- left_join(metrics_df, index_df,
                       by = c("doc1" = "doc1_id", "doc2" = "doc2_id"))
  temp_df[,"is_duplicate"] <- ifelse(is.na(temp_df[,"is_duplicate"]), 0, 1)
  return(temp_df)
}

# Select folder ---------------------------------

# mid ------------------------------
# required folder tags
required <- c(paste0(NOISE_QUANT_PREFIX, NOISE_QUANT[2]),
                    paste0(DUPLICATE_PREFIX, DUPLICATES_PERCENT[2]),
                    paste0(SIGL_PREFIX, SIGL[1]),
              paste0(NBA_PREFIX, NBA[1]),
              paste0(NBU_PREFIX, NBU[3]))

result <- dir_list[sapply(dir_list, function(x) all(sapply(required, grepl, x)))]

temp_joint_df <- JoinMetricsIndex(read.csv(paste0(result, "/", sign_sim_rel_name)),
                                  read.csv(paste0(result, "/" ,index_rel_name)))


temp_name <- paste0(required, collapse = "_")
temp_name <- paste0("buck_sig_sim", "_", temp_name)
png(filename = paste0(out_folder,temp_name, ".png", collapse = ""),
    height = HEIGHT,
    width = WIDTH)

boxplot(signature_similarity ~ shared_buckets_number,
        data = temp_joint_df[which(temp_joint_df$is_duplicate == 1),],
        xlab = SHARED_BUCK_NAME,
        ylab = SIGN_SIM_NAME,
        col = TRUE_DUPLICATES_COL,
        main = "Signatures Similarity by Shared Bucket")

boxplot(signature_similarity ~ shared_buckets_number,
        data = temp_joint_df[which(temp_joint_df$is_duplicate == 0),],
        col = FALSE_DUPLICATES_COL,
        add = TRUE)


legend("bottomright",
       legend = required,
       bty = "n",
       cex = 0.7)

legend("topleft",
       legend = c("true duplicates", "false duplicates"),
       bty = "n",
       cex = 0.7,
       col = c(TRUE_DUPLICATES_COL, FALSE_DUPLICATES_COL),
       pch = 16)

dev.off()



















