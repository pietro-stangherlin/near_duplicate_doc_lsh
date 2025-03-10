# make the signature for the original only data

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts.params import parameters as pm
from near_duplicate_doc_lsh.project.src import utils as ut

import numpy as np
import os
import json

# helper functions

# NOTE: IMPORTANT -> check where SIGNATURE LENGTH is used in the code
# it's also possible it's implicitly used by counting the 
# number of rows in hash param matrix

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.minhash_original

# MinHash load function
def LoadMinhashParamsFile(file_path):
    
    with open(file_path, 'r') as file:
        params = json.load(file)
        
        params_dict = {
        pm.SHINGLE_LEN_FIELD_NAME: params[pm.SHINGLE_LEN_FIELD_NAME],
        pm.SHINGLE_HASH_FUN_FIELD_NAME: getattr(hashing, params[pm.SHINGLE_HASH_FUN_FIELD_NAME]),
        pm.SIGNATURE_LEN_FIELD_NAME: params[pm.SIGNATURE_LEN_FIELD_NAME],
        pm.MINHASH_HASH_FUN_FIELD_NAME: getattr(hashing, params[pm.MINHASH_HASH_FUN_FIELD_NAME]),
        pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME: np.array(params[pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME], dtype = pm.INT_TYPE_64),
        pm.MINHASH_BIT_TYPE_FIELD_NAME: params[pm.MINHASH_BIT_TYPE_FIELD_NAME]}
    
        return params_dict
    
# cycle for all minhash parameters files
# for each combination if the folder already exists: do nothing
# else make it and populate with both:
# - signature_db of original data
# - metadata file

if __name__ == "__main__":

    counter = 0
    
    # for each metadata file
    for param_filename in os.listdir(pm.MINHASH_PARAMS_FOLDER):
        
        param_file_path = ut.JoinPaths(pm.MINHASH_PARAMS_FOLDER, param_filename)

        par_dict = LoadMinhashParamsFile(file_path = param_file_path)
        
        # check if 32 or 64 bit hash
        bit_type_str = par_dict[pm.MINHASH_BIT_TYPE_FIELD_NAME]
        bit_type = np.uint32 if bit_type_str == 'uint32' else np.uint64

        
        # make folder (this can be turned into a function)
        signature_folder_relative_path = ut.MakeRelativeSignatureFolderPath(shingle_len = par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                                                            signature_len = par_dict[pm.SIGNATURE_LEN_FIELD_NAME],
                                                                            bit_type = bit_type_str)
        
        
        signature_folder_full_path = ut.JoinPaths(pm.SIGNATURE_DB_ORIGINAL_FOLDER,
                                               signature_folder_relative_path + "\\")
        
        ut.MakeDir(signature_folder_full_path)
        
        signature_db_full_path = ut.JoinPaths(signature_folder_full_path,
                                            pm.SIGNATURE_DB_FILE_NAME_RELATIVE)
        
        # copy param file in the subfolder
        ut.CopyFile(src = param_file_path,
                dst = ut.JoinPaths(signature_folder_full_path,
                                pm.MINHASH_PARAMETERS_COPY_RELATIVE_NAME))
        
        # actual procedure
        # Add original data (no clones) to Signature database

        # here take always the original
        macro.MinHashPopulateSignatureSQL(file_in_full_path = pm.ROBUST_ORIGINAL_PATH,
                                    signature_db_full_path = signature_db_full_path,
                                    id_name = pm.ID_FIELD_NAME,
                                    content_name = pm.CONTENT_FIELD_NAME,
                                    shingle_len = par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                    shingle_hash_fun = par_dict[pm.SHINGLE_HASH_FUN_FIELD_NAME],
                                    minhash_hash_param_matrix = par_dict[pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME],
                                    minhash_hash_fun = par_dict[pm.MINHASH_HASH_FUN_FIELD_NAME],
                                    minhash_int_type = bit_type,
                                    num_sql_insertions = pm.NUM_SQL_INSERTIONS,
                                    match_string = r'\{(.*)\}')
        
        counter += 1
        print(f"File {counter} written!")
