from src import shingling
import unittest
import numpy as np

INT_TYPE = np.int16

def HashFunction1(text):
    return sum([ord(char) for char in text]) % 10

class TestShingles(unittest.TestCase):

    # ---------------- Duplicates Shingles ----------------#
    def test_TextToShinglesDuplicates(self):
        text = "abcdefg"
        # shingles of len 3
        text_list = ["abc", "bcd", "cde", "def", "efg"]
        shingles_list = [HashFunction1(x) for x in text_list]
        
        expected = np.array(shingles_list, dtype= INT_TYPE)
        result = shingling.TextToShinglesDuplicates(text, 3, HashFunction1, INT_TYPE)
        
        np.testing.assert_array_equal(result, expected)

    # ------------ Uniques Shingles ---------------# 
    def test_TextToShinglesUniques(self):
        text = "abcdefg"
        # shingles of len 3
        text_list = ["abc", "bcd", "cde", "def", "efg"]
        shingles_list = [HashFunction1(x) for x in text_list]
        
        expected =  set(shingles_list)
        result = shingling.TextToShinglesUniques(text, 3, HashFunction1)
        
        self.assertEqual(result, expected)
        
        
        
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_shingles 

if __name__ == "__main__":
    unittest.main()