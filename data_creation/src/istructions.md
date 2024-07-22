
# Data Creation Instructions
Assume there's a document collection json like with, ate least one id and one content fields.

Example: file_toy.json
```json
{"id" = "aab6": "content": "the apple is green"},
{"id" = "ahb8": "content": "eternal sunshine"},
{"id" = "hrr93": "content": "dust in the wind"}
```

In order to create a new file of desired format:
1) run add_sum_ids.py on the starting file to create a new file adding a new id based on the each new number
2) run make_collection.py on the file created at point 1


**IMPORTANT**: the console examples assume you're in the folder external to near_duplicate_doc_lsh
-> example:

﻿/dir1
|-- near_duplicate_doc_lsh
|-- data_folder


## 1. Instructions to use add_sum_ids.py

### Command line 
Parameters: file_in_name, file_out_name, original_id_name, new_id_name.
From command line: python 
```python .\near_duplicate_doc_lsh\data_creation\src\add_num_ids.py .\Data_Creation\file_in_name.json file_out_name new_id_name ```


Robust specific example.
From command line:
```python .\near_duplicate_doc_lsh\data_creation\src\add_num_ids.py .\Data_Creation\tipster_45_all_docs.json robust_2.json id id2 ```

### Result example 

Input file:
```json
{"id" = "aab6": "content": "the apple is green"},
{"id" = "ahb8": "content": "eternal sunshine"},
{"id" = "hrr93": "content": "dust in the wind"}
```

Output file:
```json
{"id" = "aab6": "content": "the apple is green", "id2" = "1"},
{"id" = "ahb8": "content": "eternal sunshine", "id2" = "2"},
{"id" = "hrr93": "content": "dust in the wind", "id2" = "3"}
```

## 2. Instructions to use make_collection.py

1. Copy and change one of the dictionary in make_col_params.py with the intended parameters
2. Place yourself outside the near_duplicate_doc_lsh directory,
make a python script with:

```python
from ..src import make_collection as mc
from ..src import make_col_params as pm

# replicability only
# import random
# random.seed(123)

mc.WriteRandomLines(**pm.name_of_newly_created_params_dict)
```

Example: ``` mc.WriteRandomLines(**pm.first_100_dict_params_no_original) ```

3. From PowerShell:
Exectute the script as a module.

Example (because in the tests folder there's indeed such a script)
```python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection```