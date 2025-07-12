# Real data scripts

## Short Instructions

### Arxiv

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files --collection arxiv
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_original --collection arxiv
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates --collection arxiv
python -m near_duplicate_doc_lsh.real_data_scripts.lsh_all --collection arxiv
```

### Robust

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files --collection robust
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_original --collection robust
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates --collection robust
python -m near_duplicate_doc_lsh.real_data_scripts.lsh_all --collection robust
```

## Description

This folder contains the scripts used for the actual analysis of the robust2004 corpus.
Due to license reason the collection and the related files are not included in the project folder.

All the commands below assume your in the folder above this and that theres a subfodler named "data_near_duplicate" with files and folder as specified in the scripts

From command line:

```bash
python -m near_duplicate_doc_lsh.data_creation.src.add_num_ids .\\data_near_duplicate\\robust\\tipster_45_all_docs.json .\\data_near_duplicate\\robust\\robust_id2.json id2
```

1) For robust we also initially remove documents original duplicates or near duplicates
found with our methodology in order to have more interpretable results.
So after the steps described:

a) lunch our lsh on original dataset
b) get and index of much similar documents
c) use this index to remove duplicates from the collection
d) recompute the id_2

Assuming we have an index of really similar documents which we call `original_index`.

```bash
python -m near_duplicate_doc_lsh.data_creation.src.make_unique_collection data_near_duplicate\\robust\\original_index.csv data_near_duplicate\\robust\\robust_id2.json data_near_duplicate\\robust\\robust_id2_uniques.json
```

This will produce the file `robust_id2_uniques.json.`
On which we recompute the id_2 by (first argument: input, second output, third new_id_name)

```bash
python -m near_duplicate_doc_lsh.data_creation.src.add_num_ids .\\data_near_duplicate\\robust\\robust_id2_uniques.json .\\data_near_duplicate\\robust\\robust_id2_ready.json id2
```

With final outpyt file `robust_id2_ready.json` that will be used from now on.

2) Make difference version of only duplicates of the robust_id2 collection and save them in different subfolders with their metadata file.
Description: some rows (documents) are copied (eventually some noise is added, based on parameters) and these new collection are saved (with sequential id2 values).

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.real_make_collection
```

3) Make paramater files for both minhash and LSH.
The script will read some parameters from the `parameters.py` file and populate the folders `minhash_parameters` and `lsh_parameters`. The next steps will iterate on each parameter file in those folders.

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.make_params_files
```

4) for a fixed set of parameters of shingle and minhash make signatures of just the original collection
    -> saving the result as a sqlite database.
    -> in the same folder save the shingle and minhash parameters used to make the signatures

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_original
```

5) for a fixed set of parameters of shingle and minhash:
    for each different set of clones parameters:
    -> make a subfolder: clone the sqlite database of signatures of the original collection
    and then add to it the signature of the only clones
    -> save the metadata file

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates
```

6) Run LSH on all signature databases with original + duplicates

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.lsh_all
```
