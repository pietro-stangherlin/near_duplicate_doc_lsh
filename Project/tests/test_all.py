from ..src import shingling
from ..src import minhash
from ..src import hashing
from ..src import lsh
import numpy as np
import json
import sys
import re
import time

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# also before running convert the file to utf-8 and remove BOM (from notepad++ encoding, or another way)
# >>> python -m near_duplicate_doc_lsh.project.tests.test_all


# constants
W = 9 # shingle len
K = 50 # signature len -> number of hash functions
EL = 5 # number of random integers generated
INT_TYPE_32 = np.uint32
INT_TYPE_64 = np.uint64

# exchange hashFunction paramerOrder
def ExHashFun(array: np.array, x: int):
    return hashing.CWtrick32to32(x = x, aux_params= array)

start = time.time()
# generate permutations params
hash_aux_params_list = hashing.GenerateUns64(K, EL, 123)

file_name = "data_near_duplicate\\robust_clones_first_100.json"

with open(file_name, 'r', encoding = "utf-8") as fin, open("signatures.csv", "w") as fout:
    for line in fin:
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
            signature_temp = minhash.GenerateSignatureV3(shingles = shingle_temp,
                                                       hash_function = ExHashFun,
                                                       hash_params_array = hash_aux_params_list,
                                                       int_type = INT_TYPE_64)
            # fout.write(f"{signature_temp}\n")

stop = time.time()

print(f"Time: {stop - start}")