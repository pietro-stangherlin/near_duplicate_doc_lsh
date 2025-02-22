# to do

# for a fixed set of parameters

# assuming: two files in input:
# 1) 2 columns: pairs (first two columns) of true near duplicated documents id
# 2) 3 columns: pairs (first two columns) of documents id and (third column) computed signature similarity

# goals: compute
# - true positive
# - false negative
# - precision
# - recall

# maybe using a roc curve (using the signature similarity as score)

# in a more generale script: 
# choose some sumary statistics and plot them against the change of some of the parameters
# NOTE: it should be smart to automize all the analysis

# NOTE: I also need another analysis relative to the time used,
# even though is less important beacause it's sufficient to measure 
# how the different implementation scale
