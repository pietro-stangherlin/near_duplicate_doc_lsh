import pandas as pd
import matplotlib.pyplot as plt

# important: execute the script from external directory
# so the data folder (not included in the near_duplicate_doc_lsh) is a subdirectory
# also before running convert the file to utf-8 and remove BOM 
# (from notepad++ encoding, or another way)

# If data is in test_data: (use this in testing)
# >>> python -m data_analysis.analysis_funs

# if data is in external folder:
# >>> python -m near_duplicate_doc_lsh.data_analysis.analysis_funs

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
# - precision
# - recall


# in a more general script: 
# choose some summary statistics and plot them against the change of some of the parameters
# NOTE: it's wise to automatize all the analysis

# NOTE: I also need another analysis relative to the time used,
# even though is less important because it's sufficient to measure 
# how the different implementations scale
# and also it varies across different hardware 

def ListSubfolders(folder_path):
    # Use os.walk to iterate through the directory
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders

def MakeReverseDictionary(signature_sim_df: pd.DataFrame,
                          doc1_id_name: str = "doc1_id",
                          doc2_id_name: str = "doc2_id",
                          signature_similarity_name: str = "signature_similarity",
                          shared_buckets_number_name: str = "shared_buckets_number"):
    '''
    Make dictionary with tuples of the first two columns as keys and the third column as values (float)
    
    Args:
        - signature_sim_df (pd.DataFrame): data frame with 
        - doc1_id_name (str): column name id of first document
        - doc2_id_name (str): column name id of second document
        - signature_similarity_name (str): column name of signature similarity measure
    Return:
        - reverse dictionary (dict) with
        key : signature similarity, value : (doc1_id, doc2_id, shared_bucket_number)
    '''
    signature_similarity_reverse_dict = {}
    
    for _, row in signature_sim_df.iterrows():
        sig_sim = row[signature_similarity_name]
        value = (int(row[doc1_id_name]), int(row[doc2_id_name]))
        if sig_sim not in signature_similarity_reverse_dict:
            signature_similarity_reverse_dict[sig_sim] = set()
        signature_similarity_reverse_dict[sig_sim].add(value)
    
    return signature_similarity_reverse_dict



# naive implementation
def RetrievedSetFixedSignatureSimilarityThreshold(signature_sim_reverse_dict: dict,
                                                  signature_sim_threshold: float) -> set:
    '''
    Return a set of all tuples with signature similarity
    greater than or equal than the specified signature similarity threshold
    
    Args: 
        - signature_sim_reverse_dict (dictionary): dictionary with key = signature similarity (float)
        value = set of tuples of docs with that signature similarity
        - signature_sim_threshold (float): signature similarity threshold to consider 
    Return: 
        - set (set) of tuples of (doc1_id, doc2_id) for which the signature similarity is greater 
        than the specified threshold 
    '''
    greater_than_threshold_set = set()
    
    for signature_sim in signature_sim_reverse_dict:
        if signature_sim >= signature_sim_threshold:
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

def Precision(true_duplicates_and_retrieved_count: int,
              retrieved_count: int) -> float:
    '''Return Precision = # (true_duplicates Intersection retrieved) / # retrieved
    
    Args:
        - true_duplicates_and_retrieved_count (int) : cardinality of the intersection 
            between true duplicates and retrieved documents
        - retrieved_count (int): cardinality of retrieved documents
    
    Return:
        - Precision (float)
    '''
    return (true_duplicates_and_retrieved_count / retrieved_count)

def Recall(true_duplicates_and_retrieved_count: int,
           true_duplicates_count: int) -> float:
    '''Return Recall = # (true_duplicates Intersection retrieved) / # true_duplicates

    Args:
        - true_duplicates_and_retrieved_count (int) : cardinality of the intersection 
            between true duplicates and retrieved documents
        - true_duplicates_count (int): cardinality true duplicates documents
    
    Return:
        - Recall (float)
    '''
    return (true_duplicates_and_retrieved_count / true_duplicates_count)

def ComputePrecisionRecallVsSignatureSimilarity(true_duplicates_tuples_set: set,
                                                 signature_similarity_reverse_dict: set) -> pd.DataFrame:
    '''
    Args: 
        - true_duplicate_set (set) : set of tuples of the true (near) duplicates documents
        - signature_sim_reverse_dict (dictionary): dictionary with key = signature similarity (float)
        value = set of tuples of docs with that signature similarity
    Return: 
        - pandas data frame (pd.DataFrame): with columns
        "sorted_signature_similarities", "precision", "recall"
    '''
    
    sorted_signature_similarities = sorted(signature_similarity_reverse_dict.keys())
    
    # allocate metrics_df
    metrics_df = pd.DataFrame({
        "sorted_signature_similarities": sorted(signature_similarity_reverse_dict.keys()),
        "precision": [None for i in range(len(signature_similarity_reverse_dict))],
        "recall": [None for i in range(len(signature_similarity_reverse_dict))]
    })

    # temp lists
    true_duplicates_intersection_retrieved_count_list = [None for i in range(len(signature_similarity_reverse_dict))]
    retrieved_count_list = [None for i in range(len(signature_similarity_reverse_dict))]

    # populate metrics_df
    for i in range(len(sorted_signature_similarities)):
    
        temp_retrieved_set = RetrievedSetFixedSignatureSimilarityThreshold(signature_sim_reverse_dict = signature_similarity_reverse_dict,
                                                                  signature_sim_threshold = sorted_signature_similarities[i])
    
        true_duplicates_intersection_retrieved_count_list[i] = TrueDuplicatesAndRetrievedCount(true_duplicate_set = true_duplicates_tuples_set,
                                                                                               retrieved_set = temp_retrieved_set)
        retrieved_count_list[i] = len(temp_retrieved_set)
    
        metrics_df.loc[i, "precision"] = Precision(true_duplicates_and_retrieved_count = true_duplicates_intersection_retrieved_count_list[i],
                                  retrieved_count = retrieved_count_list[i])
    
        metrics_df.loc[i, "recall"] = Recall(true_duplicates_and_retrieved_count = true_duplicates_intersection_retrieved_count_list[i],
                            true_duplicates_count = len(true_duplicates_tuples_set))
        
    return(metrics_df)


def PlotPrecisionRecallVsSignatureSimilarity(my_metrics_df: pd.DataFrame,
                                                 my_title: str = "Precision and Recall Vs Signature Similarity",
                                                 show_plot_bool: bool = True,
                                                 save_plot_bool: bool = False,
                                                 save_plot_path: str = "plot_precision_recall_vs_signature_sim.jpg") -> None:
    '''
    Args:
        - my_metrics_df (pd.DataFrame)
        - my_title (str): plot title
        - show_plot_bool (bool): if True show the plot
        - save_plot_bool (bool): if True save the plot on disk
        - save_plot_path (str): path where the plot is saved
    
    Return:
        - None
    '''
        
    plt.plot(my_metrics_df["sorted_signature_similarities"], my_metrics_df["precision"],
         color = "blue", linestyle = "-", marker = "o",
         label = "Precision")

    plt.plot(my_metrics_df["sorted_signature_similarities"], my_metrics_df["recall"],
         color = "red", linestyle = "-", marker = "o",
         label = "Recall")

    plt.title(my_title)
    plt.xlabel("Signature Similarity Threshold")
    plt.ylabel("Metrics")

    plt.legend()

    if show_plot_bool:
        plt.show()
    
    if save_plot_bool:
        plt.savefig(save_plot_path)


if __name__ == "__main__":
    # Read the true near duplicated documents file
    true_duplicates_df = pd.read_csv('test_data\\arxiv_duplicates\\arxiv_clones_1000_index.csv')
    # extract tuples 
    true_duplicates_tuples_set = set(tuple(row) for row in true_duplicates_df.itertuples(index = False, name = None))

    # read the documents with computed signature similarity file
    signature_sim_df = pd.read_csv('test_data\\arxiv_duplicates\\sig_config1\\lsh1\\arxiv_clones_first_1000_signature_sim.csv')
    
    signature_similarity_reverse_dict = MakeReverseDictionary(signature_sim_df = signature_sim_df)
    
    t = ComputePrecisionRecallVsSignatureSimilarity(true_duplicates_tuples_set = true_duplicates_tuples_set,
                                             signature_similarity_reverse_dict = signature_similarity_reverse_dict)
    
    print(t)
    
    PlotPrecisionRecallVsSignatureSimilarity(my_metrics_df = t)
    


