import pandas as pd
import sys 

# given an lsh result file of signature similarities csv file
# like:
# doc1,doc1,signature_similarity,shared_buckets_number
# 1,75517,0.02,1
# 1,137281,0.01,1
# 1,145208,0.02,1
# 1,177139,0.02,1

# save a file with only the pairs for which signature_similarity == 1.0

# usage for our case (from LSH external folder)
# > python -m near_duplicate_doc_lsh.data_analysis.isolate_sig_sim_ones data_near_duplicate\\robust\\lsh_results\\nba_10_nbu_10000000_sgn_shl_9_sigl_100_bit_uint32_no_noise_0\\signature_sim.csv  data_near_duplicate\\robust\\original_index.csv

import sys

def main():

    signature_similarity_field_name = "signature_similarity"
    shared_buckets_number_name = "shared_buckets_number"
    
    sig_sim_file_name = sys.argv[1]
    only_ones_sig_sim_output_file_name = sys.argv[2]
    
    sig_sim_pd = pd.read_csv(sig_sim_file_name)
    
    filtered_df = sig_sim_pd[sig_sim_pd[signature_similarity_field_name] == 1.0]
    
    filtered_df.drop(columns = [signature_similarity_field_name,
                                shared_buckets_number_name])
    
    filtered_df.to_csv(only_ones_sig_sim_output_file_name,
                       index = False)
    

if __name__ == "__main__":
    main()
