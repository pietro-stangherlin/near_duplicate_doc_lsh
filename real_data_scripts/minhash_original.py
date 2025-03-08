# make the signature for the original only data

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts import make_params_files as mpf
from near_duplicate_doc_lsh.real_data_scripts import parameters as pm

import numpy as np
import os
import csv
import json
import time

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_minhash_original

# MinHash load function
def LoadMinhashParamsFile(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
        
        params_dict = {
        mpf.SHINGLE_LEN_FIELD_NAME: params[mpf.SHINGLE_LEN_FIELD_NAME],
        mpf.SHINGLE_HASH_FUN_FIELD_NAME: getattr(hashing, params[mpf.SHINGLE_HASH_FUN_FIELD_NAME]),
        mpf.SIGNATURE_LEN_FIELD_NAME: getattr(hashing, params[mpf.SIGNATURE_LEN_FIELD_NAME]),
        mpf.MINHASH_HASH_FUN_FIELD_NAME: getattr(hashing, params[mpf.MINHASH_HASH_FUN_FIELD_NAME]),
        mpf.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME: np.array(params[mpf.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME], dtype = mpf.INT_TYPE_64)}
    
        return params_dict
    
# cycle for all minhash parameters files
# for each combination if the folder already exists: do nothing
# else make it and populate with both:
# - signature_db of original data
# - metadata file

# for each metadata file
for param_filename in os.listdir(pm.MINHASH_PARAMS_FOLDER):
    param_file_path = os.path.join(param_filename, pm.MINHASH_PARAMS_FOLDER)
    
    # check if 32 or 64 bit hash
    bit = 32
    if "64" in param_filename:
        bit = 64
    
    
    par_dict = LoadMinhashParamsFile(file_path = param_file_path)
    
    # make folder (this can be turned into a function)
    signature_folder_relative_path = (f"sgn_shl_{par_dict[mpf.SHINGLE_LEN_FIELD_NAME]}",
                                      f"sigl_{par_dict[mpf.SIGNATURE_LEN_FIELD_NAME]}",
                                      f"bit_{bit}\\").join()
    
    os.makedirs(signature_folder_relative_path, exist_ok = True)
    signature_db_full_path = os.path.join(mpf.SIGNATURE_DB_FILE_NAME_RELATIVE,
                                      signature_folder_relative_path)
    
    # actual procedure
    # Add original data (no clones) to Signature database
    
    start = time.time()

    # here take always the original
    macro.MinHashPopulateSignatureSQL(file_in_full_path = pm.ROBUST_ORIGINAL_PATH,
                                signature_db_full_path = signature_db_full_path,
                                id_name = pm.ID_FIELD_NAME,
                                content_name = pm.CONTENT_FIELD_NAME,
                                shingle_len = par_dict[mpf.SHINGLE_LEN_FIELD_NAME],
                                shingle_hash_fun = par_dict[pm.SHINGLE_HASH_FUN_FIELD_NAME],
                                minhash_hash_param_matrix = par_dict[pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME],
                                minhash_hash_fun = par_dict[pm.MINHASH_HASH_FUN_FIELD_NAME],
                                minhash_int_type = rmp.MINHASH_INT_TYPE,
                                num_sql_insertions = pm.NUM_SQL_INSERTIONS,
                                match_string = r'\{(.*)\}')

    stop = time.time()

    print("Only original data Signatures")
    print(f"Time: {stop - start}")
    
    # save metadata
