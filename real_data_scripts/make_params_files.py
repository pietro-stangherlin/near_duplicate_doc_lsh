import json
import numpy as np

# This just creates json files, each with shingle and minhash parameters
# which are saved in the minhash_params folder
# same for lsh parameters

from near_duplicate_doc_lsh.project.src import hashing

# instructions:
# execute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files

save_folder_minhash = "near_duplicate_doc_lsh\\real_data_scripts\\minhash_params\\"

SEED = 123

INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

# list of signature lengths
shingle_lenghts = [9, 18] # 9 is the suggested length
signature_lengths = [100, 200, 300]

# Idea: 
# with 32 bit shingle -> use 32 bit signature hash
# with 64 bit shingle -> use 64 bit signature hash

# hash functions dict:
hash_dict = {"32": (hashing.MurmUns32Hash.__name__,
                    hashing.NumbaNaiveHashU32Params.__name__),
             "64": (hashing.MurmUns64Hash.__name__,
                    hashing.NumbaNaiveHashU64Params.__name__)}


for bit in hash_dict:
    for shingle_len in shingle_lenghts:
        for signa_len in signature_lengths:
            parameters = {
        "shingle_len": shingle_len,
        "shingle_hash_fun": hash_dict[bit][0], # store hash function name
        "minhash_hash_fun": hash_dict[bit][1], # store hash function name
        "hash_params_matrix": hashing.GenerateNumpyArray(num_rows = signa_len,
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

# MAKE LSH parameters FILES

# list of signature lengths
bands_numbers = [10, 20, 30] # 9 is the suggested length
bucket_numbers = [10**6, 5 * 10**6, 10**7]

save_folder_lsh = "near_duplicate_doc_lsh\\real_data_scripts\\lsh_params\\"

for band_n in bands_numbers:
    for bucket_n in bucket_numbers:
        parameters = {
        "bands_numbers": band_n,
        "bucket_numbers": bucket_n}

        # define the filename based on the signature length
        # add bit number
        filename = save_folder_lsh + f"lsh_par_band_{band_n}_bucket_{bucket_n}.json"

        # save parameters to a file
        with open(filename, 'w') as file:
            json.dump(parameters, file, indent = 4)