# iterate analysis_funs in for each subfolder in a specified folder
# save the result as a csv

# Instructions
# >>> python -m near_duplicate_doc_lsh.data_analysis.each_folder_analysis

import os
import pandas as pd
import near_duplicate_doc_lsh.data_analysis.analysis_funs as anfn


# constants
DOC1_COL_NAME = "doc1"
DOC2_COL_NAME = "doc2"
PAIR_COL_NAME = "pair"
PRECISION_COL_NAME = "precision"
RECALL_COL_NAME = "recall"
SIGNATURE_SIMILARITY_COL_NAME = "signature_similarity"
SHARED_BUCKETS_NUMBER_COL_NAME = "shared_buckets_number"

# two output file names
METRICS_SIGNATURES_SIM_FILE_NAME = "metrics_signature_similarity.csv"
METRICS_SHARED_BUCKETS_NUMBER_FILE_NAME = "metrics_shared_buckets_number.csv"

if __name__ == "__main__":
    base_directory = "data_near_duplicate\\robust\\lsh_results"
    subfolder_names = anfn.ListSubfolders(base_directory)

    # Relative file names to read in each subfolder
    collection_index = "robust_index.csv"
    sig_sim = "signature_sim.csv"


    # Iterate through each subfolder
    for subfolder in os.listdir(base_directory):
        subfolder_path = os.path.join(base_directory, subfolder)
        
        # Ensure it's a directory
        if os.path.isdir(subfolder_path):
            # Path to the output file (metrics.csv)
            output_signature_file_path = os.path.join(subfolder_path, METRICS_SIGNATURES_SIM_FILE_NAME)
            output_shared_buckets_file_path = os.path.join(subfolder_path, METRICS_SHARED_BUCKETS_NUMBER_FILE_NAME)
            
            
            # if at one output file does NOT already exist -> proceed
            if not os.path.exists(output_signature_file_path) or not os.path.exists(output_shared_buckets_file_path):

                # Paths to the two target files
                collection_index_path = os.path.join(subfolder_path, collection_index)
                sig_sim_path = os.path.join(subfolder_path, sig_sim)

                # Check if both files exist
                if os.path.exists(collection_index_path) and os.path.exists(sig_sim_path):
                    # Read the files

                    true_duplicates_tuples_set = anfn.ConvertTrueIndexPdToTupleSet(pd.read_csv(collection_index_path))

                    signature_sim_df = pd.read_csv(sig_sim_path)
                    anfn.AddPairColumnDropSingleOnes(df = signature_sim_df,
                                                    doc1_id_col_name = DOC1_COL_NAME,
                                                    doc2_id_col_name = DOC2_COL_NAME,
                                                    pair_col_name = PAIR_COL_NAME)

            # Skip the procedure if metrics.csv already exists
            if not os.path.exists(output_signature_file_path):
                metrics_signature_df = anfn.PrecisionRecallVsSelectedMetric(lsh_results_pd = signature_sim_df,
                                                                    true_duplicates_tuple_set = true_duplicates_tuples_set,
                                                                    selected_metric_col_name = SIGNATURE_SIMILARITY_COL_NAME,
                                                                    pair_col_name = PAIR_COL_NAME,
                                                                    precision_name = PRECISION_COL_NAME,
                                                                    recall_name = RECALL_COL_NAME)
                    
                # Save the output to a file in the same subfolder
                metrics_signature_df.to_csv(output_signature_file_path, index=False)

                print(f"Processed and saved file in {subfolder}")
            else:
                    print(f"One or both files are missing in {subfolder}")
            
            if not os.path.exists(output_signature_file_path):
                metrics_shared_buckets_df = anfn.PrecisionRecallVsSelectedMetric(lsh_results_pd = signature_sim_df,
                                                                    true_duplicates_tuple_set = true_duplicates_tuples_set,
                                                                    selected_metric_col_name = SHARED_BUCKETS_NUMBER_COL_NAME,
                                                                    pair_col_name = PAIR_COL_NAME,
                                                                    precision_name = PRECISION_COL_NAME,
                                                                    recall_name = RECALL_COL_NAME)
                    
                # Save the output to a file in the same subfolder
                metrics_shared_buckets_df.to_csv(output_shared_buckets_file_path, index=False)
                
                print(f"Processed and saved file in {subfolder}")
            else:
                    print(f"One or both files are missing in {subfolder}")





 
