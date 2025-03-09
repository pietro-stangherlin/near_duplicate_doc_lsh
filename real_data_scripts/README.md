# Description

This folder contains the scripts used for the actual analysis of the robust2004 corpus.
Due to license reason the collection and the related files are not included in the project folder.

All the commands below assume your in the folder above this and that theres a subfodler named "data_near_duplicate" with files and folder as specified in the scripts

1) Adds numerical ids in order to evaluate method.

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.real_add_number_id
```

2) Make difference version of only duplicates of the robust_id2 collection: save them in different subfolders with their metadata file.

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.real_make_collection
```

3) for a fixed set of parameters of shingle and minhash make signatures of just the original collection
    -> saving the result as a sqlite database.
    -> in the same folder save the shingle and minhash parameters used to make the signatures

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_original
```

4) for a fixed set of parameters of shingle and minhash:
    for each different set of clones parameters:
    -> make a subfolder: clone the sqlite database of signatures of the original collection
    and then add to it the signature of the only clones
    -> save the metadata file

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.minhash_duplicates
```

5) Run LSH on all signature databases with original + duplicates

```bash
python -m near_duplicate_doc_lsh.real_data_scripts.lsh_all
```
