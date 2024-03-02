from src import minhash
from src import hashing
import unittest
import numpy as np

INT_TYPE_U32 = np.uint32
INT_TYPE_U64 = np.uint64

# permutations number
K = 100


# list of documents ids and signatures
TOY_DOCS_ID_SIGNATURE = [(1, np.full(shape = K, fill_value = 11111111, dtype = INT_TYPE_U32)),
                         (2, np.full(shape = K, fill_value = 22222222, dtype = INT_TYPE_U32)),
                         (3, np.full(shape = K, fill_value = 33333333, dtype = INT_TYPE_U32))]




class TestSignaturesSqlite(unittest.TestCase):

    def test_signaturesqlite(self):
        
        # initialize the instance
        sql_db = minhash.SignaturesSQLite()

        # begin transaction
        sql_db.begin_transaction()

        # insert key value pairs
        sql_db.insert_id_signature(TOY_DOCS_ID_SIGNATURE[0][0], TOY_DOCS_ID_SIGNATURE[0][1])
        sql_db.insert_id_signature(TOY_DOCS_ID_SIGNATURE[1][0], TOY_DOCS_ID_SIGNATURE[1][1])

        # end transaction
        sql_db.end_transaction()

        sql_db.print_all_records()

        # find signatures by key
        # result = sql_db.get_signature(TOY_DOCS_ID_SIGNATURE[0][0])
        # expected = TOY_DOCS_ID_SIGNATURE[0][1]



        # assertion
        # np.testing.assert_array_equal(result, expected)

        # clear the database
        sql_db.clear_database()
        
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_minhash

if __name__ == "__main__":
    unittest.main()