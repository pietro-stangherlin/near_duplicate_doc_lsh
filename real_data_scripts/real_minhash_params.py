# NOTE: this has to changed in a way to support iterative calls

# parameters used in test all
import numpy as np
from near_duplicate_doc_lsh.project.src import hashing

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

# Doc ----------------------------------------------------------
ID_NAME = "id2"
CONTENT_NAME = "content"

# MinHash -------------------------------------------------------
SHINGLE_LEN = 9 # shingle len
SHINGLE_HASH_FUN = hashing.MurmUns32Hash

SIGNATURE_LEN = 256 # signature len -> number of hash functions
MINHASH_HASH_FUN = hashing.NumbaNaiveHashU32Params
MINHASH_INT_TYPE = INT_TYPE_32

EL = 2 # number of random integers generated

NUM_SQL_INSERTIONS = 1000


# NOTE: maybe the subfolder names' creation should be automated
# (not the file names as they need to be accessed in order to make the analysis)

robust_path = "data_near_duplicate\\robust\\"
robust_clones_path = robust_path + "\\robust_clones\\"
robust_clone_no_noise = robust_clones_path + "\\no_noise"

file_in = robust_path + "robust_id2.json"

file_name_duplicates_only = robust_clones_path + "robust_duplicates.json"

# signature db folder and path -------
signature_db_folder = robust_clones_path + "signature1\\"
signature_db_relative_path = "signature_db"

# no_noise and no_noise_100k
no_noise_100k_path = robust_clone_no_noise + "no_noise_100k\\"
no_noise_100k_signature_folder_path = no_noise_100k_path + "signature1\\"
no_noise_100k_signature_file_path = no_noise_100k_signature_folder_path + signature_db_relative_path

# shingle and MinHash metadata -------
original_collection_metadata_path = "test_data\\arxiv_duplicates\\metadata_arxiv_1000_only_duplicates.json"
metadata_minhash_relative_path = "metadata_minhash.json"