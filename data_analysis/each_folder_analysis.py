# iterate analysis_funs in for each subfolder in a specified folder
# save the result as a csv

# Instructions
# >>> python -m near_duplicate_doc_lsh.data_analysis.each_folder_analysis

import os
import pandas as pd
import near_duplicate_doc_lsh.data_analysis.analysis_funs as anfn

def list_subfolders(folder_path):
    # Use os.walk to iterate through the directory
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders


if __name__ == "__main__":
    # Replace 'your_folder_path' with the path of your target folder
    base_directory = "data_near_duplicate\\robust\\lsh_results"
    subfolder_names = list_subfolders(base_directory)

    # Relative file names to read in each subfolder
    collection_index = "robust_index.csv"
    sig_sim = "signature_sim.csv"
    output_file_name = "metrics.csv"

    # Iterate through each subfolder
    for subfolder in os.listdir(base_directory):
        subfolder_path = os.path.join(base_directory, subfolder)
        
        # Ensure it's a directory
        if os.path.isdir(subfolder_path):
            # Path to the output file (metrics.csv)
            output_file_path = os.path.join(subfolder_path, output_file_name)
            
            # Skip the procedure if metrics.csv already exists
            if os.path.exists(output_file_path):
                print(f"Skipping {subfolder}, metrics.csv already exists.")
                continue
            
            # Paths to the two target files
            collection_index_path = os.path.join(subfolder_path, collection_index)
            sig_sim_path = os.path.join(subfolder_path, sig_sim)
            
            # Check if both files exist
            if os.path.exists(collection_index_path) and os.path.exists(sig_sim_path):
                # Read the files
                true_duplicates_df = pd.read_csv(collection_index_path)
                signature_sim_df = pd.read_csv(sig_sim_path)
                
                true_duplicates_tuples_set = set(tuple(row) for row in true_duplicates_df.itertuples(index=False, name=None))
                
                signature_similarity_reverse_dict = anfn.MakeReverseDictionary(
                    signature_sim_df=signature_sim_df,
                    doc1_id_name="doc1",
                    doc2_id_name="doc1.1"  # due to a mistake
                )
    
                metrics_df = anfn.ComputePrecisionRecallVsSignatureSimilarity(
                    true_duplicates_tuples_set=true_duplicates_tuples_set,
                    signature_similarity_reverse_dict=signature_similarity_reverse_dict
                )
                
                # Save the output to a file in the same subfolder
                metrics_df.to_csv(output_file_path, index=False)

                print(f"Processed and saved file in {subfolder}")
            else:
                print(f"One or both files are missing in {subfolder}")




 
