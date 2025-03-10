from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.project.src import lsh
from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import utils as ut

from near_duplicate_doc_lsh.real_data_scripts.params import parameters as pm

import csv
import os
import json
import time

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.lsh_all

def LoadLshParamsFile(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
        
        params_dict = {
        pm.BANDS_NUMBER_FIELD_NAME: params[pm.BANDS_NUMBER_FIELD_NAME],
        pm.BUCKETS_NUMBER_FIELD_NAME: params[pm.BUCKETS_NUMBER_FIELD_NAME]}
    
        return params_dict


if __name__ == "__main__":
    
    # first load file where each row is a name of already done
    # lsh result folder: if encountered this is skipped
    # NOTE: checking needed
    set_already_done_lsh_result_folders = ut.LoadCompletedFolders(pm.LSH_RESULT_DONE_FOLDERS_NAMES_FILE)
    
    counter = 0
    
    # iterate over LSH parameters file
    for lsh_params_file_name in os.listdir(pm.LSH_PARAMS_FOLDER):
        lsh_par_dict = LoadLshParamsFile(file_path = os.path.join(pm.LSH_PARAMS_FOLDER,
                                                              lsh_params_file_name))
        print(lsh_par_dict)

        n_bands = lsh_par_dict[pm.BANDS_NUMBER_FIELD_NAME]
        n_buckets = lsh_par_dict[pm.BUCKETS_NUMBER_FIELD_NAME]
        
        # iterate over all duplicates (original + duplicates) signatures db folder
        for sig_folder in os.listdir(pm.SIGNATURE_DB_DUPLICATES_FOLDER):
            
            signature_folder_path = os.path.join(pm.SIGNATURE_DB_DUPLICATES_FOLDER,
                                                 sig_folder + "\\")
            
            lsh_folder_relative_name = f"nba_{n_bands}_nbu_{n_buckets}_" + sig_folder
            
            # debug
            print(f"lsh relative folder name: {lsh_folder_relative_name}")
            
            # checking needed
            if lsh_folder_relative_name not in set_already_done_lsh_result_folders:
                
                # debug
                print("lsh relative folder name is not present in the already done")
                
                # write to set
                set_already_done_lsh_result_folders.add(lsh_folder_relative_name)
            
                lsh_result_folder = ut.JoinPaths(pm.LSH_RESULTS_FOLDER,
                                                lsh_folder_relative_name + "\\")
                
                ut.MakeDir(lsh_result_folder)
                
                # DUPLICATE INDEX COPY --------------------------------------
                ut.CopyFile(src = os.path.join(signature_folder_path,
                                            pm.DUPLICATES_INDEX_NAME),
                            dst = os.path.join(lsh_result_folder,
                                            pm.DUPLICATES_INDEX_NAME))
                
                # get the signature database path
                signature_db_path = ut.JoinPaths(signature_folder_path,
                                                pm.SIGNATURE_DB_FILE_NAME_RELATIVE)
                
                
                # read metadata to get signature length
                metadata_dict = ut.LoadMetadata(ut.JoinPaths(signature_folder_path,
                                             pm.METADATA_FILE_NAME))
                    
                signature_len = metadata_dict[pm.MINHASH_METADATA_PARAMS_NAME][pm.SIGNATURE_LEN_FIELD_NAME]
            
                # Iterates over all signature database rows
                # populate LSH band data structure

                # generate hash functions for lsh bands hashing ----------------------
                my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = n_bands,
                                                                            band_size = signature_len // n_bands,
                                                                            modulo = n_buckets,
                                                                            seed = pm.SEED_LSH)

                my_break_points = lsh.GenerateBreakPoints(n = signature_len,
                                                        n_bands = n_bands)

                # initialize LSH bands list data instance
                LshManyBands = lsh.LSHManyBandsBucketLists(n_bands = n_bands,
                                                        n_buckets = n_buckets,
                                                        signature_len = signature_len,
                                                        hash_function_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = n_bands,
                                                                            band_size = signature_len // n_bands,
                                                                            modulo = n_buckets,
                                                                            seed = pm.SEED_LSH))
                
                # open database connection
                SigSQL = mh.SignaturesSQLite(database_name = signature_db_path)

                # define rows iterator
                fetched_rows_iterator = SigSQL.fetch_all_rows()
                
                start = time.time()
                LshManyBands.AddIter(iterator = fetched_rows_iterator)
                stop = time.time()   

                time_populating_lsh = stop - start
                print(f"LSH populated in {int(stop - start)} seconds")

                #!!!!!!!!! Bootleneck !!!!!!
                start_find_sim = time.time()
                temp_all_combinations = macro.FindAllCombinations(lsh_many_bands = LshManyBands,
                                                                  sig_sql = SigSQL)
                stop_find_sim = time.time()

                SigSQL.close_database()

                time_finding_id_same_bucket = stop_find_sim - start_find_sim
                    
                # sort key values
                sorted_tuples_list = sorted(temp_all_combinations.items())

                # write signature similarity csv
                signature_sim_full_path = ut.JoinPaths(lsh_result_folder,
                                                    pm.SIGNATURE_SIMILARITY_NAME_CSV)


                with open(signature_sim_full_path, mode= 'w', newline='') as fout:
                    writer = csv.writer(fout)
                    
                    # write header
                    writer.writerow([pm.SIGNATURE_SIMILARITY_DOC1_HEADER,
                                    pm.SIGNATURE_SIMILARITY_DOC1_HEADER,
                                    pm.SIGNATURE_SIMILARITY_DOC1_SIGSIM_HEADER,
                                    pm.DOC1_DOC2_SHARED_BUCKETS_NUMBER])
                    
                    for ((first_el, second_el), value) in sorted_tuples_list:
                        writer.writerow([first_el, second_el, value[0], value[1]])
                
                # UPDATE AND WRITE METADATA ----------------------------------------------
                metadata_dict[pm.LSH_METADATA_PARAMS_NAME] = {pm.BANDS_NUMBER_FIELD_NAME: n_bands,
                                                            pm.BUCKETS_NUMBER_FIELD_NAME: n_buckets,
                                                            pm.TIME_POPULATE_LSH_NAME : time_populating_lsh,
                                                            pm.TIME_FIND_SAME_BUCKET_NAME: time_finding_id_same_bucket}
                
                ut.WriteMetadata(ut.JoinPaths(lsh_result_folder,
                                                pm.METADATA_FILE_NAME))
                
                # overwrite done lsh result folder names
                ut.UpdateCompletedFolders(pm.LSH_RESULT_DONE_FOLDERS_NAMES_FILE,
                                          set_already_done_lsh_result_folders)

                counter += 1
                print(f"File {counter} written!")

