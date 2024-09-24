import sqlite3
import pickle
import os


# ---------------- SQLite one table database ------------------------#
# This class will be used for storing both signatures and buckets
# (with slightly different specifications)
class SQLiteOneTable:
    '''Link to (or create) a sqlite3 database with one table.
    The database created assumes a simple schema:
    a unique table with columns: (col1 , col2)
    '''

    def __init__(self,
                 database_name: str = "db_name",
                 col1_type: str = "INTEGER",
                 col2_type: str = "BLOB",
                 table_name: str = "table_1",
                 col1_name: str = "col1_name",
                 col2_name: str = "col2_name",
                 do_pickle: bool = True,
                 create_index_on_col1: bool = True):
        '''Inizialize the instance creating the database.
        
        
        Args:
            - database_name: name of the database used or to be created
            - col1_type: type of the table's column 1 (INTEGER, REAL, TEXT, BLOB)
            - col2_type: type of the table's column 2 (INTEGER, REAL, TEXT, BLOB)
            - table_name: name of the unique table
            - col1_name: name of column 1
            - col2_name: name of column 2
            - do_pickle: tell if the values should be pickled and unpickled,
                        pickling has the advantage of saving attributes
                        (for some supported) python classes
            - create_index_on_col1: if True create index relative to column 1 
        
        NOTE: with SQLite Primary key specification is not needed, as deafult primary key 
        the rowid is used (unless specified otherwise), see:
        https://www.sqlite.org/lang_createtable.html#rowid
        '''

        self.database_name = database_name
        self.table_name = table_name

        self.col1_type = col1_type
        self.col2_type = col2_type

        self.col1_name = col1_name
        self.col2_name = col2_name

        self.do_pickle = do_pickle

        # connect or create database
        self.connect = sqlite3.connect(self.database_name)
        # cursor: used to perform operations
        self.cursor = self.connect.cursor()
        
        # create table if not present
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                            ({self.col1_name} {col1_type},
                            {self.col2_name} {self.col2_type})''')
        
        # create column 1 index if specified
        if create_index_on_col1:
            self.cursor.execute(f'''CREATE INDEX idx_col1 
                                ON {self.table_name} ({self.col1_name});''')
        
        # define methods based on do_pickle
        if self.do_pickle:
            self._insert_col1_col2 = self._insert_col1_col2_yes_pickle
            self._get_col2_by_col1 = self._get_col2_by_col1_yes_pickle
        else:
            self._insert_col1_col2 = self._insert_col1_col2_no_pickle
            self._get_col2_by_col1 = self._get_col2_by_col1_no_pickle
        
    
    def begin_transaction(self):
        '''Begin a transaction relative to the database.
        Remember to always end it.
        '''
        self.cursor.execute('BEGIN TRANSACTION')
        
    def end_transaction(self):
        '''Ending a database transaction.
        '''
        self.connect.commit()
    
    def insert_col1_col2(self, col1_value, col2_value):
        '''Insert a pair (col1, col2) in the database.

        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            col1_value:
            col2_value
        '''
        self._insert_col1_col2(col1_value, col2_value)
    
    def get_col2_by_col1(self, col1_value):
        '''Return value relative to column 1 value.
        
        Args:
            col1_value
        
        Return:
            col2_value
        '''
        return self._get_col2_by_col1(col1_value)
    
    def close_database(self):
        '''Close the SQLite database connection.
        '''
        self.connect.close()
    
    def delete_database(self,
                        ask_confirm: bool = True):
        '''Delete the SQLite database file.

        Args:
            ask_confirm: if True (default) ask the user a confirmation
        '''

        if ask_confirm:
            delete_yes = input("If you want to delete the database file digit Y, any other input wont delete it.\n")
            
            if delete_yes == "Y":
                os.remove(self.database_name)
        
        else:
            os.remove(self.database_name)

    def print_all_records(self):
        '''Print all records in the SQLite database.
        '''
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
    
    # hidden methods defined so the "if check" is done only once
    # (when the instance is inizialized)
    def _insert_col1_col2_yes_pickle(self, col1_value, col2_value):
        '''(hidden) Insert a pair (col1_value, col2_value) in the database.
            YesPickle
        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            key:
            value:
        '''
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES (?,?)",
                  (col1_value, pickle.dumps(col2_value)))
    
    def _insert_col1_col2_no_pickle(self, col1_value, col2_value):
        '''(hidden) Insert a pair (col1_value, col2_value) in the database.
            NoPickle        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            - col1_value
            - col2_value
        '''
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES (?,?)",
                  (col1_value, col2_value))
    
    def _get_col2_by_col1_yes_pickle(self, col1_value):
        '''(hidden) Return col2_value relative to col1_value.
            YesPickle
        Args:
            col1_value
        Return:
            col2_value
        '''
        return pickle.loads(self.connect.execute(f"SELECT {self.col2_name} FROM {self.table_name} WHERE {self.col1_name}=?",
                                     (col1_value,)).fetchone()[0])
        
    def _get_col2_by_col1_no_pickle(self, col1_value):
        '''(hidden) Return value relative to col1_value.
            NoPickle
        Args:
            - col1_value
        
        Return:
            - col2_value
        '''
        return self.connect.execute(f"SELECT {self.col2_name} FROM {self.table_name} WHERE {self.col1_name}=?",
                                     (col1_value,)).fetchone()[0]

    