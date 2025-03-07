import json
import numpy as np

from near_duplicate_doc_lsh.project.src import hashing

# This just creates json files, each with shingle and minhash parameters
# which are saved in the minhash_params folder
# same for lsh parameters

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files

# Constants ------------------------------------

SEED = 123

SHINGLE_LEN_FIELD_NAME = "shingle_len"
SHINGLE_HASH_FUN_FIELD_NAME = "shingle_hash_fun"
MINHASH_HASH_FUN_FIELD_NAME = "minhash_hash_fun"
MINHASH_HASH_PARAM_MATRIX_FIELD_NAME = "hash_params_matrix"

BANDS_NUMBER_FIELD_NAME = "bands_numbers"
BUCKETS_NUMBER_FIELD_NAME = "bucket_numbers"

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

# Paths ---------------------------------------------
SAVE_FOLDER_MINHASH = "near_duplicate_doc_lsh\\real_data_scripts\\minhash_params\\"
SAVE_FOLDER_LSH = "near_duplicate_doc_lsh\\real_data_scripts\\lsh_params\\"

# MinHash params ---------------------------------------------

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

# LSH  params --------------------------------------------------------

# list of signature lengths
BANDS_NUMBERS = [10, 20, 30] # 9 is the suggested length
BUCKET_NUMBERS = [10**6, 5 * 10**6, 10**7]

# MinHash function -----------------------------------------------------------
def SaveMinhashParamsFiles(shingle_lenghts,
                           signature_lengths,
                           hash_dict,
                           save_folder_minhash):
    for bit in hash_dict:
        for shingle_len in shingle_lenghts:
            for signa_len in signature_lengths:
                parameters = {
        SHINGLE_LEN_FIELD_NAME: shingle_len,
        SHINGLE_HASH_FUN_FIELD_NAME: hash_dict[bit][0], # store hash function name
        MINHASH_HASH_FUN_FIELD_NAME: hash_dict[bit][1], # store hash function name
        MINHASH_HASH_PARAM_MATRIX_FIELD_NAME: hashing.GenerateNumpyArray(num_rows = signa_len,
                                                         num_cols =  2,
                                                         seed= SEED,
                                                         reshape = True,
                                                         int_type = INT_TYPE_64).tolist()  # Convert the matrix to a list
    }

                # define the filename based on the signature length
                # add bit number
                filename = save_folder_minhash + f"minhash_par_shl_{shingle_len}_sil_{signa_len}_{bit}.json"

                # save parameters to a file
                with open(filename, 'w') as file:
                    json.dump(parameters, file, indent = 4)


# LSH function -----------------------------------------------------
def SaveLSHParamsFiles(bands_numbers,
                       bucket_numbers,
                       save_folder_lsh):

    for band_n in bands_numbers:
        for bucket_n in bucket_numbers:
            parameters = {
        BANDS_NUMBER_FIELD_NAME: band_n,
        BUCKETS_NUMBER_FIELD_NAME: bucket_n}

            # define the filename based on the signature length
            # add bit number
            filename = save_folder_lsh + f"lsh_par_band_{band_n}_bucket_{bucket_n}.json"

            # save parameters to a file
            with open(filename, 'w') as file:
                json.dump(parameters, file, indent = 4)


if __name__ == "__main__":
    SaveMinhashParamsFiles(shingle_lenghts = SHINGLE_LENGTHS,
                           signature_lengths = SIGNATURE_LENGTHS,
                           hash_dict = MINHASH_HASH_DICT,
                           save_folder_minhash = SAVE_FOLDER_MINHASH)
    
    SaveLSHParamsFiles(bands_numbers = BANDS_NUMBERS,
                       bucket_numbers = BUCKET_NUMBERS,
                       save_folder_lsh = SAVE_FOLDER_LSH)