from src import lsh
from src import hashing
import unittest
import numpy as np



INT_TYPE = np.int16

def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5

# trivial hash function to use 
def HashFunctionSum1(int_array: np.array):
    '''Sum the HashFunction1 of all array elements
    Args:
        - int_array : numpy array made of integers
        
    Return:
        - sum of hashes % 3 of the array's elements
    '''
    tot = 0
    
    for el in int_array:
        tot += HashFunction1(el)
    
    return tot

# this hash function should be used instead

# input vector:
SIGNATURE1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype = INT_TYPE)

# hash parameters vector: (dimension hash to match with that of SIGNATURE1)
HASH_PARAM_VECTOR1 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype = INT_TYPE)

MODULO1 = 2**32

class TestLSH2ManyBandsClassBTree(unittest.TestCase): 
    def test_LSHManyBandsBucketsBTree(self):
        print("LSHManyBandsBucketsBTree test")
        
        # excluding modulo operator to improve readability (works only for small numbers)
        def SimpleDotHash(x, params) -> int:
            return np.dot(x,params)
        
        def GenerateSimpleHashDot(params):
            
            def temp_fun(x):
                return SimpleDotHash(x, params)
            
            return temp_fun
        
        
        # size 2 bands
        Size2Hash1 = GenerateSimpleHashDot(np.array([0,0]))
        Size2Hash2 = GenerateSimpleHashDot(np.array([1,0]))
        Size2Hash3 = GenerateSimpleHashDot(np.array([1,1]))
        
        # debug, they work
        # print(Size2Hash1(np.array([1,1])))
        # print(Size2Hash2(np.array([1,1])))
        # print(Size2Hash3(np.array([1,1])))
        
        
        # assume 3 bands and trivial list of hash functions
        my_hash_fun_list = [Size2Hash1, Size2Hash2, Size2Hash3]
        
        # generate an instance
        # bands size is 2 if each signature is of length 6 and we have 3 bands (6/3 = 2)
        manyLSH = lsh.LSHManyBandsBucketsBTree(hash_functions_list = my_hash_fun_list,
                                               band_size = 2)
        
        # checks
        # I expect three instances of OneLSH Bands
        
        expected_lsh_n_bands = 3
        result_lsh_n_bands = manyLSH.n_bands
        
        self.assertEqual(result_lsh_n_bands, expected_lsh_n_bands)
        
        
        
        # add some pairs, (signature, doc_id)
        # signature length has to be multiple of 3 in this case
        
        manyLSH.InsertHashInEachBand(signature = np.array([1,2,3,4,5,6]),
                                     id_doc = 1)
        manyLSH.InsertHashInEachBand(signature = np.array([1,2,3,4,5,1]),
                                     id_doc = 2)
        manyLSH.InsertHashInEachBand(signature = np.array([1,2,3,4,2,1]),
                                     id_doc = 3)
        manyLSH.InsertHashInEachBand(signature = np.array([1,2,3,3,2,1]),
                                     id_doc = 4)
        
        # check the elements in each band
        print("manyLSH.bands_object_list[index].more_than_two_buckets_ids_set")
        print(manyLSH.bands_object_list[0].more_than_two_buckets_ids_set)
        print(manyLSH.bands_object_list[1].more_than_two_buckets_ids_set)
        print(manyLSH.bands_object_list[2].more_than_two_buckets_ids_set)
        
        # check buckets of some bands
        
        # first band: the hash is 0, same hash for all, we expect 
        # all documents 
        result_band0 = manyLSH.bands_object_list[0][0]
        expected_band0 = {1,2,3,4}
        
        self.assertEqual(result_band0, expected_band0)
        
        # second band: we expect one band with bucket id 3 = 3+1 + 4*0
        # with all the documents
        result_band1 = manyLSH.bands_object_list[1][3]
        expected_band1 = {1,2,3,4}
        
        self.assertEqual(result_band1, expected_band1)
        
        # third band: 
        # first bucket_id = 5+6 = 11 (doc_id = 1)
        # second bucket_id = 5+1 = 6 (doc_id = 2)
        # third bucket_id = 2+1 = 3 (doc_id = 3, 4)
        
        result_band2_11 = manyLSH.bands_object_list[2][11]
        expected_band2_11 = {1}
        
        self.assertEqual(result_band2_11, expected_band2_11)
        
        result_band2_6 = manyLSH.bands_object_list[2][6]
        expected_band2_6 = {2}
        
        self.assertEqual(result_band2_6, expected_band2_6)
        
        result_band2_3 = manyLSH.bands_object_list[2][3]
        expected_band2_3 = {3,4}
        
        self.assertEqual(result_band2_3, expected_band2_3)
        
        
        del(manyLSH)
        
        print("-----------------------------------------------")
        print("\n")

    
 
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_many_bands_btree

if __name__ == "__main__":
    unittest.main()