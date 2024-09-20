import sqlite3
import pickle
import os


# ---------------- SQLite one table database ------------------------
class SQLiteOneTable:
    '''Link to (or create) a sqlite3 database with one table.
    The database created assumes a simple schema:
    a unique table with fields: [key , value]
    '''

    def __init__(self,
                 database_name: str = "signatures_db",
                 key_type: str = "INTEGER",
                 value_type: str = "BLOB",
                 table_name: str = "table_1",
                 key_name: str = "key",
                 value_name: str = "value",
                 do_pickle: bool = True):
        '''Inizialize the instance creating the database.
        
        Args:
            - database_name: name of the database used or to be created
            - key_type: type of the table's key (INTEGER, REAL, TEXT, BLOB)
            - value_type: type of the table's value (INTEGER, REAL, TEXT, BLOB)
            - table_name: name of the unique table
            - key_name: name of the unique key
            - value_name: name of the value
            - do_pickle: tell if the values should be pickled and unpickled,
                        pickling has the advantage of saving attributes
                        (for some supported) python classes
        '''

        self.database_name = database_name
        self.table_name = table_name

        self.key_type = key_type
        self.value_type = value_type

        self.key_name = key_name
        self.value_name = value_name

        self.do_pickle = do_pickle

        # connect or create database
        self.connect = sqlite3.connect(self.database_name)
        # cursor: used to perform operations
        self.cursor = self.connect.cursor()
        
        # create table if not present
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                            ({self.key_name} {key_type} PRIMARY KEY, {self.value_name} {self.value_type})''')
        
        # if primary key is integer index is automatically created by sqlite
        # https://www.sqlite.org/lang_createtable.html#rowid
        
        # define methods based on do_pickle
        if self.do_pickle:
            self._insert_key_value = self._insert_key_value_yes_pickle
            self._get_value_by_key = self._get_value_by_key_yes_pickle
        else:
            self._insert_key_value = self._insert_key_value_no_pickle
            self._get_value_by_key = self._get_value_by_key_no_pickle
        
    
    def begin_transaction(self):
        '''Begin a transaction relative to the database.
        Remember to always end it.
        '''
        self.cursor.execute('BEGIN TRANSACTION')
        
    def end_transaction(self):
        '''Ending a database transaction.
        '''
        self.connect.commit()
    
    def insert_key_value(self, key, value):
        '''Insert a pair (key, value) in the database.

        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            key:
            value:
        '''
        self._insert_key_value(key, value)
    
    def get_value_by_key(self, key):
        '''Return value relative to key.
        
        Args:
            key:
        
        Return:
            value:
        '''
        return self._get_value_by_key(key)
    
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
    def _insert_key_value_yes_pickle(self, key, value):
        '''(hidden) Insert a pair (key, value) in the database.
            YesPickle
        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            key:
            value:
        '''
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES (?,?)",
                  (key, pickle.dumps(value)))
    
    def _insert_key_value_no_pickle(self, key, value):
        '''(hidden) Insert a pair (key, value) in the database.
            NoPickle        
        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            key:
            value:
        '''
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES (?,?)",
                  (key, value))
    
    def _get_value_by_key_yes_pickle(self, key):
        '''(hidden) Return value relative to key.
            YesPickle
        Args:
            key:
        
        Return:
            value:
        '''
        return pickle.loads(self.connect.execute(f"SELECT {self.value_name} FROM {self.table_name} WHERE {self.key_name}=?",
                                     (key,)).fetchone()[0])
        
    def _get_value_by_key_no_pickle(self, key):
        '''(hidden) Return value relative to key.
            NoPickle
        Args:
            key:
        
        Return:
            value:
        '''
        return self.connect.execute(f"SELECT {self.value_name} FROM {self.table_name} WHERE {self.key_name}=?",
                                     (key,)).fetchone()[0]

    