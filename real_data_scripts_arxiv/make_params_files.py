import json
import numpy as np

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import parameters as pm

# This just creates json files, each with shingle and minhash parameters
# which are saved in the minhash_params folder
# same for lsh parameters

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts_arxiv.make_params_files

# MinHash function -----------------------------------------------------------
def SaveMinhashParamsFiles(shingle_lenghts,
                           signature_lengths,
                           hash_dict,
                           save_folder_minhash):
    for bit_type in hash_dict:
        
        for shingle_len in shingle_lenghts:
            for signa_len in signature_lengths:
                parameters = {
        pm.SHINGLE_LEN_FIELD_NAME: shingle_len,
        pm.SHINGLE_HASH_FUN_FIELD_NAME: hash_dict[bit_type][0], # store hash function name
        pm.SIGNATURE_LEN_FIELD_NAME: signa_len,
        pm.MINHASH_HASH_FUN_FIELD_NAME: hash_dict[bit_type][1], # store hash function name
        pm.MINHASH_BIT_TYPE_FIELD_NAME: bit_type,
        pm.MINHASH_HASH_PARAM_MATRIX_FIELD_NAME: hashing.GenerateNumpyArray(num_rows = signa_len,
                                                         num_cols =  2,
                                                         seed= pm.SEED_MINHASH,
                                                         reshape = True,
                                                         int_type = np.uint64).tolist()  # Convert the matrix to a list
    }

                # define the filename based on the signature length
                # add bit number
                filename = save_folder_minhash + f"minhash_par_shl_{shingle_len}_sil_{signa_len}_bit_{bit_type}.json"

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
        pm.BANDS_NUMBER_FIELD_NAME: band_n,
        pm.BUCKETS_NUMBER_FIELD_NAME: bucket_n}

            # define the filename based on the signature length
            # add bit number
            filename = save_folder_lsh + f"lsh_par_band_{band_n}_bucket_{bucket_n}.json"

            # save parameters to a file
            with open(filename, 'w') as file:
                json.dump(parameters, file, indent = 4)


if __name__ == "__main__":
    SaveMinhashParamsFiles(shingle_lenghts = pm.SHINGLE_LENGTHS,
                           signature_lengths = pm.SIGNATURE_LENGTHS,
                           hash_dict = pm.MINHASH_HASH_DICT,
                           save_folder_minhash = pm.MINHASH_PARAMS_FOLDER)
    
    SaveLSHParamsFiles(bands_numbers = pm.BANDS_NUMBERS,
                       bucket_numbers = pm.BUCKET_NUMBERS,
                       save_folder_lsh = pm.LSH_PARAMS_FOLDER)