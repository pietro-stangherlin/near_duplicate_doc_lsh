# make the signature for the duplicates only data
# first try to just one collection
# then try to make a for cycle

from near_duplicate_doc_lsh.project.src import hashing
from near_duplicate_doc_lsh.project.src import macro
from near_duplicate_doc_lsh.real_data_scripts import real_minhash_params as rmp

import shutil # to copy the signature_db in subfolder
import os
import csv
import json
import time

# TO DO