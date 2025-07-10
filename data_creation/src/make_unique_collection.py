import pandas as pd
import json
import sys


# remove all duplicates documents from robust_id2
# saving a new collection
# > python -m near_duplicate_doc_lsh.data_creation.src.make_unique_collection index_csv_fin collection_fin collection_fout


def ToListofPairSets(sig_sim_file_name,
                     threshold = 0.8,
                     signature_similarity_field_name = "signature_similarity",
                     shared_buckets_number_name = "shared_buckets_number"):
    sig_sim_pd = pd.read_csv(sig_sim_file_name)
    
    filtered_df = sig_sim_pd[sig_sim_pd[signature_similarity_field_name] >= threshold]
    
    filtered_df.drop(columns = [signature_similarity_field_name,
                                shared_buckets_number_name],
                                inplace = True)
    
    return [set(el) for el in filtered_df.values.tolist()]

def CommonElementsOneSetUnion(input_list_of_sets):
    '''
    Merge sets if they have one element in common, do this operation just once
    Return a list with two elements: 
    first element is the resulting list of sets
    second element is a boolean equals True if at least one common element was found
    '''
    out_list = list()
    to_keep_indexes = set([i for i in range(0, len(input_list_of_sets))])

    bool_at_least_one_not_empty_intersection = False

    while(len(to_keep_indexes) > 0):
        reference_index = min(to_keep_indexes)
        reference_set = input_list_of_sets[reference_index]

        to_keep_indexes.remove(reference_index)
        to_remove_indexes = set()

        for i in to_keep_indexes:
            if(len(reference_set.intersection(input_list_of_sets[i])) > 0):
                    reference_set = reference_set.union(input_list_of_sets[i])
                    to_remove_indexes.add(i)

                    bool_at_least_one_not_empty_intersection = True
        
        out_list.append(reference_set)
        to_keep_indexes = to_keep_indexes.difference(to_remove_indexes)
    
    return([out_list, bool_at_least_one_not_empty_intersection])


def MakeRelationSetsList(in_pairs_list):
    '''
    given a list with elements
   [{"a", "b"}, {"a", "c"}, {"c", "d"},{"e", "f"}, {"f", "g"}]
   
   return a list of sets
   where each sets contains all the elements for which pairs share at least one element
   in the example
   [{"a", "b", "c", "d"},{"e", "f", "g"}]


   the algorithm is iterative:
   1) for each set: fix it and for each other set
   if their intersection is not empty replace the fixed set with the union of the two of them
   and delete the non fixed one
   2) repeat until all intersections are empty or just one set is left
  
   '''
    new_list_with_sets = list()

    condition = True

    while(condition):
        res = CommonElementsOneSetUnion(in_pairs_list)
        new_list_with_sets = res[0]

        if((len(new_list_with_sets) == 1) or (res[1] == False)):
             condition = False
        
        in_pairs_list = new_list_with_sets
    
    return new_list_with_sets


def RemoveOneFromAll(list_of_sets):
     '''For each set in the list remove one element
     Return the list of set modified this way
     '''
     returned_list = list_of_sets

     for el in returned_list:
          el.remove(min(el))
        
     return  returned_list

def UnionAll(list_of_sets):
     res_union = set()

     for el in list_of_sets:
          res_union = res_union.union(el)
        
     return res_union

# used

# ROBUST
# index_csv_fin = "data_near_duplicate\\robust\\original_index.csv"
# collection_fin = "data_near_duplicate\\robust\\robust.json"
# collection_fout = "data_near_duplicate\\robust\\robust_id2_uniques.json"

# > python -m near_duplicate_doc_lsh.data_creation.src.make_unique_collection data_near_duplicate\\robust\\original_index.csv data_near_duplicate\\robust\\robust.json data_near_duplicate\\robust\\robust_id2_uniques.json


# ARXIV
# index_csv_fin = "data_near_duplicate\\arxiv\\original_index.csv"
# collection_fin = "data_near_duplicate\\arxiv\\arxiv_reduced.json"
# collection_fout = "data_near_duplicate\\arxiv\\arxiv_id2_to_number.json"

# > python -m near_duplicate_doc_lsh.data_creation.src.make_unique_collection data_near_duplicate\\arxiv\\original_index.csv data_near_duplicate\\arxiv\\arxiv_reduced.json data_near_duplicate\\arxiv\\arxiv_id2_to_number.json

if __name__ == "__main__":
    
    # argument order
    index_csv_fin = sys.argv[1]
    collection_fin = sys.argv[2]
    collection_fout = sys.argv[3]
    
    df = pd.read_csv(index_csv_fin)
    
    # Extract all duplicate id2 values from the CSV
    duplicate_id2_set = UnionAll(RemoveOneFromAll(MakeRelationSetsList(ToListofPairSets(sig_sim_file_name = index_csv_fin,
                                                                                        threshold = 0.8,
                                                                                        signature_similarity_field_name = "signature_similarity",
                                                                                        shared_buckets_number_name = "shared_buckets_number"))))
    

    with open(collection_fout, 'w') as outfile:
        with open(collection_fin, 'r') as infile:
            # Read and filter JSON objects
            for line in infile:
                document = json.loads(line.strip())
                doc_id2 = document["id2"]

                # Check if this id2 is in the duplicate set
                if doc_id2 not in duplicate_id2_set:
                    outfile.write(json.dumps(document) + "\n")

    print(f"[INFO] Filtered JSON written to {collection_fout}")

