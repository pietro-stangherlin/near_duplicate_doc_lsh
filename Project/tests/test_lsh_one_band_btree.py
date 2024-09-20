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

# define the actual hash function
def MotwaniHash1(signature):
    return (hashing.MotwaniBandArrayHash(v = signature,
                                 random_int_array = HASH_PARAM_VECTOR1,
                                 modulo = MODULO1))



# given a vector of parameters [a1,...,a]


class TestLSHFunctions(unittest.TestCase):
    
    def test_ComputeOneHashGivenParameters(self):
        result1 = MotwaniHash1(SIGNATURE1)
        expected1 = sum(SIGNATURE1) % MODULO1
        
        self.assertEqual(result1, expected1)
        
        print("-----------------------------------------------")
        print("\n")
        
        
    
    def test_ComputeHashBand(self):
        signature1 = SIGNATURE1
        inf_index = 2
        sup_index = 5
        
        
        # trivial hash function
        # hash function used: HashFunction1
        expected1 = 0 + 1 + 2
        
        result1 = lsh.ComputeHashBand(signature1,
                                     inf_index,
                                     sup_index,
                                     HashFunctionSum1)
        self.assertEqual(result1, expected1)
        
        print("-----------------------------------------------")
        print("\n")
        
        # I need to define another hash function suited for the band dimension
        # non trivial hash function (base function is tested in test_ComputeOneHashGivenParameters)
        def MotwaniHash2(signature):
            return (hashing.MotwaniBandArrayHash(v = signature,
                                 random_int_array = HASH_PARAM_VECTOR1[inf_index:sup_index],
                                 modulo = MODULO1))
        
        result2 = lsh.ComputeHashBand(signature1,
                                     inf_index,
                                     sup_index,
                                     MotwaniHash2)
        
        
        expected2 = sum(signature1[inf_index:sup_index]) % MODULO1
        
        self.assertEqual(result2, expected2)
    
    def test_GenerateMotwaniHashFunctionsList(self):
        print("GenerateMotwaniHashFunctionsList test")
        
        l1 = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = 5,
                                                band_size = 3,
                                                modulo = 2**32,
                                                seed = 123)
        
        print("function list")
        print(l1)
        
        print("try one function")
        print(l1[0](np.array([1,1,2])))
        
        print("-----------------------------------------------")
        print("\n")
    
class TestLSH1OneBandClassBTree(unittest.TestCase):
    def test_LSHOneBandBucketsBTree(self):
        print("LSHOneBandBucketsBTree test")
        
        # initialize the instance
        band_instance = lsh.LSHOneBandBucketsBTree()
        
        # add some key value pairs
        band_instance.add_ids_pair(id_bucket = 1, id_doc = 4)
        band_instance.add_ids_pair(id_bucket = 1, id_doc = 5)
        band_instance.add_ids_pair(id_bucket = 2, id_doc = 7)
        band_instance.add_ids_pair(id_bucket = 2, id_doc = 9)
        band_instance.add_ids_pair(id_bucket = 3, id_doc = 10)
        band_instance.add_ids_pair(id_bucket = 4, id_doc = 11)
        
        # check sets of one and sets of two by key
        # two elements set
        result_key_value = band_instance[1]
        expected_key_value = set([4, 5])
        
        self.assertEqual(result_key_value,
                         expected_key_value)
        
        # one element set
        result_key_value = band_instance[3]
        expected_key_value = set([10])
        
        self.assertEqual(result_key_value,
                         expected_key_value)
        
        
        # more than two buckets ids set
        result_more_than_two_buckets_ids_set = band_instance.more_than_two_buckets_ids_set
        print("band_instance.more_than_two_buckets_ids_set:")
        print(result_more_than_two_buckets_ids_set)
        
        expected_more_than_two_buckets_ids_set = set([1,2])
        
        self.assertEqual(result_more_than_two_buckets_ids_set,
                         expected_more_than_two_buckets_ids_set)
        
        del(band_instance)
        
        print("-----------------------------------------------")
        print("\n")
 
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_one_band_btree

if __name__ == "__main__":
    unittest.main()