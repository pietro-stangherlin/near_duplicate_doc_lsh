from src import minhash
import unittest
import numpy as np

INT_TYPE = np.int64

def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5

hash_funs_list = [HashFunction1, HashFunction2, HashFunction3]

hash_dict = dict()

# --------- V2 versions: use list of hash parameters instead of list of hash functions
# example equivalent to the previously defined hash functions
def HashGeneral1(number, params_array):
    modulo = params_array[0]
    return number % modulo

hash_params_list_1 = [[3], [4], [5]]


class TestSignatures(unittest.TestCase):

    
    def test_ComputeHashValuesV2(self):
        expected = np.array([1, 1, 1], dtype = INT_TYPE)
        
        result = minhash.ComputeHashValuesV2(1, HashGeneral1, hash_params_list_1, INT_TYPE)
        
        np.testing.assert_array_equal(result, expected)
    
    def test_GenerateSignature_3V2(self):
        
        shingles_array_1 = np.array([1, 2, 2, 4, 5], dtype = INT_TYPE)

        # permutations based on HashFunctions 1, 2, 3
        permutation_1 = np.array([1, 2, 2, 1, 2], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 0, 1], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 4, 0], dtype = INT_TYPE)
        
        # for each permutation choose the shingle with the lowest permutation value
        signature_expected = np.array([1, 4, 5], dtype = INT_TYPE)
        
        # tested function result
        result_function = minhash.GenerateSignatureV2(shingles_array_1,
                                                 HashGeneral1,
                                                 hash_params_list_1,
                                                 False,
                                                 None,
                                                int_type = INT_TYPE)
        
        
        np.testing.assert_array_equal(result_function, signature_expected)
        
        
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_minhash

if __name__ == "__main__":
    unittest.main()