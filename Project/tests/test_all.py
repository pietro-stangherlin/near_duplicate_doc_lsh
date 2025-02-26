from ..src import shingling
from ..src import minhash
from ..src import hashing
from ..src import lsh

import sys
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
# >>> python -m project.tests.test_all

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.project.tests.test_all


# constants
SHINGLE_LEN = 9 # shingle len
SIGNATURE_LEN = 50 # signature len -> number of hash functions
EL = 2 # number of random integers generated

N_BANDS = 5 # number of bands
N_BUCKETS = 10**6 # number of buckets in each band

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

file_name = "test_data\\arxiv_clones_first_1000.json"

# MinHASH ----------------------------------------------------------
# generate permutations params
hash_params_matrix = hashing.GenerateNumpyArray(num_rows = 100,
                                                num_cols = 2,
                                                seed = 123,
                                                reshape = True,
                                                int_type = INT_TYPE_64)

# initialize Signature Btree instance
SigBTree = minhash.SignaturesBTree()

# SQL -----------------------------------------------------------------

# initialize SignaturesSQLite
# SigSQL = minhash.SignaturesSQLite()

# number of insertions for each transaction
# NUM_SQL_INSERTIONS = 100
# insertion_counter = 0

# SigSQL.begin_transaction()

# LSH --------------------------------------------------------------------

# generate hash functions for lsh bands hashing
my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = N_BANDS,
                                                            band_size = SIGNATURE_LEN // N_BANDS,
                                                            modulo = N_BUCKETS,
                                                            seed = 123)

my_break_points = lsh.GenerateBreakPoints(n = SIGNATURE_LEN, n_bands = N_BANDS)

# initialize LSH bands list data instance
LshManyBands = lsh.LSHManyBandsBucketLists(n_bands = N_BANDS, n_buckets = N_BUCKETS)


# Actual procedure ------------------------------------------------------

start = time.time()

with open(file_name, 'r', encoding = "utf-8") as fin:
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

            # add key (doc id) value (signature) pair to the Signature Btree
            SigBTree.insert(id_temp, signature_temp)

            # add key (doc id) value (signature) pair to the SignatureSQL
            # if insertion_counter % NUM_SQL_INSERTIONS == 0:
                # SigSQL.end_transaction()
                # SigSQL.begin_transaction()
            
            # SigSQL.insert_key_value(key = id_temp, value = signature_temp)
            # insertion_counter += 1
            
            LshManyBands.AddToBands(bucket_ids = lsh.ComputeAllHashBands(signature = signature_temp,
                                                                         break_points = my_break_points,
                                                                         hash_functions_list = my_lsh_hash_fun_list),
                                    object = id_temp)

# SigSQL.end_transaction()

stop = time.time()

print(f"Time: {stop - start}")

# LSH --------------------------------------
print("LshManyBands first band")
print(LshManyBands.bands_list[0])

# consider only the first band: for each bucket with more than two elements compute the similarity 
# between the signatures of all elements in the bucket

similar_set_band_0 = set()
indexes_more_than_one_band_0 = LshManyBands.bands_list[0].more_than_one_index


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
                    sig_sim = SigBTree.compute_similarity(temp_key[0], temp_key[1])
                    
                    if sig_sim != 0:
                        # do not include if signature similarity is zero
                        temp_all_combinations[temp_key] = sig_sim
    
# print(temp_all_combinations)

print(f"length of dictionary is {len(temp_all_combinations)}")

# sort key values
sorted_tuples_list = sorted(temp_all_combinations.items())

# write signature similarity csv
with open('test_data\\arxiv_clones_first_1000_signature_sim.csv', mode='w', newline='') as fout:
    writer = csv.writer(fout)
    
    # write header
    writer.writerow(['doc1_id', 'doc2_id', 'signature_similarity'])
    
    for ((first_el, second_el), value) in sorted_tuples_list:
        writer.writerow([first_el, second_el, value])




# BTree ------------------------------------
# compare the similarity of two documents
# doc1_id = 1
# doc2_id = 1001
# sim_doc1_doc2 =  SigBTree.compute_similarity(doc1_id, doc2_id)
# print(f"The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}")

# SQL -------------------------------------
# value1 = SigSQL.get_value_by_key(doc1_id)
# value2 = SigSQL.get_value_by_key(doc2_id)

# sim_doc1_doc2 = minhash.SignatureSimilarity(value1, value2)
# print(f"The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}")

# SigSQL.close_database()
# SigSQL.delete_database(ask_confirm = False)