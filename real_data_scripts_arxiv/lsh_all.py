from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.project.src import lsh
from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import utils as ut

from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import parameters as pm

import csv
import os
import json
import time

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts_arxiv.lsh_all

def LoadLshParamsFile(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
        
        params_dict = {
        pm.BANDS_NUMBER_FIELD_NAME: params[pm.BANDS_NUMBER_FIELD_NAME],
        pm.BUCKETS_NUMBER_FIELD_NAME: params[pm.BUCKETS_NUMBER_FIELD_NAME]}
    
        return params_dict

# debug
def print_first_10_rows(cursor, table_name):
    query = f"SELECT * FROM {table_name} LIMIT 10"
    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"First 10 rows from table '{table_name}':")
    for row in rows:
        print(row)


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
        

        times_buckets = lsh_par_dict[pm.BUCKETS_NUMBER_FIELD_NAME]
        
        # iterate over all duplicates (original + duplicates) signatures db folder
        for sig_folder in os.listdir(pm.SIGNATURE_DB_DUPLICATES_FOLDER):
            
            signature_folder_path = os.path.join(pm.SIGNATURE_DB_DUPLICATES_FOLDER,
                                                 sig_folder + "\\")
            
            lsh_folder_relative_name = f"nba_{n_bands}_nbu_{int(times_buckets // pm.arxiv_no_duplicates_nlines)}_" + sig_folder
            
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

                n_documents = int(metadata_dict[pm.COLLECTION_PARAMS_NAME][pm.ORIGINAL_DOC_NUMBER_NAME]) + int(metadata_dict[pm.COLLECTION_PARAMS_NAME][pm.DUPLICATES_DOC_NUMBER_NAME])
                n_buckets = times_buckets * n_documents
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

                # previous implementation for all steps (NOT USED)
                # temp_all_combinations = macro.FindAllCombinationsPreload(lsh_many_bands = LshManyBands,
                                                                        # sig_sql = SigSQL)

                # get dictionary with
                # key = document pair
                # value = shared buckets number
                doc1_doc2_sharedbucket_dict = LshManyBands.FindAllPairs()

                print(f"got all pairs")

                # delete lsh data structure to save memory
                del LshManyBands

                # in general filter by shared buckets number threshold
                # here is done only to convert to list

                doc1_doc2_sharedbucket_dict = lsh.FilterAllPairsDictBySharedBucketThreshold(pairs_sharedbuckets_dict= doc1_doc2_sharedbucket_dict,
                                                                                            shared_bucket_threshold = 1)

                print(f"filtered by shared bucket number")
                # convert to pd.dataframe
                lsh_pd_df = lsh.ConvertAllPairsListToPdDataframe(pairs_sharedbuckets_list = doc1_doc2_sharedbucket_dict,
                                                                 doc1_col_name = pm.SIGNATURE_SIMILARITY_DOC1_HEADER,
                                                                 doc2_col_name = pm.SIGNATURE_SIMILARITY_DOC2_HEADER,
                                                                 shared_bucket_number_col_name = pm.DOC1_DOC2_SHARED_BUCKETS_NUMBER)
                
                print(f"conversion to pd dataframe")
                # delete dictionary to save memory
                del doc1_doc2_sharedbucket_dict

                # get unique document ids
                unique_doc_ids = lsh.GetUniquesIdSet(pairs_sharedbukets_pd = lsh_pd_df,
                                    doc1_col_name = pm.SIGNATURE_SIMILARITY_DOC1_HEADER,
                                    doc2_col_name = pm.SIGNATURE_SIMILARITY_DOC2_HEADER)
                
                # debug try
                unique_doc_ids = [int(el) for el in unique_doc_ids]
                
                # debug
                
                print(f"got unique doc ids")
                
                # populate {document: signature} cache dictionary
                signature_dict = SigSQL.GetDocSignatureSubsetDictionary(doc_ids_subset = unique_doc_ids,
                                                                        batch_size = 10**4)
                
                #debug
                # check type of signature dict key

                first_key = next(iter(signature_dict))
                print(f"[DEBUG]: signature_dict first key = {first_key}")
                print(f"[DEBUG]: signature_dict type(first key) = {type(first_key)}")

                print(f"got cached signature dict")
                
                # add signature similarity column
                lsh_pd_df[pm.SIGNATURE_SIMILARITY_DOC1_SIGSIM_HEADER] = mh.GetSignatureSimilarityArray(pairs_sharedbukets_pd = lsh_pd_df,
                                                                                                       doc_signature_dict = signature_dict,
                                                                                                       doc1_col_name = pm.SIGNATURE_SIMILARITY_DOC1_HEADER,
                                                                                                        doc2_col_name = pm.SIGNATURE_SIMILARITY_DOC2_HEADER)

                print(f"added signature similarity column")
                # filter out columns for which signature similarity is 0
                lsh_pd_df = lsh_pd_df[lsh_pd_df[pm.SIGNATURE_SIMILARITY_DOC1_SIGSIM_HEADER] > 0]

                print(f"filtered out similarities <= 0")

                stop_find_sim = time.time()

                SigSQL.close_database()
            

                time_finding_id_same_bucket = stop_find_sim - start_find_sim
                    

                # write signature similarity csv
                signature_sim_full_path = ut.JoinPaths(lsh_result_folder,
                                                    pm.SIGNATURE_SIMILARITY_NAME_CSV)
                
                lsh_pd_df.to_csv(signature_sim_full_path, index=False)

                
                # UPDATE AND WRITE METADATA ----------------------------------------------
                metadata_dict[pm.LSH_METADATA_PARAMS_NAME] = {pm.BANDS_NUMBER_FIELD_NAME: n_bands,
                                                            pm.BUCKETS_NUMBER_FIELD_NAME: times_buckets,
                                                            pm.TIME_POPULATE_LSH_NAME : time_populating_lsh,
                                                            pm.TIME_FIND_SAME_BUCKET_NAME: time_finding_id_same_bucket}
                
                ut.WriteMetadata(file_path = ut.JoinPaths(lsh_result_folder, pm.METADATA_FILE_NAME),
                                 metadata_dict = metadata_dict)
                
                # overwrite done lsh result folder names
                ut.UpdateCompletedFolders(pm.LSH_RESULT_DONE_FOLDERS_NAMES_FILE,
                                          set_already_done_lsh_result_folders)

                counter += 1
                print(f"File {counter} written!")

