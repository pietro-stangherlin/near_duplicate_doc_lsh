# This file containts all the parameters used in all the other scripts
# using the real data

from near_duplicate_doc_lsh.project.src import hashing

# Collection ------------------------------------------------

ID_FIELD_NAME = "id2"
CONTENT_FIELD_NAME = "content"

ROBUST_DUPLICATES_NAME = "robust_duplicates.json"
DUPLICATES_INDEX_NAME = "robust_index.csv"

# METADATA -------------------------------------
METADATA_FILE_NAME = "metadata.json"

MINHASH_METADATA_PARAMS_NAME = "minhash_params"
LSH_METADATA_PARAMS_NAME = "lsh_params"

BIT_TYPE_NAME = "bit_type"
TIME_NAME = "time"

# Constants ------------------------------------

# NOTE: one should add the string "np." as a prefix, like "np.uint32"
# here it's not present in order to be able to save the file as a json
# (python doesn't allow to write object types as json)
# also pickling is avoided to improve readability
INT_TYPE_32 = "uint32"
INT_TYPE_64 = "uint64"

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

MINHASH_BIT_TYPE_FIELD_NAME = "minhash_bit_type"

# Parameters values  -------------------
# list of signature lengths
SHINGLE_LENGTHS = [9, 18] # 9 is the suggested length
SIGNATURE_LENGTHS = [100, 200, 300]

# Idea: 
# with 32 bit shingle -> use 32 bit signature hash
# with 64 bit shingle -> use 64 bit signature hash

# hash functions dict:
MINHASH_HASH_DICT = {INT_TYPE_32: (hashing.MurmUns32Hash.__name__, # shingle
                    hashing.NumbaNaiveHashU32Params.__name__), # minhash
             INT_TYPE_64: (hashing.MurmUns64Hash.__name__, # shingle
                    hashing.NumbaNaiveHashU64Params.__name__)} # minhash

# Paths ------------------
MINHASH_PARAMS_FOLDER = "near_duplicate_doc_lsh\\real_data_scripts\\minhash_params\\"

# folder of signatures
SIGNATURE_DB_ORIGINAL_FOLDER = "data_near_duplicate\\robust\\signatures_db_original\\"
# relative name of the signature sql database file
SIGNATURE_DB_FILE_NAME_RELATIVE = "signature_db"

MINHASH_PARAMETERS_COPY_RELATIVE_NAME = "minhash_params.json"

# folder with subfolder of complete signature_db (original + duplicates)
# + metadata file + index maybe, which is copied
SIGNATURE_DB_DUPLICATES_FOLDER = "data_near_duplicate\\robust\\signatures_db_duplicates\\"

MINHASH_SIGNATURE_DB_DUPLICATES_DONE_FOLDERS_NAMES_FILE = "near_duplicate_doc_lsh\\real_data_scripts\\already_done\\signature_db_duplicates_done_names.txt"

# LSH ----------------------------------------------------------------------------
# name of the bands number length field in the dictionary
BANDS_NUMBER_FIELD_NAME = "bands_numbers"
# name of the buckets number length field in the dictionary
BUCKETS_NUMBER_FIELD_NAME = "bucket_numbers"

# list of signature lengths
BANDS_NUMBERS = [10, 20, 30]
BUCKET_NUMBERS = [10**7, 2 * 10**7]

# Paths -----------------
LSH_PARAMS_FOLDER = "near_duplicate_doc_lsh\\real_data_scripts\\lsh_params\\"

# each line is a name of already done
# lsh result folder
LSH_RESULT_DONE_FOLDERS_NAMES_FILE = "near_duplicate_doc_lsh\\real_data_scripts\\already_done\\lsh_names_result_done.txt"

# final results
LSH_RESULTS_FOLDER = "data_near_duplicate\\robust\\lsh_results\\"
SIGNATURE_SIMILARITY_NAME_CSV = "signature_sim.csv"

SIGNATURE_SIMILARITY_DOC1_HEADER = "doc1"
SIGNATURE_SIMILARITY_DOC2_HEADER = "doc2"
SIGNATURE_SIMILARITY_DOC1_SIGSIM_HEADER = "signature_similarity"
DOC1_DOC2_SHARED_BUCKETS_NUMBER = "shared_buckets_number"

TIME_POPULATE_LSH_NAME = "time_populate_lsh"
TIME_FIND_SAME_BUCKET_NAME = "time_find_same_bucket"


# (Only) Duplicates collections folder path
ONLY_DUPLICATES_COLLECTION_FOLDER_PATH = "data_near_duplicate\\robust\\robust_clones\\"

# Other Paths --------------------------------------------------------------------
ROBUST_ORIGINAL_PATH = "data_near_duplicate\\robust\\robust_id2.json"
