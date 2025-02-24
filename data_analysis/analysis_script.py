import pandas as pd
import matplotlib.pyplot as plt

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
# NOTE: it's wise to automatize all the analysis

# NOTE: I also need another analysis relative to the time used,
# even though is less important beacause it's sufficient to measure 
# how the different implementations scale

# Read the true near duplicated documents file
true_duplicates_df = pd.read_csv('test_data\\arxiv_clones_first_1000_index.csv')

# print(true_duplicates_df)

# extract tuples 
true_duplicates_tuples_set = set(tuple(row) for row in true_duplicates_df.itertuples(index=False, name=None))

print(true_duplicates_tuples_set)


# Read the documents with computed signature similarity file
signature_sim_df = pd.read_csv('test_data\\arxiv_clones_first_1000_signature_sim.csv')

# print(signature_sim_df)

# Create dictionary with tuples of the first two columns as keys and the third column as values
signature_sim_dict = {(int(row['doc1_id']), int(row['doc2_id'])): row['signature_similarity'] for _, row in signature_sim_df.iterrows()}

# print(signature_sim_dict)

# inverted index signature similarity
# key : signature similarity
# value : set of doc ids tuples 

# make reverse dictionary
signature_similarity_reverse_dict = {}
for key, value in signature_sim_dict.items():
    if value not in signature_similarity_reverse_dict:
        signature_similarity_reverse_dict[value] = set()
    signature_similarity_reverse_dict[value].add(key)

print(signature_similarity_reverse_dict)

# define metrics
# for a fixed signature similarity threshold


def RetrievedSetFixedSignatureSimilarityThreshold(signature_sim_reverse_dict: dict,
                                                  signature_sim_threshold: float) -> set:
    '''
    Return a set of all tuples with signature similarity
    greater than or equal the specified signature similarity threshold
    
    Args: 
        - signature_sim_reverse_dict (dictionary): dictionary with key = signature similarity (float)
        value = set of tuples of docs with that signature similarity
        - signature_sim_threshold (float): signature similarity threshold to consider 
    Return: 
        - set (set) of tuples of documents id for which the signature similarity is greater 
        than the specified threshold 
    '''
    greater_than_threshold_set = set()
    
    for signature_sim in signature_sim_reverse_dict:
        if signature_sim_dict >= signature_sim_threshold:
            greater_than_threshold_set = greater_than_threshold_set.union(signature_sim_reverse_dict[signature_sim])

    return greater_than_threshold_set

def TrueDuplicatesAndRetrievedCount(true_duplicate_set: set,
                                    retrieved_set: set) -> int:
    '''Return the count of the set given by the instersection of the two 
    argument sets.
    
    Args:
        - true_duplicate_set (set) : set of tuples of the true (near) duplicates documents
        - retrieved_set (set) :  set of tuples of the retrieved set (usualy for a fixed threshold)
    Return:
        - cardinality of the intersection (int)
    '''
    return len(true_duplicate_set.intersection(retrieved_set))

def Precision(true_duplicate_set: set,
              signature_sim_reverse_dict: dict,
              signature_sim_threshold: float) -> float:
    '''Return Precision = #(true_duplicates Intersection retrieved) / #retrieved
    where retrieved is the set of tuples of pairs with a signature similarity greater than
     signature_sim_threshold
    
    Args:
        - true_duplicate_set (set) : set of tuples of the true (near) duplicates documents
        - signature_sim_reverse_dict (dictionary): dictionary with key = signature similarity (float)
        value = set of tuples of docs with that signature similarity
        - signature_sim_threshold (float): signature similarity threshold to consider
    
    Return:
        - Precision (float)
    '''
    pass 

def Recall(true_duplicate_set: set,
            signature_sim_reverse_dict: dict,
            signature_sim_threshold: float) -> float:
    pass






