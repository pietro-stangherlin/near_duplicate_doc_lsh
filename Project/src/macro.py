from ..src import minhash
from ..src import shingling
from ..src import line_reading as lr

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
                  sig_sql):
    '''
    '''
    temp_all_combinations = {}

    for band_object in lsh_many_bands.bands_list:
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
                            temp_all_combinations[temp_key] = sig_sim

    return temp_all_combinations



            