# make the signature for the original only data

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts import make_params_files as mpf

import os
import csv
import json
import time

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_minhash_original

robust_original_path = "data_near_duplicate\\robust\\robust_id2.json"

minhash_params_folder = "near_duplicate_doc_lsh\\real_data_scripts\\minhash_params\\"

signature_db_folder = "data_near_duplicate\\signatures_db_original\\"

# cycle for all minhash parameters files
# for each combination if the folder already exists: do nothing
# else make it and populate with both:
# - signature_db of original data
# - metadata file

# for each metadata file
for param_filename in os.listdir(minhash_params_folder):
    param_file_path = os.path.join(param_filename, minhash_params_folder)
    
    # open param file
    # get params and save 
    
    
    # get 
    # make folder in signature path
    



os.makedirs(rmp.signature_db_folder, exist_ok = True)
signature_db_full_path = os.path.join(rmp.signature_db_folder,
                                      rmp.signature_db_relative_path)

# Actual procedure ------------------------------------------------------

# 1) Add original Data
# Add original data (no clones) to Signature database

start = time.time()

# here take always the original
macro.MinHashPopulateSignatureSQL(file_in_full_path = robust_original_path,
                                signature_db_full_path = signature_db_full_path,
                                id_name = rmp.ID_NAME,
                                content_name = rmp.CONTENT_NAME,
                                shingle_len = rmp.SHINGLE_LEN,
                                shingle_hash_fun = rmp.SHINGLE_HASH_FUN,
                                minhash_hash_param_matrix = hash_params_matrix,
                                minhash_hash_fun = rmp.MINHASH_HASH_FUN,
                                minhash_int_type = rmp.MINHASH_INT_TYPE,
                                num_sql_insertions = rmp.NUM_SQL_INSERTIONS,
                                match_string = r'\{(.*)\}')

stop = time.time()

print("Only original data Signatures")
print(f"Time: {stop - start}")