from src import lsh
import unittest
import numpy as np


INT_TYPE = np.int16

def HashFunction1(number):
    return number % 3
def HashFunction2(number):
    return number % 4
def HashFunction3(number):
    return number % 5

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

class TestLSH(unittest.TestCase):
    
    def test_ComputeHashBand(self):
        signature1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype = INT_TYPE)
        inf_index = 2
        sup_index = 5
        doc_id1 = 23
        
        # hash function used: HashFunction1
        expected = (0 + 1 + 2, doc_id1)
        
        result = lsh.ComputeHashBand(signature1,
                                     inf_index,
                                     sup_index,
                                     doc_id1,
                                     HashFunctionSum1)
        self.assertEqual(result, expected)
        
    
    def test_LSHOneBandBucketsNaive(self):
        expected = lsh.LSHOneBandBucketsNaive()
        expected.buckets = {3 : [12, 16], 7 : [14]}
        expected
        
        result = lsh.LSHOneBandBucketsNaive()
        result.insert(3, 12)
        result.insert(3, 16)
        result.insert(7, 14)
        
        self.assertEqual(result.buckets, expected.buckets)
        
        expected_iter = [[12, 16], [14]]
        result_iter = [el for el in result.iter()]
        
        self.assertEqual(result_iter, expected_iter)
        
        expected_iter_more_than_one = [[12, 16]]
        result_iter_more_than_one = [el for el in result.iter_more_than_one()]
        
        self.assertEqual(result_iter_more_than_one, expected_iter_more_than_one)

    def test_LSHAllBandsBucketsNaive(self):
        # two bands
        result = lsh.LSHAllBandsBucketsNaive(2)
        result.insert(0, 3, 12)
        result.insert(0, 3, 16)
        result.insert(0, 7, 14)
        result.insert(1, 2, 12)
        result.insert(1, 2, 16)
        result.insert(1, 5, 14)
        
        expected_band1 = {3 : [12, 16], 7 : [14]}
        expected_band2 = {2 : [12, 16], 5 : [14]}
        
        
        self.assertEqual(result.bands_list[0].buckets, expected_band1)
        self.assertEqual(result.bands_list[1].buckets, expected_band2)
        
        expected_iter_band0 = [[12, 16], [14]]
        result_iter_band0 = [el for el in result.iter_band(0)]
        self.assertEqual(result_iter_band0, expected_iter_band0)
        
        expected_iter_more_than_one_band0 = [[12, 16]]
        result_iter__more_than_one_band0 = [el for el in result.iter_band_more_than_one(0)]
        self.assertEqual(result_iter__more_than_one_band0,
                         expected_iter_more_than_one_band0)
        
        
    
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh 

if __name__ == "__main__":
    unittest.main()