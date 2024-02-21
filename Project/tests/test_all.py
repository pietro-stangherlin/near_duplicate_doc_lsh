import src.shingling as shingling
import src.minhash as minhash
import src.lsh as lsh
import numpy as np
import json
import sys
import re

# constants
W = 4 # shingle len
K = 6 # signature len -> number of hash functions
B = 3 # LSH bands number

INT_TYPE = np.int16

# hash dictionary to create the signature
hash_dict = dict()

# define hash functions for all steps
# shingle hash function
def HashFunction0(text):
    return sum([ord(char) for char in text]) % 10

# mihash
# one for each signature element
# the first 3 are also used for the bands of LSH
def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5
def HashFunction4(number):
    return number % 6
def HashFunction5(number):
    return number % 7
def HashFunction6(number):
    return number % 8

hash_sig_list = [HashFunction1, HashFunction2, HashFunction3,
                 HashFunction4, HashFunction5, HashFunction6]

hash_lsh_list = [HashFunction1, HashFunction2, HashFunction3]

# initialize LSH data structure
lsh_object = lsh.LSHAllBandsBucketsNaive(bands_number = B)

# default file name
file_name = "toy_data.json"

# file name from command line
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    


# read file line by line
with open(file_name, 'r') as file:
    for line in file:
        # Use regular expression to find the content inside the brackets
        match = re.search(r'\{(.*)\}', line)
        if match:
            content = match.group(0)  # group(0) returns the entire match
            json_content = json.loads(content)  # Convert the content to JSON
            id_temp = json_content["id1"]
            text_temp = json_content["text"]
            shingle_temp = shingling.TextToShinglesArray(text_temp,
                                                         W,
                                                         HashFunction0,
                                                         INT_TYPE)
            signature_temp = minhash.GenerateSignature(shingle_temp,
                                                       hash_sig_list,
                                                       hash_dict,
                                                       INT_TYPE)
            # print(signature_temp)
            # LSH for each band
            # PROBLEM: K is actually useless
            # beacuse it is derived from the len of the hash function list
            # That problem is also present in LSH
            # maybe I should insert some kind type of check
            # or think better about the classes
            
            step = K // B
            band_index = 0
            for i in range(0, K, step):
                # Convert the slice to a string, then to an integer
                integer = int(''.join(map(str, signature_temp[i: i + step])))
                lsh_object.insert(band_index,
                                  hash_lsh_list[band_index](integer),
                                  id_temp)
                band_index += 1


t = lsh_object.iter_more_than_one_all_bands()

for el in t:
    print("----------- band -------------")
    for val in el:
        print(val)    