from src import minhash
from src import hashing
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

TEST_ARRAY = np.array([[11111111, 22222222, 3333333, 444444444, 555555555],
                       [66666666, 77777777, 8888888, 999999999, 858488463],
                       [13131141, 13141411, 5363636, 747747484, 858488463],
                       [13131141, 13141411, 5363636, 747747484, 858488463]])

# --------- V2 versions: use list of hash parameters instead of list of hash functions
# example equivalent to the previously defined hash functions
def HashGeneral1(number, params_array):
    modulo = params_array[0]
    return number % modulo




class TestSignatures(unittest.TestCase):
    pass
        
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_minhash

if __name__ == "__main__":
    unittest.main()