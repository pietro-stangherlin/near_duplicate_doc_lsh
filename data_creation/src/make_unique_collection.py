import pandas as pd
import json
import sys


# remove all duplicates documents from robust_id2
# saving a new collection
# > python -m near_duplicate_doc_lsh.data_creation.src.make_unique_collection index_csv_fin collection_fin collection_fout


# used
# index_csv_fin = "data_near_duplicate\\robust\\original_index.csv"
# collection_fin = "data_near_duplicate\\robust\\robust_id2.json"
# collection_fout = "data_near_duplicate\\robust\\robust_id2_uniques.json"


if __name__ == "__main__":
    
    # argument order
    index_csv_fin = sys.argv[1]
    collection_fin = sys.argv[2]
    collection_fout = sys.argv[3]
    
    df = pd.read_csv(index_csv_fin)
    
    # Extract all duplicate id2 values from the CSV
    duplicate_id2_set = set(df['doc1.1'])
    

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

