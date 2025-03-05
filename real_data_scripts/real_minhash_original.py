# make the signature for the original only data
# first try to just one collection
# then try to make a for cycle

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts import real_minhash_params as rmp

import os
import csv
import json
import time

# instructions:
# exectute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_minhash_original


os.makedirs(rmp.signature_db_folder, exist_ok = True)
signature_db_full_path = os.path.join(rmp.signature_db_folder,
                                      rmp.signature_db_relative_path)


# MinHASH ----------------------------------------------------------
# generate permutations params
hash_params_matrix = hashing.GenerateNumpyArray(num_rows = 100,
                                                num_cols = 2,
                                                seed = 123,
                                                reshape = True,
                                                int_type = rmp.INT_TYPE_64)

# SQL -----------------------------------------------------------------

# first make subfolder, with respect to the duplicates file folder
# where to store the signature database

# Actual procedure ------------------------------------------------------

# 1) Add original Data
# Add original data (no clones) to Signature database

start = time.time()

# here take always the original
macro.MinHashPopulateSignatureSQL(file_in_full_path = rmp.file_in,
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