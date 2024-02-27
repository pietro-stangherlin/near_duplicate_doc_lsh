from ..src import shingling
from ..src import minhash
from ..src import hashing
from ..src import lsh
import numpy as np
import json
import sys
import re

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# >>> python -m near_duplicate_doc_lsh.Project.tests.test_all


# constants
W = 9 # shingle len
K = 100 # signature len -> number of hash functions
INT_TYPE_32 = np.int32


# generate permutations params
hash_aux_params_list = hashing.GenerateTwoUns64(K, 123)

file_name = "data_near_duplicate\\robust_clones_first_100.json"

with open(file_name, 'r', encoding = "utf-8") as file:
    for line in file:
        # Use regular expression to find the content inside the brackets
        match = re.search(r'\{(.*)\}', line)
        if match:
            content = match.group(0)  # group(0) returns the entire match
            # due to json problems
            json_content = json.loads(content)  # Convert the content to JSON
            id_temp = json_content["id2"]
            text_temp = json_content["content"]
            shingle_temp = shingling.TextToShinglesUniques(text_temp,
                                                         W,
                                                         hashing.MurmUns32Hash)
            signature_temp = minhash.GenerateSignatureV2(shingles = shingle_temp,
                                                       hash_function = hashing.HashMultShift32,
                                                       hash_params_list = hash_aux_params_list,
                                                       int_type = INT_TYPE_32)