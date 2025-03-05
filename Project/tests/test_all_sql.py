# test all storing the MinHash Signatures in a SQL single table Database
# LSH band buckets still stored in list of lists data structure
# then all records need to be read again in order to populate the LSH data structure

from ..src import minhash as mh
from ..src import hashing
from ..src import lsh
from ..src import macro
from project.tests import test_all_params as tap

import os
import csv
import json
import time

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# also before running convert the file to utf-8 and remove BOM 
# (from notepad++ encoding, or another way)

# If data is in test_data: (use this in testing)
# >>> python -m project.tests.test_all_sql

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.project.tests.test_all_sql

os.makedirs(tap.signature_db_folder, exist_ok = True)
signature_db_full_path = os.path.join(tap.signature_db_folder,
                                      tap.signature_db_relative_path)


# MinHASH ----------------------------------------------------------
# generate permutations params
hash_params_matrix = hashing.GenerateNumpyArray(num_rows = tap.SIGNATURE_LEN,
                                                num_cols = 2,
                                                seed = 123,
                                                reshape = True,
                                                int_type = tap.INT_TYPE_64)

# SQL -----------------------------------------------------------------

# first make subfolder, with respect to the duplicates file folder
# where to store the signature database

# Actual procedure ------------------------------------------------------

# 1) Add original Data
# Add original data (no clones) to Signature database

start = time.time()

macro.MinHashPopulateSignatureSQL(file_in_full_path = tap.file_name_original_only,
                                signature_db_full_path = signature_db_full_path,
                                id_name = tap.ID_NAME,
                                content_name = tap.CONTENT_NAME,
                                shingle_len = tap.SHINGLE_LEN,
                                shingle_hash_fun = tap.SHINGLE_HASH_FUN,
                                minhash_hash_param_matrix = hash_params_matrix,
                                minhash_hash_fun = tap.MINHASH_HASH_FUN,
                                minhash_int_type = tap.MINHASH_INT_TYPE,
                                num_sql_insertions = tap.NUM_SQL_INSERTIONS,
                                match_string = r'\{(.*)\}')

stop = time.time()

print("Only original data Signatures")
print(f"Time: {stop - start}")

# 2) Add duplicates Data
# Add duplicates data to Signature database

start = time.time()

doc_count_signature = 0

macro.MinHashPopulateSignatureSQL(file_in_full_path = tap.file_name_duplicates_only,
                                signature_db_full_path = signature_db_full_path,
                                id_name = tap.ID_NAME,
                                content_name = tap.CONTENT_NAME,
                                shingle_len = tap.SHINGLE_LEN,
                                shingle_hash_fun = tap.SHINGLE_HASH_FUN,
                                minhash_hash_param_matrix = hash_params_matrix,
                                minhash_hash_fun = tap.MINHASH_HASH_FUN,
                                minhash_int_type = tap.MINHASH_INT_TYPE,
                                num_sql_insertions = tap.NUM_SQL_INSERTIONS,
                                match_string = r'\{(.*)\}')

stop = time.time()

print("Only duplicates data Signatures")
print(f"Time: {stop - start}")


metadata_minhash_full_path = os.path.join(tap.signature_db_folder,
                                      tap.metadata_minhash_relative_path)


# NOTE: in future ADD: type of integer used for both shingling and Hashing
# + type of Hashing functions used, for both

with open(tap.original_collection_metadata_path, "r") as fin:
    metadata_minhash_dict = json.load(fin)
    metadata_minhash_dict["minhash"] = {"shingle_length": tap.SHINGLE_LEN,
                                        "signature_length": tap.SIGNATURE_LEN,
                                        "random_integers" : tap.EL,
                                        "document_count": doc_count_signature,
                                        "time" : stop - start}
    
with open(metadata_minhash_full_path, "w") as fout:
    json.dump(metadata_minhash_dict, fout)


# LSH --------------------------------------------------------------------


# 3) Iterates over all signature database rows
# populate LSH band data structure

# generate hash functions for lsh bands hashing
my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = tap.N_BANDS,
                                                            band_size = tap.SIGNATURE_LEN // tap.N_BANDS,
                                                            modulo = tap.N_BUCKETS,
                                                            seed = 123)

my_break_points = lsh.GenerateBreakPoints(n = tap.SIGNATURE_LEN, n_bands = tap.N_BANDS)

# initialize LSH bands list data instance
LshManyBands = lsh.LSHManyBandsBucketLists(n_bands = tap.N_BANDS, n_buckets = tap.N_BUCKETS)


# open database connection
SigSQL = mh.SignaturesSQLite(database_name = signature_db_full_path)

# define rows iterator
fetched_rows_iterator = SigSQL.fetch_all_rows()

# populate LSH band data structure

start = time.time()

for row in fetched_rows_iterator:
    id_temp = row[0]
    signature_temp = row[1]
    
    LshManyBands.AddToBands(bucket_ids =
                            lsh.ComputeAllHashBands(signature = signature_temp,
                                                    break_points = my_break_points,
                                                    hash_functions_list = my_lsh_hash_fun_list),
                                                    object = id_temp)
stop = time.time()

print("Adding to LSH bands buckets")
print(f"Time: {stop - start}")


start_find_sim = time.time()

temp_all_combinations = macro.FindAllCombinations(lsh_many_bands = LshManyBands,
                                                  sig_sql = SigSQL)

stop_find_sim = time.time()

print("Finding documents in the same bucket LSH bands")
print(f"Time: {stop_find_sim - start_find_sim}")
    
# print(temp_all_combinations)

print(f"length of dictionary is {len(temp_all_combinations)}")

# sort key values
sorted_tuples_list = sorted(temp_all_combinations.items())


# write signature similarity csv
signature_sim_folder_path = "test_data\\arxiv_duplicates\\sig_config1\\lsh1"
signature_sim_relative_path = "arxiv_clones_first_1000_signature_sim.csv"

os.makedirs(signature_sim_folder_path, exist_ok = True)

signature_sim_full_path = os.path.join(signature_sim_folder_path,
                                      signature_sim_relative_path)


with open(signature_sim_full_path, mode= 'w', newline='') as fout:
    writer = csv.writer(fout)
    
    # write header
    writer.writerow(['doc1_id', 'doc2_id', 'signature_similarity'])
    
    for ((first_el, second_el), value) in sorted_tuples_list:
        writer.writerow([first_el, second_el, value])


SigSQL.close_database()
SigSQL.delete_database(ask_confirm = False)



metadata_lsh_relative_path = "metadata_lsh.json"

metadata_lsh_full_path = os.path.join(signature_sim_folder_path ,
                                      metadata_lsh_relative_path)


# NOTE: in future ADD: type of integer used for both shingling and Hashing
# + type of Hashing functions used, for both

with open(metadata_minhash_full_path, "r") as fin:
    metadata_lsh_dict = json.load(fin)
    metadata_lsh_dict["lsh"] = {"bands_number": tap.N_BANDS,
                                        "buckets_number": tap.N_BUCKETS,
                                        "time_populate" : stop - start,
                                        "time_find_sim": stop_find_sim - start_find_sim}
    
with open(metadata_lsh_full_path, "w") as fout:
    json.dump(metadata_lsh_dict, fout)
