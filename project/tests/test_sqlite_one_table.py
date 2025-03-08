from src import sqlite_one_table
import unittest
import numpy as np

INT_TYPE_U32 = np.uint32
INT_TYPE_U64 = np.uint64

K = 100

# debugging NOTE: if any error occurs it's likely the database created
# has not been deleted after testing (as it should),
# in that case delete it from the current folder 

class TestSqliteOneTable(unittest.TestCase):

    def test_sqliteonetable(self):
        
        # list of documents ids and signatures
        TOY_DOCS_ID_SIGNATURE = [(1, np.full(shape = K, fill_value = 11111111, dtype = INT_TYPE_U32)),
                         (2, np.full(shape = K, fill_value = 22222222, dtype = INT_TYPE_U32)),
                         (3, np.full(shape = K, fill_value = 33333333, dtype = INT_TYPE_U32))]
        
        # initialize the instance
        sql_db = sqlite_one_table.SQLiteOneTable()

        # begin transaction
        sql_db.begin_transaction()

        # insert key value pairs
        sql_db.insert_col1_col2(TOY_DOCS_ID_SIGNATURE[0][0], TOY_DOCS_ID_SIGNATURE[0][1])
        sql_db.insert_col1_col2(TOY_DOCS_ID_SIGNATURE[1][0], TOY_DOCS_ID_SIGNATURE[1][1])
        sql_db.insert_col1_col2(TOY_DOCS_ID_SIGNATURE[2][0], TOY_DOCS_ID_SIGNATURE[2][1])
        # end transaction
        sql_db.end_transaction()

        # sql_db.print_all_records()

        # find signatures by key
        result = sql_db.get_col2_by_col1(TOY_DOCS_ID_SIGNATURE[0][0])
        expected = TOY_DOCS_ID_SIGNATURE[0][1]

        # assertion
        np.testing.assert_array_equal(result, expected)
        
        # fetch many test
        fetched_rows = sql_db.fetch_all_rows()
        
        row_index = 0
        for row in fetched_rows:
            np.testing.assert_array_equal(row[1],
                                          TOY_DOCS_ID_SIGNATURE[row_index][1])
            row_index += 1

        # close database
        sql_db.close_database()

        # clear the database
        sql_db.delete_database(ask_confirm = False)
        
class TestSqliteOneTableGeneral(unittest.TestCase):

    def test_sqliteonetable_general(self):
        
        my_records = [[1, "lol", ["a", "b", "c"]],
                      [2, "yes", ["d", "d", "c"]],
                      [2, "yes", ["z", "z", "z"]]] # this should NOT be inserted (if all works as intended)
        
        # initialize the instance
        sql_db = sqlite_one_table.SQLiteOneTableGeneral(col_names_list = ["col1", "col2", "col3"],
                                    col_types_list = ["INTEGER", "TEXT", "BLOB"],
                                    col_do_pickle_bool_list = [False, False, True],
                                    col_create_index_bool_list = [True, True, False],
                                    col_not_null_bool_list = [True, False, False],
                                    col_is_unique_bool_list = [True, False, False])

        # begin transaction
        sql_db.begin_transaction()

        # insert key value pairs
        sql_db.insert_record_values(values_list = my_records[0])
        sql_db.insert_record_values(values_list = my_records[1])

        # end transaction
        sql_db.end_transaction()

        print("print_all_records")
        sql_db.print_all_records()
        
        # check for equality
        expected = my_records[0]
        
        result = sql_db.get_records_by_value(col_name = "col1",
                                            col_value = my_records[0][0])[0]
        # where the last [0] is needed to extract the returned list 
        # from the list of lists
        
        self.assertEqual(result, expected)

        # close database
        sql_db.close_database()

        # clear the database
        sql_db.delete_database(ask_confirm = False)     

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_sqlite_one_table

if __name__ == "__main__":
    unittest.main()