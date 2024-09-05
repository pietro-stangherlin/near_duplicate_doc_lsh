from ..src import hashing
from ..src import shingling
from ..src import minhash
import numpy as np
import unittest


# important: to execute the script from external directory

# If data is in test_data: (use this in testing)
# >>> python -m project.tests.test_minhash

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.project.tests.test_minhash


# constants
W = 9 # shingle len
K = 50 # signature len -> number of hash functions
EL = 2 # number of random integers generated
INT_TYPE_U32 = np.uint32
INT_TYPE_U64 = np.uint64

INT_TYPE = INT_TYPE_U32

# list of documents ids and signatures
TOY_DOCS_ID_SIGNATURE = [(1, np.full(shape = K, fill_value = 11111111, dtype = INT_TYPE)),
                         (2, np.full(shape = K, fill_value = 22222222, dtype = INT_TYPE)),
                         (3, np.full(shape = K, fill_value = 33333333, dtype = INT_TYPE))]

class TestSignaturesSqlite(unittest.TestCase):

    def test_signaturesqlite(self):
        
        # initialize the instance
        sql_db = minhash.SignaturesSQLite()

        # begin transaction
        sql_db.begin_transaction()

        # insert key value pairs
        sql_db.insert_key_value(TOY_DOCS_ID_SIGNATURE[0][0], TOY_DOCS_ID_SIGNATURE[0][1])
        sql_db.insert_key_value(TOY_DOCS_ID_SIGNATURE[1][0], TOY_DOCS_ID_SIGNATURE[1][1])

        # end transaction
        sql_db.end_transaction()

        # sql_db.print_all_records()


        # find signatures by key
        result = sql_db.get_value_by_key(TOY_DOCS_ID_SIGNATURE[0][0])
        expected = TOY_DOCS_ID_SIGNATURE[0][1]

        # assertion
        np.testing.assert_array_equal(result, expected)

        # close database
        sql_db.close_database()

        # clear the database
        sql_db.delete_database(ask_confirm = False)


# generate permutations params
hash_params_matrix = hashing.GenerateNumpyArray(num_rows = K,
                                                num_cols = EL,
                                                seed = 123,
                                                reshape = True,
                                                int_type = INT_TYPE_U64)


TOY_DOCS = [{"id2": 1, "id3": "NULL", "content": "abcdefghilmno"},
            {"id2": 2, "id3": "NULL", "content": "up in the sky we shine"},
            {"id2": 3, "id3": 1, "content": "abcdefghilmno"}, # equal to first document
            {"id2": 4, "id3": "NULL", "content": "temple os in for real"},
            {"id2": 5, "id3": "NULL", "content": "bob and alice here are mentioned"}]

class TestMinHash_SQL_and_BTree(unittest.TestCase):
    
    def test_minhashSQL(self):
        
        # just for debug
        signatures_temp_dict = dict()
        
        # inizialize SignaturesSQLite
        SigSQL = minhash.SignaturesSQLite()
        
        # number of insertions for each transaction
        NUM_SQL_INSERTIONS = 3
        insertion_counter = 0

        SigSQL.begin_transaction()
        
        
        for el in TOY_DOCS:
                
            id_temp = el["id2"]
            text_temp = el["content"]
            shingle_temp = shingling.TextToShinglesUniques(text = text_temp,
                                                               shingle_len = W,
                                                               hash_fun = hashing.MurmUns32Hash)
            
            signature_temp = minhash.NumbaSignatureByRowParallel(shingles_array = np.array(list(shingle_temp),
                                                                                               dtype= INT_TYPE),
                                                                     hash_params_matrix = hash_params_matrix,
                                                                     hash_fun = hashing.NumbaNaiveHashU32Params,
                                                                     int_type = INT_TYPE)
            
            # just for debug
            signatures_temp_dict[id_temp] = signature_temp
                
            # add key (doc id) value (signature) pair to the SignatureSQL
            if insertion_counter % NUM_SQL_INSERTIONS == 0:
                SigSQL.end_transaction()
                SigSQL.begin_transaction()
            
            SigSQL.insert_key_value(key = id_temp, value = signature_temp)

            insertion_counter += 1
        
        # print(f"Signature dict: {signatures_temp_dict}")
        
        # outside the for loop
        SigSQL.end_transaction()

        # compare the similarity of two documents: those two should be equal
        doc1_id = 1
        doc2_id = 3
        
        value1 = SigSQL.get_value_by_key(doc1_id)
        value2 = SigSQL.get_value_by_key(doc2_id)
        
        print("SQL")

        sim_doc1_doc2 = minhash.SignatureSimilarity(value1, value2)
        print(f'''The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}
              Should be 1''')
        
        self.assertEqual(sim_doc1_doc2, 1.0)
        
        # compare the similarity of two documents: those two should be different
        doc1_id = 1
        doc2_id = 5
        
        value1 = SigSQL.get_value_by_key(doc1_id)
        value2 = SigSQL.get_value_by_key(doc2_id)

        sim_doc1_doc2 = minhash.SignatureSimilarity(value1, value2)
        print(f'''The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}
              Should be less than 1''')
        
        self.assertLess(sim_doc1_doc2, 1)

        SigSQL.close_database()
        SigSQL.delete_database(ask_confirm = False)
    
    def test_minhashBTree(self):
        
        # just for debug
        signatures_temp_dict = dict()
        
        # initialize Signature Btree instance
        SigBTree = minhash.SignaturesBTree()
        
        for el in TOY_DOCS:
                
            id_temp = el["id2"]
            text_temp = el["content"]
            shingle_temp = shingling.TextToShinglesUniques(text = text_temp,
                                                               shingle_len = W,
                                                               hash_fun = hashing.MurmUns32Hash)
            
            signature_temp = minhash.NumbaSignatureByRowParallel(shingles_array = np.array(list(shingle_temp),
                                                                                               dtype= INT_TYPE),
                                                                     hash_params_matrix = hash_params_matrix,
                                                                     hash_fun = hashing.NumbaNaiveHashU32Params,
                                                                     int_type = INT_TYPE)
            
            # just for debug
            signatures_temp_dict[id_temp] = signature_temp
            
            # add key (doc id) value (signature) pair to the Signature Btree
            SigBTree.insert(id_temp, signature_temp)
                
            
        
        # print(f"Signature dict: {signatures_temp_dict}")
        # compare the similarity of two documents: those two should be equal
        doc1_id = 1
        doc2_id = 3

        print("BTree")
        
        sim_doc1_doc2 =  SigBTree.compute_similarity(doc1_id, doc2_id)
        print(f'''The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}
              Should be 1''')
        
        self.assertEqual(sim_doc1_doc2, 1.0)
        
        # compare the similarity of two documents: those two should be different
        doc1_id = 1
        doc2_id = 5
        
        sim_doc1_doc2 =  SigBTree.compute_similarity(doc1_id, doc2_id)
        
        print(f'''The signature similarity between doc {doc1_id} and doc {doc2_id} is {sim_doc1_doc2}
              Should be less than 1''')
        
        self.assertLess(sim_doc1_doc2, 1)


# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_minhash

if __name__ == "__main__":
    unittest.main()