import sqlite3
import pickle
import os

# ---------------- SQLite one table database ------------------------#
# This class will be used for storing both signatures and buckets
# (with slightly different specifications).
# NOTE: this has to be changed: I need to generalize it to an arbitrary number
# of columns
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
                            {self.col2_name} {self.col2_type});''')
        
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
    
    # ---------------- SQLite one table database ------------------------#
# This class will be used for storing both signatures and buckets
# (with slightly different specifications).
# NOTE: this is the working in progress version of the more general SQL data structure
class SQLiteOneTableGeneral:
    '''Link to (or create) a sqlite3 database with one table.
    This is used as a general case to create specific databases both for MinHash and LSH
    '''

    def __init__(self,
                 col_names_list: list,
                 col_types_list: list,
                 col_do_pickle_bool_list: list,
                 col_not_null_bool_list: list,
                 col_create_index_bool_list: list,
                 table_name: str = "table_1",
                 database_name: str = "db_name"):
        '''Inizialize the instance creating the database.
        
        Args:
            - col_types_list: list of column types
            - col_names_list: list of column names
            - col_do_pickle_bool_list: list of bool,
                            tell if the values of the specific column
                            should be pickled and unpickled.
                            (pickling has the advantage of saving attributes
                            ,for some supported, python classes)
            - col_not_null_bool_list: list of bool, 
                            tell if the specific column CANNOT have NULL values
            - col_create_index_bool_list: list of bool,
                                        tell if for the specific column an index 
                                        should be created
            - table_name: name of the unique table
            - database_name: name of the database used or to be created
        
        Return:
            None 
        
        Example:
            Assume a database with one table and 3 columns is created,
            first column stores integers
            second column stores text
            third column stores BLOB type and has to be pickled.
            
            Indexes are created on columns 1 and 2.
            Column 1 CANNOT have null values, while columns 2 and 3 can.
            Columns, table, and database name are arbitray.
            
            -> SQLiteOneTableGeneral(col_names_list = ["col1", "col2", "col3"],
                                    col_types_list = ["INTEGER", "TEXT", "BLOB"],
                                    col_do_pickle_bool_list = [False, False, True],
                                    col_create_index_bool_list = [True, True, False],
                                    col_not_null_bool_list = [True, False, False])
        
        NOTE: 
        1) with SQLite Primary key specification is not needed, as deafult primary key 
        the rowid is used (unless specified otherwise), see:
        https://www.sqlite.org/lang_createtable.html#rowid
        '''
        # add the database creation features as attributes of the class
        self.n_col = len(col_names_list)
        
        self.database_name = database_name
        self.table_name = table_name

        self.col_names_list = col_names_list
        self.col_types_list = col_types_list

        self.do_pickle_lst = col_do_pickle_bool_list
        # get indexes for which to pickle
        self.do_pickle_indexes_list = []
        for i in range(self.n_col):
            if col_do_pickle_bool_list[i] == True:
                self.do_pickle_indexes_list.append(i)
        
        
        self.col_not_null_bool_list = col_not_null_bool_list
        self.col_create_index_bool_list = col_create_index_bool_list
        
        
        # convert the col_not_null_bool_list to appropriate strings
        col_not_null_string_list = ["" for i in range(self.n_col)]
        
        # in future some checks can be added
        for i in range(self.n_col):
            if col_not_null_bool_list[i] == True:
                col_not_null_string_list[i] = " NOT NULL"
        
        # create the table creation statement
        db_creation_string = f"CREATE TABLE IF NOT EXISTS {self.table_name}(" # open statement
        
        # all except last column, because last column declaration lacks comma
        for i in range(self.n_col - 1):
            temp_str = col_names_list[i] + " " + col_types_list[i] + col_not_null_string_list[i] + ","
            db_creation_string += temp_str
        
        # last column
        db_creation_string += col_names_list[-1] + " " + col_types_list[-1] + col_not_null_string_list[-1]
        
        db_creation_string += ");" # close statement
        
        # define placeholder string for insertion, on the form (?,?,?)
        # where the number of question marks is equal to the column number
        self.n_question_marks_string = "(" + ",".join(["?" for i in range(self.n_col)]) + ")"
             
        # connect or create database
        self.connect = sqlite3.connect(self.database_name)
        # cursor: used to perform operations
        self.cursor = self.connect.cursor()
        
        # create table if not present
        self.cursor.execute(db_creation_string)
        
        # create indexes for specified columns
        for i in range(self.n_col):
            if col_create_index_bool_list[i] == True:
                self.cursor.execute(f'''CREATE INDEX idx_{col_names_list[i]}
                                ON {table_name} ({col_names_list[i]});''')
        
    
    def begin_transaction(self):
        '''Begin a transaction relative to the database.
        Remember to always end it.
        '''
        self.cursor.execute('BEGIN TRANSACTION')
        
    def end_transaction(self):
        '''Ending a database transaction.
        '''
        self.connect.commit()
    
    def insert_record_values(self,
                      values_list: list):
        '''Insert a record in the database table.

        NOTE:
        the insertion has to be done while in a transaction.
        
        Args:
            - values_list: list of values, in following the columns ordering
        '''
        # first, eventually pickle the marked as pickle column values
        for i in self.do_pickle_indexes_list:
            values_list[i] = pickle.dumps(values_list[i])
        
        self.connect.execute(f"INSERT INTO {self.table_name} VALUES {self.n_question_marks_string}",
                  values_list)

    
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
            Mainly used for debug
        '''
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
    
    