from near_duplicate_doc_lsh.project.src import lsh
from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import utils as ut

import importlib
import argparse
from memory_profiler import profile


import os
import json
import time

# memory profiling lsh operations
# assuming a signature database is already present


def SQLIterator(signature_db_path) -> dict:
    '''Given a SQL signature database with two columns:
    first column is document id
    second column is a pickled numpy array holding the signature

    Return: dictionary with rows iterator, length if the signatures and the number of rows
    '''
    # open database connection
    SigSQL = mh.SignaturesSQLite(database_name = signature_db_path)
    signature_len = SigSQL.GetSignatureLen()
    n_rows = SigSQL.count_rows()

    # define rows iterator
    fetched_rows_iterator = SigSQL.fetch_all_rows()

    return {"iterator": fetched_rows_iterator,
            "signature_len": signature_len,
            "n_rows": n_rows}


@profile
def LSHAllGetPairs(lsh_class,
                    signatures_iterator,
                    signature_len,
                    n_bands: int,
                    n_buckets: int,
                    hash_seed = 123):
    '''
    Args:
        - lsh_class (Class): lsh class used (example: list or btree)
        - signatue_iterator (Iter): iterator from which each row is read
        - signature_len (int): minhash parameter
        - n_bands (int): lsh parameter
        - n_buckets (int): lsh parameter
        - has_seed (int): lsh hash function parameter

    Return:
        - (dict) with documents id tuple pair as key and number of shared buckets as value
    '''

    # make lsh class instance
    lsh_instance = lsh_class(n_bands = n_bands,
                             n_buckets = n_buckets,
                             signature_len = signature_len,
                             hash_function_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = n_bands,
                                                                                       band_size = signature_len // n_bands,
                                                                                       modulo = n_buckets,
                                                                                       seed = hash_seed))
    # populate lsh
    lsh_instance.AddIter(iterator = signatures_iterator)

    print("LSH: added all documents")

    # find all doc ids pair sharing at least one bucket
    return lsh_instance.FindAllPairs()



# > python -m near_duplicate_doc_lsh.real_data_scripts.lsh_profiling --signature_db data_near_duplicate\robust\signatures_db_duplicates\sgn_shl_9_sigl_100_bit_uint32_mid_noise_per1\signature_db

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--signature_db",
    type=str,
    required=True)

    args = parser.parse_args()

    collection_dict = SQLIterator(args.signature_db)

    print("SQL parameters extraction ended")

    N_BANDS = 10
    TIMES_BUCKET = 10
    N_BUCKETS = collection_dict["n_rows"] * TIMES_BUCKET

    # WARNING: at the moment is only possible to test one function at a time

    # list implementation
    res1 = LSHAllGetPairs(lsh_class = lsh.LSHManyBandsBucketLists,
                          signatures_iterator = collection_dict["iterator"],
                   signature_len = collection_dict["signature_len"],
                   n_bands = N_BANDS,
                   n_buckets = N_BUCKETS)
    
    print(len(res1))

    # reset iterator
    collection_dict = SQLIterator(args.signature_db)
    del res1
    
    # btree implementation
    res2 = LSHAllGetPairs(lsh_class = lsh.LSHManyBandsBucketLists,
                               signatures_iterator = collection_dict["iterator"],
                   signature_len = collection_dict["signature_len"],
                   n_bands = N_BANDS,
                   n_buckets = N_BUCKETS)
    
    print(len(res2))

    
