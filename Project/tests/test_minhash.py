from src import functions_minhash_lsh as funs
import unittest
import numpy as np

INT_TYPE = np.int16

def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5

hash_funs_list = [HashFunction1, HashFunction2, HashFunction3]

hash_dict = dict()


class TestSignatures(unittest.TestCase):
    
    def test_ComputeHashValues(self):
        expected = np.array([1, 1, 1], dtype = INT_TYPE)
        
        result = funs.ComputeHashValues(1, hash_funs_list, INT_TYPE)
        
        np.testing.assert_array_equal(result, expected)
    
    
    def test_HashDictionary(self):
        shingles_array_1 = np.array([1, 2, 3, 4, 5], dtype = INT_TYPE)
        
        expected_hash_dictionary = {1 : np.array([1, 1, 1], dtype = INT_TYPE),
                                    2 : np.array([2, 2, 2], dtype = INT_TYPE),
                                    3 : np.array([0, 3, 3], dtype = INT_TYPE),
                                    4 : np.array([1, 0, 4], dtype = INT_TYPE),
                                    5 : np.array([2, 1, 0], dtype = INT_TYPE)}
        
        funs.GenerateSignature(shingles_array_1,
                                hash_funs_list,
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
        result_function = funs.GenerateSignature(shingles_array_1,
                                                 hash_funs_list,
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
        result_function = funs.GenerateSignature(shingles_array_1,
                                                 hash_funs_list,
                                                 hash_dict,
                                                int_type = INT_TYPE)
        
        # clean dictionary so other test are not influenced by this
        hash_dict.clear()
        
        np.testing.assert_array_equal(result_function, signature_expected)
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_minhash

if __name__ == "__main__":
    unittest.main()