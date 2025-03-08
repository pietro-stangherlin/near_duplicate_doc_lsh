# Complexity Analysis
Below are given some complexity analysis of the methods used.

## Shingling
Assume the text to be shingled has n characters and each shingle has length w.

### Time complexity
Both versions of TextToShingles have a time complexity linear in n.
### Space complexity
The space occupied by the Array version could be precisley computed: it is equal to (n - w + 1) * w times the memory occupied by type of int chosen. The set version occupied space depends on the number of equal shingles (the more they are the less space occupied) and by the empty space allocated by the set class.  

## MinHash
Assume there are n documents and the signature has k elements.
In theory it's possible to store the pairs (id_doc, signature) in a dictionary (hash table) allowing O(1) query time; the problem is in order to have few collisions a large empty chunk of memory has to be allocated, which, unless there's plenty of free main memory we don't have, for this reason it's not implemented.

### BTree main memory
Avaible only if there's enough free main memory.
Space complexity O(n), query complexity O(log(n)).

### SQL Table(id_doc, signature)
The signature is a numpy array which has to stored as BLOB after pickling.
An BTree index is created on id_doc (which is the primary key) allowing a query time of O(log(n)) (altough the constant is greater than the BTree implementation in main memory).
The ER scheme consist just of an entity with two attributes.

## LSH
The goal is to retrieve all documents ids in the same bucket (in the same band).
Assuming there are no disk space contraints and a linear (in the documents number) search time complexity (cycle through each bucket).
The time complexity should be O(l * b * n), where "l" is the number of bands, "b" is the maximum number of bucket of each band and "n" is the number of documents.

**WARNING**: I should also need to account for SSD optimized data structures.

### Possibilities
Assuming we condition on one band. One way to implement multiple bands data structure is to brutally create many simple databases, doig this, we do not have to care to search conditioning on a specific band.

#### Main memory BTree
Partially implemented.

#### SQL TABLE(id_bucket, id_doc)
An index is created for the id_bucket.
The index is needed since for each id_bucket value we need to retrieve all id_doc associated to it.

Creating the index (assuming a btree index) will slow the insertion operations from O(1) to O(log(n)), but will speed up the query operations from O(n) to O(log(n)).
Space complexity is O(n).

ER Schema:
![alt text](figures\LSH_SQL_ER_ID_BUCKET_ID_DOC.jpg)

#### SQL TABLE(id_bucket, id_doc_list, n_doc)
An index is created for the id_bucket. The value is a list (implemented as a BLOB) of documents ids with the same bucket value.
The index is needed since for each id_bucket value we need to retrieve all id_doc associated to it.
We also need to keep track of how many elements are in each list of doc_ids, this is done using the counter n_doc.

Creating the index (assuming a btree index) will slow the insertion operations from O(1) to O(log(n)), but will speed up the query operations from O(n) to O(log(n)).
Here There's also the update cost, beacuse if a doc_id has the same id_bucket value of a present row we need to update the value, which is done in steps:
    1) extract the list value
    2) add the doc id to the list
    3) update the row with the new (converted) list value.
Space complexity is O(n).

ER Schema:
![alt text](figures\LSH_SQL_ER_ID_BUCKET_ID_DOC_LIST.jpg)


