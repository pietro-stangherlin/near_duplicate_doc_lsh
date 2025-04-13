import pandas as pd
import matplotlib.pyplot as plt
import os

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

# -> memory profiling
# NOTE: I also need another analysis relative to the time used,
# even though is less important because it's sufficient to measure 
# how the different implementations scale
# and also it varies across different hardware 

def ListSubfolders(folder_path):
    # Use os.walk to iterate through the directory
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders


def ConvertTrueIndexPdToTupleSet(true_duplicates_index_pd: pd.DataFrame) -> set:
    return(set(tuple(row) for row in true_duplicates_index_pd.itertuples(index = False, name = None)))

def AddPairColumnDropSingleOnes(df: pd.DataFrame,
                  doc1_id_col_name: str = "doc1",
                  doc2_id_col_name: str = "doc2",
                  pair_col_name: str = "pair"):
    
    # do all inplace
    df[pair_col_name] = list(zip(df[doc1_id_col_name], df[doc2_id_col_name]))
    df[pair_col_name] = df[pair_col_name].apply(lambda x: tuple(sorted(x)))

    df.drop(columns = [doc1_id_col_name, doc2_id_col_name], inplace = True)

def SortDfByColumn(lsh_result_df: pd.DataFrame,
                   sorting_column_name: str):
    pass

def PrecisionRecallVsSelectedMetric(lsh_results_pd: pd.DataFrame,
                                    true_duplicates_tuple_set: set,
                                    selected_metric_col_name: str,
                                    pair_col_name: str = "pair",
                                    precision_name: str = "precision",
                                    recall_name: str = "recall") -> pd.DataFrame:
    
    '''Given a (pandas) dataframe with lsh results and a set of true duplicates tuples
    return a (pandas) dataframe with columns: ascending order selected metrics, recall and precision based
    on that metric threshold

    Args:
        - lsh_results_pd (pandas DataFrame): dataframe with at least two columns, 
            one of documents id pairs sorted tuples (ex. (doc1_id, doc2_id) with doc1_id < doc2_ids)
            and the other column of signature similarities
        - true_duplicates_tuple_set (set): set of tuple of true duplicates document ids
        - selected_metric_col_name (str): name of selected metric column used in both
          input and returned dataframes
        - pair_col_name (str): name of tuples column
        - precision_name (str): name of precision column in the returned dataframe
        - recall_name (str): name of recall column in the returned dataframe

    Return:
        - dataframe (pandas dataframe): with columns ascending order selected metrics, recall and precision based
            on that metric threshold
    '''
    # lsh_results_pd.sort_values(by = selected_metric_col_name, inplace = True)

    # sort twice in order to be sure
    unique_sorted_metric_values = sorted(lsh_results_pd[selected_metric_col_name].unique())
    n_thresholds = len(unique_sorted_metric_values)

    precision = [None for i in range(n_thresholds)]
    recall = [None for i in range(n_thresholds)]

    len_true_duplicates = len(true_duplicates_tuple_set)

    # NOTE: optimize if it gets slow
    # (i.e. sort the df by metric once and then cycle on the sorted dataframe)
    for i in range(len(unique_sorted_metric_values)):
        filtered_df = lsh_results_pd[lsh_results_pd[selected_metric_col_name] >= unique_sorted_metric_values[i]]
        filtered_tuples_set = set(filtered_df[pair_col_name])

        true_positive_count = TrueDuplicatesAndRetrievedCount(true_duplicate_set = true_duplicates_tuple_set,
                                                        retrieved_set = filtered_tuples_set)
        
        precision[i] = Precision(true_duplicates_and_retrieved_count = true_positive_count,
                                 retrieved_count = len(filtered_tuples_set))
        
        recall[i] = Recall(true_duplicates_and_retrieved_count = true_positive_count,
                           true_duplicates_count = len_true_duplicates)
    
    # save a pd. dataframe
    returned_df = pd.DataFrame()
    returned_df[selected_metric_col_name] = unique_sorted_metric_values
    returned_df[precision_name] = precision
    returned_df[recall_name] = recall

    return(returned_df)


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
    return (true_duplicates_and_retrieved_count / retrieved_count if retrieved_count > 0 else 0)

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
    return (true_duplicates_and_retrieved_count / true_duplicates_count if true_duplicates_count > 0 else 0)



def PlotPrecisionRecallVsSelectedMetric(my_metrics_df: pd.DataFrame,
                                        recall_col_name: str = "recall",
                                        precision_col_name: str = "precision",
                                        metric_col_name: str = "signature_similarity",
                                        my_title: str = "Precision and Recall Vs Metrics",
                                        x_label: str = "Signature Similarity",
                                        y_label: str = "Metric Values",
                                        show_plot_bool: bool = True,
                                        save_plot_bool: bool = False,
                                        save_plot_path: str = "plot_precision_recall_vs_metric.jpg") -> None:
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
        
    plt.plot(my_metrics_df[metric_col_name], my_metrics_df[precision_col_name],
         color = "blue", linestyle = "-", marker = "o",
         label = "Precision")

    plt.plot(my_metrics_df[metric_col_name], my_metrics_df[recall_col_name],
         color = "red", linestyle = "-", marker = "o",
         label = "Recall")

    plt.title(my_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.legend()

    if show_plot_bool:
        plt.show()
    
    if save_plot_bool:
        plt.savefig(save_plot_path)


if __name__ == "__main__":
    # Read the true near duplicated documents file
    true_duplicates_df = pd.read_csv('test_data\\arxiv_duplicates\\arxiv_clones_1000_index.csv')
    # extract tuples 
    true_duplicates_tuples_set = ConvertTrueIndexPdToTupleSet(true_duplicates_df)

    # read the documents with computed signature similarity file
    signature_sim_df = pd.read_csv('test_data\\arxiv_duplicates\\sig_config1\\lsh1\\arxiv_clones_first_1000_signature_sim.csv')
    
    # add tuples column and drop others
    AddPairColumnDropSingleOnes(df = signature_sim_df,
                                doc1_id_col_name = "doc1_id",
                                doc2_id_col_name = "doc2_id",
                                pair_col_name = "pair")

    
    t = PrecisionRecallVsSelectedMetric(lsh_results_pd = signature_sim_df,
                                        true_duplicates_tuple_set = true_duplicates_tuples_set,
                                        selected_metric_col_name = "signature_similarity",
                                        pair_col_name = "pair")
    
    print(t)
    
    PlotPrecisionRecallVsSelectedMetric(my_metrics_df = t,
                                        metric_col_name = "signature_similarity")
    


