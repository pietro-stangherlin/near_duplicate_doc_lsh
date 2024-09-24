from src import sqlite_one_table
import unittest
import numpy as np

INT_TYPE_U32 = np.uint32
INT_TYPE_U64 = np.uint64

K = 100

# list of documents ids and signatures
TOY_DOCS_ID_SIGNATURE = [(1, np.full(shape = K, fill_value = 11111111, dtype = INT_TYPE_U32)),
                         (2, np.full(shape = K, fill_value = 22222222, dtype = INT_TYPE_U32)),
                         (3, np.full(shape = K, fill_value = 33333333, dtype = INT_TYPE_U32))]


class TestSqliteOneTable(unittest.TestCase):

    def test_sqliteonetable(self):
        
        # initialize the instance
        sql_db = sqlite_one_table.SQLiteOneTable()

        # begin transaction
        sql_db.begin_transaction()

        # insert key value pairs
        sql_db.insert_col1_col2(TOY_DOCS_ID_SIGNATURE[0][0], TOY_DOCS_ID_SIGNATURE[0][1])
        sql_db.insert_col1_col2(TOY_DOCS_ID_SIGNATURE[1][0], TOY_DOCS_ID_SIGNATURE[1][1])

        # end transaction
        sql_db.end_transaction()

        # sql_db.print_all_records()


        # find signatures by key
        result = sql_db.get_col2_by_col1(TOY_DOCS_ID_SIGNATURE[0][0])
        expected = TOY_DOCS_ID_SIGNATURE[0][1]

        # assertion
        np.testing.assert_array_equal(result, expected)

        # close database
        sql_db.close_database()

        # clear the database
        sql_db.delete_database(ask_confirm = False)
        
        

# Warning: this script has to be executed 
# from the (external) project directory as 
# python -m unittest tests.test_sqlite_one_table

if __name__ == "__main__":
    unittest.main()