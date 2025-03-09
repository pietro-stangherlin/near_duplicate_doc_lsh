from src import lsh
import unittest
    
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

class TestLSH1OneBandClassSQL(unittest.TestCase):
    def test_LSHOneBandBucketsSQL(self):
        print("LSHOneBandBucketsSQL test")
        
        # initialize instance
        band_instance_sql = lsh.LSHOneBandSQLite_id_bucket_id_doc(col_types_list = ["INTEGER", "INTEGER"])
        
        # add some key value pairs
        band_instance_sql.begin_transaction()
        
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 1, id_doc_value = 4)
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 1, id_doc_value = 5)
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 2, id_doc_value = 7)
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 2, id_doc_value = 9)
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 3, id_doc_value = 10)
        band_instance_sql.insert_bucket_doc_pair(bucket_value = 4, id_doc_value = 11)
        
        band_instance_sql.end_transaction()
        
        band_instance_sql.print_all_records()
        
        # first use the standard output
        band_instance_sql.getDocIdsByBucket(output_path = "stdout")
        
        # delete database
        band_instance_sql.close_database()
        
        band_instance_sql.delete_database(ask_confirm = False)
        
        
        
        
        print("-----------------------------------------------")
        print("\n")
 
# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_lsh_one_band_btree

if __name__ == "__main__":
    unittest.main()