# Simulation Plan

## Save metadata file of parameters (json)

For each different parameters set make a folder with:
    - metadata file with all parameters + names (in order to make the analysis easier)
    - (near duplicates dataset)
    - index with original and copies doc id
    - signature similarity pairs file

### Document collection

1) save the original collection once for all
    For each set of MinHash Parameters
    a) make MinHash data structure and pickle it
        For each set of LSH parameters
        b) make LSH data structurea and pickle it

2) for each set of parameters
    a) make an additional collection with (near) duplicates docs
    b) make the corresponding index to keep track of original doc id + their duplicate doc id

3) Hierachical for MinHash (first) and LSH (after):
 a) unpickle MinHash data structure
    NOTE: for each MinHash we can make different LSH structure by changing different number of bands and buckets
    add the (near duplicates to MinHash data structure)

    For each LSH parameter unpickle LSH data structure:
    b) add the (near) duplicates to the LSH data structure