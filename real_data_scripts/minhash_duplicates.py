# make the signature for the duplicates only data
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts import parameters as pm
# this import needs an "aestethic" fix, maybe
from near_duplicate_doc_lsh.real_data_scripts import minhash_original as mho

import time
import numpy as np
import os
import shutil
import json

# NOTE: IMPORTANT -> check where SIGNATURE LENGTH is used in the code
# it's also possible it's implicitly used by counting the 
# number of rows in hash param matrix

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates
    
# cycle for all minhash parameters files
# for each combination if the folder already exists: do nothing
# else make it and populate with both:
# - signature_db of original data
# - metadata file

if __name__ == "__main__":

    counter = 0
    
    # for each subfolder holding a signature_db
    for signa_original_folder in os.listdir(pm.SIGNATURE_DB_ORIGINAL_FOLDER):
        signa_original_folder_path = os.path.join(pm.SIGNATURE_DB_ORIGINAL_FOLDER,
                                                  signa_original_folder)
        
        # load parameters file: ----------------
        param_file_name_path = os.path.join(signa_original_folder_path,
                                            pm.MINHASH_PARAMETERS_COPY_RELATIVE_NAME)
        
        par_dict = mho.LoadMinhashParamsFile(file_path = param_file_name_path)
        
        # check if 32 or 64 bit hash
        bit_type_str = par_dict[pm.MINHASH_BIT_TYPE_FIELD_NAME]
        bit_type = np.uint32 if bit_type_str == 'uint32' else np.uint64
        
        # original signature db file: --------------------
        signature_db_name_path = os.path.join(signa_original_folder_path,
                                              pm.SIGNATURE_DB_FILE_NAME_RELATIVE)
        
        # consider only duplicates collection
        for duplicates_folder in pm.ONLY_DUPLICATES_COLLECTION_FOLDER_PATH:
            
            duplicates_folder_path = os.path.join(pm.ONLY_DUPLICATES_COLLECTION_FOLDER_PATH,
                                                  duplicates_folder)
            
            robust_duplicates_file_path = duplicates_folder_path + pm.ROBUST_DUPLICATES_NAME
            
            # try to concatenate names, hoping in no path length problems
            # make folder (this can be turned into a function)
            signature_folder_relative_path = "_".join([signa_original_folder,
                                                       duplicates_folder])
            signature_folder_full_path = pm.SIGNATURE_DB_DUPLICATES_FOLDER + signature_folder_relative_path

            os.makedirs(signature_folder_full_path, exist_ok = True)
            
            # the one where the duplicates are added
            signature_db_copy_full_path = signature_folder_full_path + pm.SIGNATURE_DB_FILE_NAME_RELATIVE
            # copy it in the new folder
            shutil.copy(src = signature_db_name_path, dst = signature_db_copy_full_path)

            start = time.time()
            # actual procedure
            macro.MinHashPopulateSignatureSQL(file_in_full_path = robust_duplicates_file_path,
                                    signature_db_full_path = signature_db_copy_full_path,
                                    id_name = pm.ID_FIELD_NAME,
                                    content_name = pm.CONTENT_FIELD_NAME,
                                    shingle_len = par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                    shingle_hash_fun = par_dict[pm.SHINGLE_HASH_FUN_FIELD_NAME],
                                    minhash_hash_param_matrix = par_dict[pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME],
                                    minhash_hash_fun = par_dict[pm.MINHASH_HASH_FUN_FIELD_NAME],
                                    minhash_int_type = bit_type,
                                    num_sql_insertions = pm.NUM_SQL_INSERTIONS,
                                    match_string = r'\{(.*)\}')

            stop = time.time()
            
            # open metadata, update them and write them in the new folder
            
            metadata_duplicates = os.path.join(pm.ONLY_DUPLICATES_COLLECTION_FOLDER_PATH,
                                                  duplicates_folder)
            with open(metadata_duplicates) as metadata_fin:
                metadata_dict = json.load(metadata_fin)
            
            metadata_dict["minhash_params"] = {pm.SHINGLE_LEN_FIELD_NAME: par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                               pm.SIGNATURE_LEN_FIELD_NAME: par_dict[pm.SIGNATURE_LEN_FIELD_NAME],
                                               pm.BIT_TYPE_NAME: bit_type,
                                               pm.TIME_NAME: stop - start}
            
            metadata_new_file_path = signature_folder_full_path + pm.METADATA_FILE_NAME
            
            with open(metadata_new_file_path) as fout:
                json.dump(metadata_dict)
            
            counter += 1
            print(f"File {counter} written!")