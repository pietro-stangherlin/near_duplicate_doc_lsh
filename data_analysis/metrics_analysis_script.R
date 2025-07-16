rm(list = ls())

dir_list_all <- list.dirs(path = "../../data_near_duplicate/robust/lsh_results")
dir_list = dir_list_all[2:length(dir_list_all)]



# Constants ----------------- ----------------------------

SHARED_BUCK_METRIC_NAME <- "metrics_shared_buckets_number.csv"
SIGN_METRIC_NAME <- "metrics_signature_similarity.csv"

SIGN_SIM_NAME = "signature_similarity"
SHARED_BUCK_NAME = "shared_buckets_number"

PCH_PRECISION = 16
PCH_RECALL = 8
PLOT_TYPE = "b"

PRECISION_NAME = "precision"
RECALL_NAME = "recall"



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

# Plotting function ------------

# x= precision and/or recall
# signature similarity or shared buckets number

# fix all other parameters
# and vary just one

#' @param params_list (list): list of type ()
#' @param prefix_list (list)

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
  
  index_not_fixed_param <- which(length(params_list) > 1)
  
  if(length(index_not_fixed_param) > 1){
    print("Error: more than one parameter has more than one value, leaving")
    return(NULL)
  }
  
  fixed_params_indexes <- setdiff(all_indexes, index_not_fixed_param)
  fixed_params_names <- names(params_list)[fixed_params_indexes]
  
  # Fixed params folders name subset
  fixed_params_values <- rep(NA, length(fixed_params_indexes))
  text_to_select = rep(NA, length(fixed_params_indexes))
  
  for (i in 1:length(fixed_params_indexes)){
    actual_index <- fixed_params_indexes[i]
    par_name = names(params_list)[actual_index]
    fixed_params_values[i] <- params_list[[par_name]]
    text_to_select[i] = paste0(prefix_list[[par_name]],
                               params_list[[par_name]],
                               collapse = "")
  }
  
  pattern <- paste0("(?=.*", text_to_select, "(_|$))", collapse = "")
  
  selected_dirs <- my_dir_list[grep(pattern,
                                    my_dir_list,
                                    perl = TRUE)]
  
  # Not Fixed param sub folders conditioned on the previuos found
  not_fixed_par_name = names(params_list)[index_not_fixed_param]
  
  # first value: reference plot
  
  text_to_select = paste0(prefix_list[[not_fixed_par_name]],
                          params_list[[not_fixed_par_name]][1],
                          collapse = "")
  
  used_dir <- selected_dirs[grep(text_to_select,selected_dirs)]
  
  
  metrics_df <- read.csv(paste0(c(used_dir, my_sim_name),
                                collapse = "/"))
  
  plot(metrics_df[,x_axis_var_name],
       metrics_df[,precision_var_name],
       col = 1,
       xlim = my_xlim,
       ylim = my_ylim,
       xlab = my_xlab,
       ylab = "metric",
       pch = PCH_PRECISION,
       type = PLOT_TYPE,
       main = not_fixed_par_name)
  
  points(metrics_df[,x_axis_var_name],
         metrics_df[,recall_var_name],
         pch = PCH_RECALL, 
         col = 1,
         type = PLOT_TYPE)
  
  
  # other values: points on the reference plot
  
  color_index = 1
  for(val in params_list[[index_not_fixed_param]][-1]){
    color_index = color_index + 1
    
    text_to_select = paste0(prefix_list[[not_fixed_par_name]], val,
                               collapse = "")
    
    used_dir <- my_dir_list[grep(text_to_select,selected_dirs)]
    
    metrics_df <- read.csv(paste0(c(used_dir, my_sim_name),
                                     collapse = "/"))
    
    points(metrics_df[,x_axis_var_name],
           metrics_df[,precision_var_name],
           col = color_index,
           pch = PCH_PRECISION,
           type = PLOT_TYPE)
    
    points(metrics_df[,x_axis_var_name],
           metrics_df[,recall_var_name],
           pch = PCH_RECALL,
           col = color_index,
           type = PLOT_TYPE)
   
  }
  
  legend("topleft",
         legend = paste(fixed_params_names, ": ", fixed_params_values),
         bty = "n")
  
  legend("bottomright",
         legend = c(PRECISION_NAME, RECALL_NAME),
         pch = c(PCH_PRECISION, PCH_RECALL),
         bty = "n")
  
  legend("bottomleft",
         legend = paste(not_fixed_par_name, ": ", params_list[[index_not_fixed_param]]),
         col = 1:color_index,
         bty = "n",
         lty = 1,
         lwd = 2)
  
}


# compare one parameter fixing all the others


# Noise quantity ------------------------------------------------

temp_param_list = EMPTY_PARAMS_LIST
temp_param_list[[NOISE_QUANT_NAME]] = NOISE_QUANT
temp_param_list[[DUPLICATES_PERCENT_NAME]] = DUPLICATES_PERCENT[1]
temp_param_list[[SIGL_NAME]] = SIGL[1]
temp_param_list[[NBA_NAME]] = NBA[1]
temp_param_list[[NBU_NAME]] = NBU[1]

PlotSimMetricsVSPrecRecOneParam(params_list = temp_param_list,
                                prefix_list = PREFIX_LIST,
                                my_sim_name = SIGN_METRIC_NAME,
                                x_axis_var_name = SIGN_SIM_NAME,
                                precision_var_name = PRECISION_NAME,
                                recall_var_name = RECALL_NAME,
                                my_dir_list = dir_list,
                                my_xlim = c(0.4, 1),
                                my_ylim = c(0.4, 1),
                                my_xlab = SIGN_SIM_NAME)

# Duplicates percentage -----------------------------------------

# Signature Length ----------------------------------------------

# Number of bands -----------------------------------------------

# Number of buckets ---------------------------------------------











