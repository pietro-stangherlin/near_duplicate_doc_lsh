rm(list = ls())

dir_list <- list.dirs(path = "../../data_near_duplicate/robust/lsh_results")
dir_list

# CONSTANTS -----------------
SHARED_BUCK_METRIC_NAME <- "metrics_shared_buckets_number.csv"
SIGN_METRIC_NAME <- "metrics_signature_similarity.csv"

PCH_PRECISION = 16
PCH_RECALL = 8



# parameters sets ------------
nbu <- c("5000000", "10000000", "20000000")
sigl <- c(100, 200, 300)
nba <- c(10, 20)


# Plotting function ------------
PlotTwoBandsVSPrecisionREcall <- function(my_xlab,
                                          my_xlim,
                                          my_dir_list,
                                          my_metrics_name,
                                          x_axis_var_name,
                                          precision_var_name,
                                          recall_var_name){
  
  
  for (nbuck in nbu){
    for(siglen in sigl){
      temp_pattern <- paste0(c(nbuck,"_sgn_shl_9_sigl_", siglen), collapse = "")
      
      temp_dirs <- my_dir_list[grep(temp_pattern,my_dir_list)]
      
      temp_nba_10 <- temp_dirs[grep("nba_10",temp_dirs)]
      
      metrics_df_10 <- read.csv(paste0(c(temp_nba_10, my_metrics_name),
                                       collapse = "/"))
      
      temp_nba_20 <- temp_dirs[grep("nba_20",temp_dirs)]
      
      metrics_df_20 <- read.csv(paste0(c(temp_nba_20, my_metrics_name),
                                       collapse = "/"))
      
      plot(metrics_df_10[,x_axis_var_name],
           metrics_df_10[,precision_var_name],
           col = COL_nba_10,
           xlim = my_xlim,
           ylim = c(0.4, 1),
           xlab = my_xlab,
           ylab = "metric",
           pch = PCH_PRECISION,
           main = paste0(c("N bucket: ", nbuck,
                           "; Signature len : ", siglen), collapse = ""))
      
      points(metrics_df_10[,x_axis_var_name],
             metrics_df_10[,recall_var_name],
             pch = PCH_RECALL, 
             col = COL_nba_10)
      
      points(metrics_df_20[,x_axis_var_name],
             metrics_df_20[,precision_var_name],
             col = COL_nba_20,
             pch = PCH_PRECISION)
      
      points(metrics_df_20[,x_axis_var_name],
             metrics_df_20[,recall_var_name],
             pch = PCH_RECALL,
             col = COL_nba_20)
      
      legend("bottomleft",
             legend = c("precision", "recall"),
             pch = c(PCH_PRECISION, PCH_RECALL),
             bty = "n")
      
      legend("bottomright",
             legend = c("10 bands", "20 bands"),
             col = c(COL_nba_10, COL_nba_20),
             bty = "n",
             lty = 1,
             lwd = 2)
      
      
    }
  }
}


# no noise ----------------------------
dir_list_no_noise <- dir_list[grep("no_noise", dir_list)]

# 10k ----------------------------------
dir_list_10k <- dir_list[grep("_10k", dir_list)]

# no noise 10k -------------------------------
dir_list_no_noise_10k <- intersect(dir_list_no_noise,
                                   dir_list_10k)

par(mfrow = c(3,3))

COL_nba_10 = "black"
COL_nba_20 = "red"



PlotTwoBandsVSPrecisionREcall(my_xlab = "signature similarity",
                              my_xlim = c(0.4, 1),
                              my_dir_list = dir_list_no_noise_10k,
                              my_metrics_name = SIGN_METRIC_NAME,
                              x_axis_var_name = "signature_similarity",
                              precision_var_name = "precision",
                              recall_var_name = "recall")

PlotTwoBandsVSPrecisionREcall(my_xlab = "shared bucket number",
                              my_xlim = c(5, 20),
                              my_dir_list = dir_list_no_noise_10k,
                              my_metrics_name = SHARED_BUCK_METRIC_NAME,
                              x_axis_var_name = "shared_buckets_number",
                              precision_var_name = "precision",
                              recall_var_name = "recall")

# small noise ----------------------------
dir_list_small_noise <- dir_list[grep("small_noise", dir_list)]

# no noise 10k -------------------------------
dir_list_small_noise_10k <- intersect(dir_list_small_noise,
                                   dir_list_10k)

par(mfrow = c(3,3))


PlotTwoBandsVSPrecisionREcall(my_xlab = "signature similarity",
                              my_xlim = c(0.4, 1),
                              my_dir_list = dir_list_small_noise_10k,
                              my_metrics_name = SIGN_METRIC_NAME,
                              x_axis_var_name = "signature_similarity",
                              precision_var_name = "precision",
                              recall_var_name = "recall")

PlotTwoBandsVSPrecisionREcall(my_xlab = "shared bucket number",
                              my_xlim = c(0, 20),
                              my_dir_list = dir_list_small_noise_10k,
                              my_metrics_name = SHARED_BUCK_METRIC_NAME,
                              x_axis_var_name = "shared_buckets_number",
                              precision_var_name = "precision",
                              recall_var_name = "recall")








