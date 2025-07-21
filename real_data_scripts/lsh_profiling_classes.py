from near_duplicate_doc_lsh.project.src import lsh
from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import utils as ut
from near_duplicate_doc_lsh.real_data_scripts.robust.params import profiling_params as pp

import argparse
from memory_profiler import profile


import os
import json
import time

# memory profiling lsh operations
# different LSH implementations comparaison
# assuming a signature database is already present

fp=open(pp.OUT_COMPLETE_PATH,'w+')

@profile(stream = fp)
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



# > python -m near_duplicate_doc_lsh.real_data_scripts.lsh_profiling_classes

if __name__ == "__main__":


    collection_dict = mh.SignatureSQLIterator(pp.DB_PATH)

    print("SQL parameters extraction ended")

    N_BUCKETS = collection_dict["n_rows"] * pp.TIMES_BUCKET

    # list implementation
    res1 = LSHAllGetPairs(lsh_class = lsh.LSHManyBandsBucketLists,
                          signatures_iterator = collection_dict["iterator"],
                   signature_len = collection_dict["signature_len"],
                   n_bands = pp.N_BANDS,
                   n_buckets = N_BUCKETS)
    
    print(len(res1))

    # reset iterator
    collection_dict = mh.SignatureSQLIterator(pp.DB_PATH)
    del res1
    
    # btree implementation
    res2 = LSHAllGetPairs(lsh_class = lsh.LSHManyBandsBucketsBTree,
                               signatures_iterator = collection_dict["iterator"],
                   signature_len = collection_dict["signature_len"],
                   n_bands = pp.N_BANDS,
                   n_buckets = N_BUCKETS)
    
    print(len(res2))
    
