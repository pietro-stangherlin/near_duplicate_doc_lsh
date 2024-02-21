from src import functions_lsh as lsh
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
    
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh 

if __name__ == "__main__":
    unittest.main()