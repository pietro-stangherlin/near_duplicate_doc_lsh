import minhash
import hashing
import shingling
import line_reading as lr

import regex as re
import numpy as np

# this file holds macro function useful to the evaluation

# number of insertions for each transaction
NUM_SQL_INSERTIONS = 100

def ToMatchFromIdAndSignature(my_match: str,
                              id_name: str,
                              content_name: str,
                              shingle_len: int,
                              shingle_hash_fun,
                              minhash_hash_param_matrix,
                              minhash_hash_fun,
                              minhash_int_type):
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

# initialize SignaturesSQLite
SigSQL = minhash.SignaturesSQLite(database_name = signature_db_full_path)

SigSQL.begin_transaction()

# Actual procedure ------------------------------------------------------

# 1) Add original Data
# Add original data (no clones) to Signature database

with open(file_name_original_only, 'r', encoding = "utf-8") as fin:
    insertion_counter = 0
    for line in fin:
        # Use regular expression to find the content inside the brackets
        match = re.search(r'\{(.*)\}', line)
        if match:
            tuple_id_content = lr.ToJsonLineRead(my_match = match,
                                        id_name = ID_NAME,
                                        content_name = CONTENT_NAME)
                        
            shingle_temp = shingling.TextToShinglesUniques(
                text = tuple_id_content[1],
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
            
            SigSQL.insert_id_signature_pair(id_value = tuple_id_content[0],
                                            signature_value = signature_temp)
            insertion_counter += 1
            
SigSQL.end_transaction()
SigSQL.close_database()