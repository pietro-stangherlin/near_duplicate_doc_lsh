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
    
    def test_ComputeHashValues(self):
        expected = np.array([1, 1, 1], dtype = INT_TYPE)
        
        result = minhash.ComputeHashValues(1, hash_funs_list, INT_TYPE)
        
        np.testing.assert_array_equal(result, expected)

    
    def test_ComputeHashValuesV2(self):
        expected = np.array([1, 1, 1], dtype = INT_TYPE)
        
        result = minhash.ComputeHashValuesV2(1, HashGeneral1, hash_params_list_1, INT_TYPE)
        
        np.testing.assert_array_equal(result, expected)
    
    
    
    def test_HashDictionary(self):
        shingles_array_1 = np.array([1, 2, 3, 4, 5], dtype = INT_TYPE)
        
        expected_hash_dictionary = {1 : np.array([1, 1, 1], dtype = INT_TYPE),
                                    2 : np.array([2, 2, 2], dtype = INT_TYPE),
                                    3 : np.array([0, 3, 3], dtype = INT_TYPE),
                                    4 : np.array([1, 0, 4], dtype = INT_TYPE),
                                    5 : np.array([2, 1, 0], dtype = INT_TYPE)}
        
        minhash.GenerateSignature(shingles_array_1,
                                hash_funs_list,
                                True,
                                hash_dict,
                                int_type = INT_TYPE)
        
        print(hash_dict)
        
        result_hash_dictionary = hash_dict
    
        
        for key in expected_hash_dictionary.keys():
            np.testing.assert_array_equal(result_hash_dictionary[key],
                                          expected_hash_dictionary[key])
    
    def test_GenerateSignature_1(self):
        # clear dict
        hash_dict.clear()
        
        shingles_array_1 = np.array([1, 2, 3, 4, 5], dtype = INT_TYPE)

        # permutations based of HashFunctions 1, 2, 3
        permutation_1 = np.array([1, 2, 0, 1, 2], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 3, 0, 1], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 3, 4, 0], dtype = INT_TYPE)
        
        # for each permutation choose the shingle with the lowest permutation value
        signature_expected = np.array([3, 4, 5], dtype = INT_TYPE)
        
        # tested function result
        result_function = minhash.GenerateSignature(shingles_array_1,
                                                 hash_funs_list,
                                                 True,
                                                 hash_dict,
                                                 int_type = INT_TYPE)
        
        # clean dictionary so other test are not influenced by this
        hash_dict.clear()
        
        np.testing.assert_array_equal(result_function, signature_expected)
    
    def test_GenerateSignature_2(self):
        # clear dict
        hash_dict.clear()
        
        shingles_array_1 = np.array([1, 2, 2, 4, 5], dtype = INT_TYPE)

        # permutations based on HashFunctions 1, 2, 3
        permutation_1 = np.array([1, 2, 2, 1, 2], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 0, 1], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 4, 0], dtype = INT_TYPE)
        
        # for each permutation choose the shingle with the lowest permutation value
        signature_expected = np.array([1, 4, 5], dtype = INT_TYPE)
        
        # tested function result
        result_function = minhash.GenerateSignature(shingles_array_1,
                                                 hash_funs_list,
                                                 True,
                                                 hash_dict,
                                                int_type = INT_TYPE)
        
        # clean dictionary so other test are not influenced by this
        hash_dict.clear()
        
        np.testing.assert_array_equal(result_function, signature_expected)
        
        # no dictionary
    def test_GenerateSignature_3(self):
        
        shingles_array_1 = np.array([1, 2, 2, 4, 5], dtype = INT_TYPE)

        # permutations based on HashFunctions 1, 2, 3
        permutation_1 = np.array([1, 2, 2, 1, 2], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 0, 1], dtype = INT_TYPE)
        permutation_2 = np.array([1, 2, 2, 4, 0], dtype = INT_TYPE)
        
        # for each permutation choose the shingle with the lowest permutation value
        signature_expected = np.array([1, 4, 5], dtype = INT_TYPE)
        
        # tested function result
        result_function = minhash.GenerateSignature(shingles_array_1,
                                                 hash_funs_list,
                                                 False,
                                                 None,
                                                int_type = INT_TYPE)
        
        
        np.testing.assert_array_equal(result_function, signature_expected)
    
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