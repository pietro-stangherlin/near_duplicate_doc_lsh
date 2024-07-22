# Instructions (for myself) to use the make_collection.py script

0. Activate the virtual environment with all the needed modules
1. Copy and change one of the dictionary in make_col_params.py with the intended parameters
(when specifing the path assume you are in the directory from where you're launching the command)
2. Place yourself outside the near_duplicate_doc_lsh directory,
make a python script with:

```python
from ..src import make_collection as mc
from ..src import make_col_params as pm
# import random

# replicability only
# random.seed(123)

mc.WriteRandomLines(**pm.name_of_newly_created_params_dict)
```

3. From PowerShell: 
```python -m near_duplicate_doc_lsh.data_creation.tests.test_make_collection```