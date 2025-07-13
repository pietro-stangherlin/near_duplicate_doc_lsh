rm(list = ls())

# do the same for robust
dir_list_all <- list.dirs(path = "../../data_near_duplicate/arxiv/lsh_results")
dir_list = dir_list_all[2:length(dir_list_all)]

# Constants ----------------- ----------------------------

SHARED_BUCK_METRIC_NAME <- "metrics_shared_buckets_number.csv"
SIGN_METRIC_NAME <- "metrics_signature_similarity.csv"

PCH_PRECISION = 16
PCH_RECALL = 8


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

SIGL_PREFIX <- "sig_"
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




# compare one parameter fixing all the others


# Signature Length ----------------------------------------------

# Noise quantity ------------------------------------------------

# Duplicates percentage -----------------------------------------

# Number of bands -----------------------------------------------

# Number of buckets ---------------------------------------------


# Plotting function ------------

# x= precision and/or recall
# signature similarity or shared buckets number

# fix all other parameters
# and vary just one

#' @param params_list (list): list of type ()

PlotSimMetricsVSPrecRecOneParam <- function(params_list,
                                            prefix_list,
                                            my_sim_name,
                                            x_axis_var_name,
                                            precision_var_name,
                                            recall_var_name,
                                            my_dir_list,
                                            my_xlim = c(0, 1),
                                            my_ylim = c(0.4, 1),
                                            my_xlab = ""){
  
  all_indexes <- 1:length(params_list)
  
  index_not_fixed_param <- which(params_list > 1)
  
  if(length(index_not_fixed_param) > 1){
    print("Error: more than one parameter has more than one value, leaving")
    return(NULL)
  }
  
  fixed_params_indexes <- setdiff(all_indexes, index_not_fixed_param)
  
  text_to_select = rep(NA, length(fixed_params_indexes))
  
  for (i in fixed_params_indexes){
    par_name = names(params_list)[i]
    text_to_select[i] = paste0(prefix_list[[par_name]], params_list[[par_name]],
                               collapse = "")
  }
  
  pattern <- paste0("(?=.*", text_to_select, ")", collapse = "")
  
  selected_dirs <- my_dir_list[grep(pattern,my_dir_list,
                                    perl = TRUE)]
  
  not_fixed_par_name = names(params_list)[index_not_fixed_param]
  
  # first value: reference plot
  
  text_to_select = paste0(prefix_list[[not_fixed_par_name]],
                          params_list[[not_fixed_par_name]][1],
                          collapse = "")
  
  used_dir <- my_dir_list[grep(text_to_select,selected_dirs)]
  
  metrics_df <- read.csv(paste0(c(used_dir, my_sim_name),
                                collapse = "/"))
  
  plot(metrics_df[,x_axis_var_name],
       metrics_df[,precision_var_name],
       col = 1,
       xlim = my_xlim,
       ylim = my_ylim,
       xlab = my_xlab,
       ylab = "metric",
       pch = PCH_PRECISION)
  
  points(metrics_df[,x_axis_var_name],
         metrics_df[,recall_var_name],
         pch = PCH_RECALL, 
         col = 1)
  
  
  # other values: points on the reference plot
  
  for(i in params_list[[index_not_fixed_param]][2:]){
    
    text_to_select = paste0(prefix_list[[not_fixed_par_name]], val,
                               collapse = "")
    
    used_dir <- my_dir_list[grep(text_to_select,selected_dirs)]
    
    metrics_df <- read.csv(paste0(c(used_dir, my_metrics_name),
                                     collapse = "/"))
    
    

    
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









