from ..src import minhash
from ..src import shingling
from ..src import line_reading as lr

from itertools import combinations
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import pickle
import regex as re
import numpy as np
import time

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
                                batch_size: int,
                                match_string: str = r'\{(.*)\}'):
    '''
    '''
    SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

    SigSQL.begin_transaction()
    
    start = time.time()
    
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
                if insertion_counter % batch_size == 0:
                    SigSQL.end_transaction()
                    SigSQL.begin_transaction()
                    stop = time.time()
                    print(f"[INFO]: batch_size {batch_size} in time {round(stop - start)}")
                    start = time.time()
            
                SigSQL.insert_id_signature_pair(id_value = tuple_id_signature[0],
                                            signature_value = tuple_id_signature[1])
                insertion_counter += 1
                    
    SigSQL.end_transaction()
    SigSQL.close_database()








