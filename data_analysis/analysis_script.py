# TO DO

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# also before running convert the file to utf-8 and remove BOM 
# (from notepad++ encoding, or another way)

# If data is in test_data: (use this in testing)
# >>> python -m data_analysis.analysis_script

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.data_analysis.analysis_script

# for a fixed set of parameters
# NOTE: the two files should have the same header names for the first two columns

# assuming: two files (1 and 2) in input:
# 1) 2 columns: pairs (first two columns) of true near duplicated documents id
# example (header + first rows):
# doc1_id,doc2_id
# 1,1000
# 6,1001
# 12,1002

# 2) 3 columns: pairs (first two columns) of documents id and (third column) computed signature similarity
# example (header + first rows):
# doc1_id,doc2_id,signature_sim
# 4,1000,1.0
# 6,1008,0.5
# 12,1002,0.8

# goals: compute
# - true positive
# - false negative
# - precision
# - recall

# x axis: threshold for signature similarity value
# y axis: metric (maybe use just one plot with four lines and different colours)

# in a more generale script: 
# choose some sumary statistics and plot them against the change of some of the parameters
# NOTE: it's wise to automize all the analysis

# NOTE: I also need another analysis relative to the time used,
# even though is less important beacause it's sufficient to measure 
# how the different implementation scale

import pandas as pd

import matplotlib.pyplot as plt

# Read the true near duplicated documents file
true_duplicates = pd.read_csv('test_data\\arxiv_clones_first_1000_index.csv')

print(true_duplicates)

# Read the documents with computed signature similarity file
signature_sim = pd.read_csv('test_data\\arxiv_clones_first_1000_signature_sim.csv')

print(signature_sim)



