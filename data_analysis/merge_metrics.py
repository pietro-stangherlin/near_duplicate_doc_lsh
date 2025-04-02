# merge metrics and metadata in a unique data.frame
# and save it as a csv

# Testing needed

import json
import os
import pandas as pd
import near_duplicate_doc_lsh.data_analysis.analysis_funs as anfn

if __name__ == "__main__":
    
    combined_meta_metrics = []
    
    
    base_directory = "data_near_duplicate\\robust\\lsh_results"
    subfolder_names = anfn.ListSubfolders(base_directory)
    
    output_json_path = "combined_meta_metrics.json"

    # Relative file names to read in each subfolder
    metadata_name = "metadata.json"
    metrics_name = "metrics.csv"

    # Iterate through each subfolder
    for subfolder in os.listdir(base_directory):
        subfolder_path = os.path.join(base_directory, subfolder)
        
        # Ensure it's a directory
        if os.path.isdir(subfolder_path):
            
            # Paths to the two target files
            metadata_path = os.path.join(subfolder_path, metadata_name)
            metrics_path = os.path.join(subfolder_path, metrics_name)

            # Load the JSON file
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # Load the CSV file
            metrics = pd.read_csv(metrics_path)
            
            el = {
                    "collection_params": metadata["collection_params"],
                    "minhash_params": metadata["minhash_params"],
                    "lsh_params": metadata["lsh_params"],
                    "sorted_signature_similarity": list(metrics["sorted_signature_similarities"]),
                    "precision": list(metrics["precision"]),
                    "recall": list(metrics["recall"])
                }
            
            combined_meta_metrics.append(el)

    
    with open(output_json_path, 'w') as f:
        json.dump(combined_meta_metrics, f, indent=4)
               

