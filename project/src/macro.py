from ..src import minhash
from ..src import shingling
from ..src import line_reading as lr

from itertools import combinations
from collections import defaultdict

import regex as re
import numpy as np

# this file holds macro function useful to the evaluation

def ToMatchFromIdAndSignature(my_match: str,
                              id_name: str,
                              content_name: str,
                              shingle_len: int,
                              shingle_hash_fun,
                              minhash_hash_param_matrix,
                              minhash_hash_fun,
                              minhash_int_type) -> tuple:
    '''Given a 'match' string and minHashing parameters return a pair(id, signature)
    Args:
        - my_match
        - id_name
        - content_name
        - shingle_len
        - shingle_hash_fun
        - minhash_hash_param_matrix
        - minhash_hash_fun
        - minhash_int_type
    Return:
        - tuple (tuple): (id, signature)
    '''
    tuple_id_content = lr.ToJsonLineRead(my_match = my_match,
                                        id_name = id_name,
                                        content_name = content_name)
                        
    shingle_temp = shingling.TextToShinglesUniques(
                text = tuple_id_content[1],
                shingle_len = shingle_len,
                hash_fun = shingle_hash_fun)
            
    signature_temp = minhash.NumbaSignatureByRowParallel(
                shingles_array = np.array(list(shingle_temp),
                                          dtype= minhash_int_type),
                hash_params_matrix = minhash_hash_param_matrix,
                hash_fun = minhash_hash_fun,
                int_type = minhash_int_type)
    
    return (tuple_id_content[0], signature_temp)


def MinHashPopulateSignatureSQL(file_in_full_path: str,
                                signature_db_full_path: str,
                                id_name: str,
                                content_name: str,
                                shingle_len: int,
                                shingle_hash_fun,
                                minhash_hash_param_matrix,
                                minhash_hash_fun,
                                minhash_int_type,
                                num_sql_insertions: int,
                                match_string: str = r'\{(.*)\}'):
    '''
    '''
    SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

    SigSQL.begin_transaction()
    
    with open(file_in_full_path, 'r', encoding = "utf-8") as fin:
        insertion_counter = 0
        for line in fin:
            # Use regular expression to find the content inside the brackets
            match = re.search(match_string, line)
            if match:
                tuple_id_signature = ToMatchFromIdAndSignature(my_match = match,
                                                           id_name = id_name,
                                                           content_name = content_name,
                                                           shingle_len = shingle_len,
                                                           shingle_hash_fun = shingle_hash_fun,
                                                           minhash_hash_param_matrix = minhash_hash_param_matrix,
                                                           minhash_hash_fun = minhash_hash_fun,
                                                           minhash_int_type = minhash_int_type)

                # add key (doc id) value (signature) pair to the SignatureSQL
                if insertion_counter % num_sql_insertions == 0:
                    SigSQL.end_transaction()
                    SigSQL.begin_transaction()
            
                SigSQL.insert_id_signature_pair(id_value = tuple_id_signature[0],
                                            signature_value = tuple_id_signature[1])
                insertion_counter += 1
                    
    SigSQL.end_transaction()
    SigSQL.close_database()


def FindAllCombinations(lsh_many_bands,
                        sig_sql) -> dict:
    '''
    Return a dictionary with
        - key (tuple) = (doc_id1, doc_id2) and doc_id1 < doc_id2 (assuming an ordering is possible)
        - value (list) = [signature_similarity, number_of_shared_buckets]
    '''
    temp_all_combinations = {}

    for band_object in lsh_many_bands.bands_list:
        # debug 
        print(f"more_than_one_index len is {len(band_object.more_than_one_index)}")

        for k in band_object.more_than_one_index:
            temp_bucket = band_object.band[k]


            for i in range(len(temp_bucket) - 1):
                for j in range(i + 1, len(temp_bucket)):
                    # store just one tuple for each pair:
                    # i.e. (a,b) = (b,a)
                    # we ensure this (assuming the doc_id allows an ordering)
                    
                    temp_key = (temp_bucket[i], temp_bucket[j])
                    
                    if temp_bucket[i] > temp_bucket[j]:
                        temp_key = (temp_bucket[j], temp_bucket[i])
                    
                    if temp_key not in temp_all_combinations:
                        value1 = sig_sql.get_signature_by_id(temp_key[0])
                        value2 = sig_sql.get_signature_by_id(temp_key[1])
                        sig_sim = minhash.SignatureSimilarity(value1, value2)
                        
                        if sig_sim != 0:
                            # do not include if signature similarity is zero
                            temp_all_combinations[temp_key] = [sig_sim, 1]
                    else:
                        # pair already present: increment the shared bucket counter by 1
                        temp_all_combinations[temp_key][1] += 1


    return temp_all_combinations

import pickle

def fetch_rows_by_doc_ids(cursor, table_name, doc_ids_batch,
                          unpickle_col=True,
                          doc_id_col_name = "id_doc"):
    """
    Fetch rows from the database for the specified document IDs.
    Args:
        - cursor: SQL cursor object
        - table_name: Name of the database table
        - doc_ids_batch: A batch of document IDs
        - unpickle_col (bool): If True, unpickle the value in column2
        - doc_id_col_name (string): name of document id column in the database
    Returns:
        - List of rows corresponding to the specified document IDs, with unpickled values if needed.
    """
    placeholders = ','.join(['?'] * len(doc_ids_batch))  # Create placeholders for the query
    query = f"SELECT * FROM {table_name} WHERE {doc_id_col_name} IN ({placeholders})"
    cursor.execute(query, doc_ids_batch)
    rows = cursor.fetchall()

    # Unpickle the values in column2 if requested
    if unpickle_col:
        rows = [(row[0], pickle.loads(row[1])) for row in rows]

    return rows



def FindAllCombinationsPreload(lsh_many_bands, sig_sql, batch_size=10000) -> dict:
    """
    Optimized function with print statements to track progress.
    """
    temp_all_combinations = defaultdict(lambda: [0, 0])  # Default value: [0 (similarity), 0 (shared buckets)]
    visited_doc_ids = set()

    print("[INFO] Starting to process LSH bands...")

    # Step 1: Populate visited_doc_ids
    for band_index, band_object in enumerate(lsh_many_bands.bands_list):
        print(f"[DEBUG] Processing band {band_index + 1}/{len(lsh_many_bands.bands_list)}...")
        for k in band_object.more_than_one_index:
            temp_bucket = band_object.band[k]

            # Generate unique pairs using combinations
            for doc_id1, doc_id2 in combinations(temp_bucket, 2):
                visited_doc_ids.update([doc_id1, doc_id2])  # Add to the visited set
                temp_key = (doc_id1, doc_id2) if doc_id1 < doc_id2 else (doc_id2, doc_id1)
                temp_all_combinations[temp_key][1] += 1  # Increment shared bucket count

    print(f"[INFO] Finished processing LSH bands. Found {len(visited_doc_ids)} unique document IDs.")

    # Step 2: Fetch only the visited document IDs in batches
    signature_cache = {}
    visited_doc_ids = list(visited_doc_ids)  # Convert to list for indexing
    print("[INFO] Starting to preload document signatures...")
    for i in range(0, len(visited_doc_ids), batch_size):
        batch = visited_doc_ids[i:i + batch_size]
        print(f"[DEBUG] Fetching batch {i // batch_size + 1} containing {len(batch)} document IDs...")
        rows = fetch_rows_by_doc_ids(sig_sql.cursor, sig_sql.table_name, batch)
        for row in rows:
            signature_cache[row[0]] = row[1]  # Assuming row[0] is doc_id and row[1] is the signature
    print(f"[INFO] Finished preloading document signatures. Cached {len(signature_cache)} signatures.")

    # debug
    print(f"One set element")

    # Step 3: Calculate signature similarities for unique pairs
    print("[INFO] Starting to calculate signature similarities...")
    for progress, temp_key in enumerate(temp_all_combinations, 1):
        if progress % 100000 == 0:  # Print every 1000 iterations to avoid excessive output
            print(f"[DEBUG] Processing similarity for pair {progress}/{len(temp_all_combinations)}...")
        doc_id1, doc_id2 = temp_key
        value1 = signature_cache[doc_id1]
        value2 = signature_cache[doc_id2]
        sig_sim = minhash.SignatureSimilarity(value1, value2)  # Assuming minhash.SignatureSimilarity exists

        if sig_sim != 0:
            temp_all_combinations[temp_key][0] = sig_sim  # Store similarity

    print(f"[INFO] Finished calculating similarities for {len(temp_all_combinations)} pairs.")

    return dict(temp_all_combinations)





            