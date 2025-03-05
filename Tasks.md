# Creation of the new collection

## Map - Reduce implementation (TO - DO)

## General - TO DO

- Use unsigned numpy.integer instead of signed integer
- Create a toy dataset to be used in tests
- assume all dataset to be json

### Rolling Hashing Shingles - TO DO

Implement a function for rolling hashing shingling (could be useful for large documents)

## Implemenentation of LSH

## LSH band hash function or functions - TO DO 

Given a signature as numpy array of 32 or 64 unsigned integers,
the number of bands (which is a perfect divisor of the length of the signature)
define a hash function to produce the hash for each bands of buckets.

### Problem is to turn a sub-array to an integer.

Example: original signature: s = [1, 1, 2, 1, 5, 3], the goal is to compute an hash
for sub-arrays [1, 1], [2, 1] and [5, 3] (assuming 3 bands), the hidden problem here is to avoid (if necessary) overflow of operations.

### Problem: depence from LSH data structure used

Of course the hash function depends on the implementation of LSH data structure

### Problem: different of equals hash functions for each band?

## LSH buckets data structure - TO DO

Choose a way to implement the LSH band with buckets.
One option is to just use a list or array of m bucktes for each band.
Here some considerations depends on the nature of documents ids (their type in terms of occupied memory).
Options:

- main memory storage -> half done: btree data structure
- disk storage (database) -> TO - DO: the SQL schema has to be defined or evaluate a graph database

### Sudden Similiary approach

One option is to compute the similarities suddenly after having found the bucket (for each document). The problem with this approach is that for some documents we get incomplete information.
Example:

1. at iteration j - 1 one bucket is [1, 15, 23] (where each element is a document id)
2. at iteration j one the document 57 is hashed to that bucket so [1, 15, 23, 57]
and we compute the similarity of 57 with 1, 15 and 23.
3. at some next iteration j + l the bucket has elements [1, 15, 23, 57, 89, 101],
clearly if we're interested in the documents similar to 57 we need to scan all the others, because the set 57 -> {1, 15, 23} is not complete.

### Problem: duplicates and redundancy

- duplicates: do we care having duplicates?
like from one band we get: 57 -> {1, 15, 23}
from another band we get 57 -> {1, 46} and so on...
- redundancy: do we care about redundancy?
Example:
1 -> {15, 23, 57}
23 -> {1, 15, 57}
57 -> {1, 15, 23}

We can try to solve this with a graph database keeping all the documents as nodes and similarities as weighted edges, where a missing node is considered as a zero similarity.
We need to investigate it further.

### Select only documets which share a minimum number of buckets - TO DO
