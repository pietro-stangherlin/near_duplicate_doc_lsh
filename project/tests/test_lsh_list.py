from src import lsh
import numpy as np
import unittest
    
class TestLSHClassLists(unittest.TestCase):
    def test_LSHOneBandBucketsLists(self):
        print("LSHOneBandBucketLists test")
        
        # initialize the instance
        band_instance = lsh.LSHOneBandBucketLists(n_buckets = 5)
        
        # add some key value pairs
        band_instance.AddToBucket(bucket_id = 1, object = 4)
        band_instance.AddToBucket(bucket_id = 1, object = 5)
        band_instance.AddToBucket(bucket_id = 2, object = 7)
        band_instance.AddToBucket(bucket_id = 2, object = 9)
        band_instance.AddToBucket(bucket_id = 3, object = 10)
        band_instance.AddToBucket(bucket_id = 4, object = 11)
        
        # check sets of one and sets of two by key
        # two elements set
        result_key_value = band_instance.band[1]
        expected_key_value = [4, 5]
        
        self.assertEqual(result_key_value,
                         expected_key_value)
        
        # one element set
        result_key_value = band_instance.band[3]
        expected_key_value = [10]
        
        self.assertEqual(result_key_value,
                         expected_key_value)
        
        
        # more than two buckets ids set
        result_more_than_one_index = band_instance.more_than_one_index
        print("band_instance.more_than_one_index:")
        print(result_more_than_one_index)
        
        expected_more_than_one_index = set([1,2])
        
        self.assertEqual(result_more_than_one_index,
                         expected_more_than_one_index)
        
        del(band_instance)
        
        print("-----------------------------------------------")
        print("\n")

    def test_LSHManyBandsBucketLists(self):
        print("LSHManyBandsBucketLists test")

        N_BANDS = 3
        N_BUCKETS = 5
        SIGNATURE_LEN = 6

        def MyBandHash(np_array_input):
            return np.dot(np_array_input, np_array_input) % N_BUCKETS


        HASH_FUNCTION_LIST = [MyBandHash for i in range(N_BANDS)]
        
        # initialize the instance
        lsh_instance = lsh.LSHManyBandsBucketLists(n_bands = N_BANDS,
                                                    n_buckets = N_BUCKETS, # not used param, here depends on hash function
                                                    signature_len = SIGNATURE_LEN,
                                                    hash_function_list = HASH_FUNCTION_LIST)
        
        lsh_instance.AddIdBySignature(id = 1, signature = np.array([1, 1, 5, 1, 4, 1]))
        lsh_instance.AddIdBySignature(id = 2, signature = np.array([1, 1, 5, 1, 1, 1]))
        lsh_instance.AddIdBySignature(id = 3, signature = np.array([2, 1, 2, 1, 5, 1]))
        lsh_instance.AddIdBySignature(id = 4, signature = np.array([2, 1, 3, 1, 5, 1]))
        lsh_instance.AddIdBySignature(id = 5, signature = np.array([3, 1, 4, 1, 1, 1]))

        all_pairs = lsh_instance.FindAllPairs()

        print(all_pairs)
        
        
        print("-----------------------------------------------")
        print("\n")


 
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_list

if __name__ == "__main__":
    unittest.main()