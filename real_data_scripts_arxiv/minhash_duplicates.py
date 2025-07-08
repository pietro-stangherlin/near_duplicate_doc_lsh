# make the signature for the duplicates only data
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import parameters as pm
# this import needs an "aestethic" fix, maybe
from near_duplicate_doc_lsh.real_data_scripts_arxiv import minhash_original as mho
from near_duplicate_doc_lsh.project.src import utils as ut

import time
import numpy as np
import os

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates

# cycle for all minhash parameters files
# for each combination if the folder already exists: do nothing
# else make it and populate with both:
# - signature_db of original data
# - metadata file

if __name__ == "__main__":
    
    # first load file where each row is a name of already done
    # signature result folder: if encountered this is skipped
    # NOTE: checking needed
    set_done_signature_db_clones_folder_names = ut.LoadCompletedFolders(pm.MINHASH_SIGNATURE_DB_DUPLICATES_DONE_FOLDERS_NAMES_FILE)

    counter = 0
    
    # for each subfolder holding a signature_db
    for signa_original_folder in os.listdir(pm.SIGNATURE_DB_ORIGINAL_FOLDER):
        signa_original_folder_path = ut.JoinPaths(pm.SIGNATURE_DB_ORIGINAL_FOLDER,
                                                  signa_original_folder)
        
        # load parameters file: ----------------
        par_dict = mho.LoadMinhashParamsFile(file_path = ut.JoinPaths(signa_original_folder_path,
                                                                      pm.MINHASH_PARAMETERS_COPY_RELATIVE_NAME))
        
        # check if 32 or 64 bit hash
        bit_type_str = par_dict[pm.MINHASH_BIT_TYPE_FIELD_NAME]
        bit_type = np.uint32 if bit_type_str == 'uint32' else np.uint64
        
        # original signature db file: --------------------
        signature_db_original_file_path = ut.JoinPaths(signa_original_folder_path,
                                                       pm.SIGNATURE_DB_FILE_NAME_RELATIVE)
        
        # ONLY DUPLICATES COLLECTION ----------------------------------------------
        for duplicates_folder in os.listdir(pm.ONLY_DUPLICATES_COLLECTION_FOLDER_PATH):
            
            duplicates_collection_original_folder_path = ut.JoinPaths(pm.ONLY_DUPLICATES_COLLECTION_FOLDER_PATH,
                                                                      duplicates_folder)
            
            # collection of only duplicates
            robust_duplicates_file_path = duplicates_collection_original_folder_path + "\\" + pm.ROBUST_DUPLICATES_NAME
            
            # try to concatenate names, hoping in no path length problems
            # make folder (this can be turned into a function)
            new_signature_folder_relative_path = "_".join([signa_original_folder,
                                                       duplicates_folder])
            
            # debug
            print(f"signature db relative folder name: {new_signature_folder_relative_path}")
            if new_signature_folder_relative_path not in set_done_signature_db_clones_folder_names:
                
                # debug
                print("signature db relative folder name is not present in the already done")
                
                set_done_signature_db_clones_folder_names.add(new_signature_folder_relative_path)
                
                new_signature_folder_full_path = ut.JoinPaths(pm.SIGNATURE_DB_DUPLICATES_FOLDER,
                                                              new_signature_folder_relative_path + "\\")

                os.makedirs(new_signature_folder_full_path, exist_ok = True)
                
                # INDEX -------------------------------------------------------------------
                # copy duplicates index in the new folder
                # original index
                duplicates_original_index_path = ut.JoinPaths(duplicates_collection_original_folder_path,
                                                            pm.DUPLICATES_INDEX_NAME)
                
                copy_duplicates_index_path = ut.JoinPaths(new_signature_folder_full_path,
                                                          pm.DUPLICATES_INDEX_NAME)
                
                ut.CopyFile(src = duplicates_original_index_path,
                            dst = copy_duplicates_index_path)
                
                # SIGNATURE DB COPY ----------------------------------------------------------
                # the one where the duplicates are added
                signature_db_copy_full_path = new_signature_folder_full_path + pm.SIGNATURE_DB_FILE_NAME_RELATIVE
                # copy it in the new folder
                ut.CopyFile(src = signature_db_original_file_path,
                            dst = signature_db_copy_full_path)

                # POPULATE SIGNATURE DB WITH DUPLICATES ---------------------------------------
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
                                        batch_size = pm.NUM_SQL_INSERTIONS,
                                        match_string = r'\{(.*)\}')

                stop = time.time()
                
                # METADATA -----------------------------------------------------------------
                # update metadata and write them in the new folder
                metadata_dict = ut.LoadMetadata(ut.JoinPaths(duplicates_collection_original_folder_path,
                                                            pm.METADATA_FILE_NAME))
                
                metadata_dict[pm.MINHASH_METADATA_PARAMS_NAME] = {pm.SHINGLE_LEN_FIELD_NAME: par_dict[pm.SHINGLE_LEN_FIELD_NAME],
                                                pm.SIGNATURE_LEN_FIELD_NAME: par_dict[pm.SIGNATURE_LEN_FIELD_NAME],
                                                pm.BIT_TYPE_NAME: bit_type_str,
                                                pm.TIME_NAME: stop - start}
            
                
                ut.WriteMetadata(file_path = new_signature_folder_full_path + pm.METADATA_FILE_NAME,
                                  metadata_dict = metadata_dict)
                
                 # overwrites done minhash result folder names
                ut.UpdateCompletedFolders(pm.MINHASH_SIGNATURE_DB_DUPLICATES_DONE_FOLDERS_NAMES_FILE,
                                          set_done_signature_db_clones_folder_names)

                counter += 1
                print(f"File {counter} written!")