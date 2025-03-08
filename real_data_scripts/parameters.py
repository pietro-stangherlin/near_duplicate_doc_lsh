# This file containts all the parameters used in all the other scripts
# using the real data

import numpy as np

from near_duplicate_doc_lsh.project.src import hashing

# Collection ------------------------------------------------
ID_FIELD_NAME = "id2"
CONTENT_FIELD_NAME = "content"

# Constants ------------------------------------

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

# seeds used for making the hash functions parameters matrix
SEED_MINHASH = 123
SEED_LSH = 123

# Shingle -------------------------------------------------------------
# name of the shingle length field in the dictionary
SHINGLE_LEN_FIELD_NAME = "shingle_len"
SHINGLE_HASH_FUN_FIELD_NAME = "shingle_hash_fun"

# Minhash ----------------------------------------------------------------------

NUM_SQL_INSERTIONS = 1000

# Parameters name ---------
# name of the signature length field in the dictionary
SIGNATURE_LEN_FIELD_NAME = "signature_len"
MINHASH_HASH_FUN_FIELD_NAME = "minhash_hash_fun"
MINHASH_HASH_PARAM_MATRIX_FIELD_NAME = "hash_params_matrix"

# Parameters values  -------------------
# list of signature lengths
SHINGLE_LENGTHS = [9, 18] # 9 is the suggested length
SIGNATURE_LENGTHS = [100, 200, 300]


# Idea: 
# with 32 bit shingle -> use 32 bit signature hash
# with 64 bit shingle -> use 64 bit signature hash

# hash functions dict:
MINHASH_HASH_DICT = {"32": (hashing.MurmUns32Hash.__name__, # shingle
                    hashing.NumbaNaiveHashU32Params.__name__), # minhash
             "64": (hashing.MurmUns64Hash.__name__, # shingle
                    hashing.NumbaNaiveHashU64Params.__name__)} # minhash

# Paths ------------------
MINHASH_PARAMS_FOLDER = "near_duplicate_doc_lsh\\real_data_scripts\\minhash_params\\"

# folder of signatures
SIGNATURE_DB_FOLDER = "data_near_duplicate\\signatures_db_original\\"
# relative name of the signature sql database file
SIGNATURE_DB_FILE_NAME_RELATIVE = "signature_db"

# LSH ----------------------------------------------------------------------------
# name of the bands number length field in the dictionary
BANDS_NUMBER_FIELD_NAME = "bands_numbers"
# name of the buckets number length field in the dictionary
BUCKETS_NUMBER_FIELD_NAME = "bucket_numbers"

# list of signature lengths
BANDS_NUMBERS = [10, 20, 30] # 9 is the suggested length
BUCKET_NUMBERS = [10**6, 5 * 10**6, 10**7]

# Paths -----------------
SAVE_FOLDER_LSH = "near_duplicate_doc_lsh\\real_data_scripts\\lsh_params\\"

# Other Paths --------------------------------------------------------------------
ROBUST_ORIGINAL_PATH = "data_near_duplicate\\robust\\robust_id2.json"

