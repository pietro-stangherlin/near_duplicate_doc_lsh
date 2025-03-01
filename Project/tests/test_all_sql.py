# test all storing the MinHash Signatures in a SQL single table Database
# LSH band buckets still stored in list of lists data structure
# then all records need to be read again in order to populate the LSH data structure

from ..src import shingling
from ..src import minhash
from ..src import hashing
from ..src import lsh

import os
import csv
import numpy as np
import json
import re
import time

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# also before running convert the file to utf-8 and remove BOM 
# (from notepad++ encoding, or another way)

# If data is in test_data: (use this in testing)
# >>> python -m project.tests.test_all_sql

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.project.tests.test_all_sql

# constants
SHINGLE_LEN = 9 # shingle len
SIGNATURE_LEN = 50 # signature len -> number of hash functions
EL = 2 # number of random integers generated

N_BANDS = 5 # number of bands
N_BUCKETS = 10**6 # number of buckets in each band

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

file_name_original_only = "test_data\\arxiv_first_1000_id2.json"
file_name_duplicates_only = "test_data\\arxiv_duplicates\\arxiv_clones_1000_only_duplicates.json"

# signature db folder and path
signature_db_folder = "test_data\\arxiv_duplicates\\sig_config1"
signature_db_relative_path = "signature_db"

os.makedirs(signature_db_folder, exist_ok = True)
signature_db_full_path = os.path.join(signature_db_folder,
                                      signature_db_relative_path)


# MinHASH ----------------------------------------------------------
# generate permutations params
hash_params_matrix = hashing.GenerateNumpyArray(num_rows = 100,
                                                num_cols = 2,
                                                seed = 123,
                                                reshape = True,
                                                int_type = INT_TYPE_64)

# write shingle and MinHash metadata
original_collection_metadata_path = "test_data\\metadata_arxiv_1000_only_duplicates.json"
# read it
# add shingle and minhash parameters
# save it in subfolder


# SQL -----------------------------------------------------------------

# first make subfolder, with respect to the duplicates file folder
# where to store the signature database

# initialize SignaturesSQLite
SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

# number of insertions for each transaction
NUM_SQL_INSERTIONS = 100
insertion_counter = 0

SigSQL.begin_transaction()

# Actual procedure ------------------------------------------------------

# 1) Add original Data
# Add original data (no clones) to Signature database

start = time.time()

with open(file_name_original_only, 'r', encoding = "utf-8") as fin:
    for line in fin:
        # Use regular expression to find the content inside the brackets
        match = re.search(r'\{(.*)\}', line)
        if match:
            content = match.group(0)  # group(0) returns the entire match
            # due to json problems
            json_content = json.loads(content)  # Convert the content to JSON
            id_temp = int(json_content["id2"])
            text_temp = json_content["content"]
            
            
            shingle_temp = shingling.TextToShinglesUniques(
                text = text_temp,
                shingle_len = SIGNATURE_LEN,
                hash_fun = hashing.MurmUns32Hash)
            
            signature_temp = minhash.NumbaSignatureByRowParallel(
                shingles_array = np.array(list(shingle_temp), dtype= INT_TYPE_32),
                hash_params_matrix = hash_params_matrix,
                hash_fun = hashing.NumbaNaiveHashU32Params,
                int_type = INT_TYPE_32)

            # add key (doc id) value (signature) pair to the SignatureSQL
            if insertion_counter % NUM_SQL_INSERTIONS == 0:
                SigSQL.end_transaction()
                SigSQL.begin_transaction()
            
            SigSQL.insert_id_signature_pair(id_value = id_temp, signature_value = signature_temp)
            insertion_counter += 1
            
SigSQL.end_transaction()

stop = time.time()

print("Only original data Signatures")
print(f"Time: {stop - start}")


# close database
SigSQL.close_database()

# open database
SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)


# 2) Add duplicates Data
# Add dupicates data to Signature database

start = time.time()

with open(file_name_duplicates_only, 'r', encoding = "utf-8") as fin:
    for line in fin:
        # Use regular expression to find the content inside the brackets
        match = re.search(r'\{(.*)\}', line)
        if match:
            content = match.group(0)  # group(0) returns the entire match
            # due to json problems
            json_content = json.loads(content)  # Convert the content to JSON
            id_temp = int(json_content["id2"])
            text_temp = json_content["content"]
            
            
            shingle_temp = shingling.TextToShinglesUniques(
                text = text_temp,
                shingle_len = SIGNATURE_LEN,
                hash_fun = hashing.MurmUns32Hash)
            
            signature_temp = minhash.NumbaSignatureByRowParallel(
                shingles_array = np.array(list(shingle_temp), dtype= INT_TYPE_32),
                hash_params_matrix = hash_params_matrix,
                hash_fun = hashing.NumbaNaiveHashU32Params,
                int_type = INT_TYPE_32)

            # add key (doc id) value (signature) pair to the SignatureSQL
            if insertion_counter % NUM_SQL_INSERTIONS == 0:
                SigSQL.end_transaction()
                SigSQL.begin_transaction()
            
            SigSQL.insert_id_signature_pair(id_value = id_temp, signature_value = signature_temp)
            insertion_counter += 1
            
SigSQL.end_transaction()

stop = time.time()

print("Only duplicates data Signatures")
print(f"Time: {stop - start}")



# SQL ------------------------------------
# compare the similarity of two documents
doc1_id = 2
doc2_id = 1001

value1 = SigSQL.get_signature_by_id(doc1_id)
value2 = SigSQL.get_signature_by_id(doc2_id)

sim_doc1_doc2 = minhash.SignatureSimilarity(value1, value2)
print(f"The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}")

SigSQL.close_database()

# LSH --------------------------------------------------------------------


# 3) Iterates over all signature database rows
# populate LSH band data structure

# generate hash functions for lsh bands hashing
my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = N_BANDS,
                                                            band_size = SIGNATURE_LEN // N_BANDS,
                                                            modulo = N_BUCKETS,
                                                            seed = 123)

my_break_points = lsh.GenerateBreakPoints(n = SIGNATURE_LEN, n_bands = N_BANDS)

# initialize LSH bands list data instance
LshManyBands = lsh.LSHManyBandsBucketLists(n_bands = N_BANDS, n_buckets = N_BUCKETS)


# open database connection
SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

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


start = time.time()

temp_all_combinations = dict()

for band_object in LshManyBands.bands_list:
    for k in band_object.more_than_one_index:
        temp_bucket = band_object.band[k]
        
        for i in range(len(temp_bucket) - 1):
            for j in range(i + 1, len(temp_bucket)):
                # already in the dictionary
                
                # store just one tuple for each pair:
                # i.e. (a,b) = (b,a)
                # we ensure this (assuming the doc_id allows an ordering)
                
                # it's ugly, just for readbility
                
                temp_key = (temp_bucket[i], temp_bucket[j])
                
                if (temp_bucket[i] > temp_bucket[j]):
                    temp_key = (temp_bucket[j], temp_bucket[i])
                
                
                condition = temp_key in temp_all_combinations
                if not condition:
                    value1 = SigSQL.get_signature_by_id(temp_key[0])
                    # debug
                    # print(value1)
                    value2 = SigSQL.get_signature_by_id(temp_key[1])
                    sig_sim = minhash.SignatureSimilarity(value1, value2)
                    
                    if sig_sim != 0:
                        # do not include if signature similarity is zero
                        temp_all_combinations[temp_key] = sig_sim

print("Finding documents in the same bucket LSH bands")
print(f"Time: {stop - start}")
    
# print(temp_all_combinations)

print(f"length of dictionary is {len(temp_all_combinations)}")

# sort key values
sorted_tuples_list = sorted(temp_all_combinations.items())


# write signature similarity csv

# signature db folder and path
signature_db_folder = "test_data\\arxiv_duplicates\\sig_config1"
signature_db_relative_path = "signature_db"


signature_db_full_path = os.path.join(signature_db_folder,
                                      signature_db_relative_path)

signature_sim_folder_path = "test_data\\arxiv_duplicates\\sig_config1\\lsh1"
signature_sim_relative_path = "arxiv_clones_first_1000_signature_sim.csv"

os.makedirs(signature_sim_folder_path, exist_ok = True)

signature_sim_full_path = os.path.join(signature_sim_folder_path,
                                      signature_sim_relative_path)


with open(signature_sim_full_path, mode='w', newline='') as fout:
    writer = csv.writer(fout)
    
    # write header
    writer.writerow(['doc1_id', 'doc2_id', 'signature_similarity'])
    
    for ((first_el, second_el), value) in sorted_tuples_list:
        writer.writerow([first_el, second_el, value])


SigSQL.close_database()
SigSQL.delete_database(ask_confirm = False)
