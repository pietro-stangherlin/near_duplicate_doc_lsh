# Creation of the new collection

# Implementation of shingles
Remember to delete each shingles set after it has been used to generate its signature.

# Implementation of Minhash

## Family of row permutation hash functions
Choose an appropriate familty of row permutation hash functions.
The idea is to use a familty of hash function which hash depends upon one or more parameters,
so changing the parameter will generate a different hash function.
We need a different hash function for each signature element.
Attetion is needed in not chosing hash functions that behave nearly the same with 
different parameters. 

## Storage of Signature Matrix
Options are
1. not store it: from a shingle generate the signature matrix, from it fill the LSH bands
and then delete both the shingle and the signature
2. store it in working memory in a btree with a library (https://pypi.org/project/BTrees/) aid
3. store it in mass memory (sql)
4. both 2 and 3


# Implemenentation of LSH
