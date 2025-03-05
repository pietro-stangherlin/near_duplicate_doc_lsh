# Description

This folder contains the scripts used for the actual analysis of the robust2004 corpus.
Due to license reason the collection and the related files are not included in the project folder.

1) execute: "real_add_number_id.py" from external project folder: this just
    adds numerical ids in order to evaluate method.

2) Make difference version of only duplicates of the robust_id2 collection:
    save them in different subfolders with their metadata file

3) for a fixed set of parameters of shingle and minhash make signatures of just the original collection
    -> saving the result as a sqlite database.
    -> in the same folder save the shingle and minhash parameters used to make the signatures

4) for a fixed set of parameters of shingle and minhash:
    for each different set of clones parameters:
    -> make a subfolder: clone the sqlite database of signatures of the original collection
    and then add to it the signature of the only clones
    -> save the metadata file
