# Complexity Analysis
Below are given some complexity analysis of the methods used.

## Shingling
Assume the text to be shingled has n characters and each shingle has length w.
### Time complexity
Both versions of TextToShingles have a time complexity linear in n.
### Space complexity
The space occupied by the Array version could be precisley computed: it is equal to (n - w + 1) * w times the memory occupied by type of int chosen. The Set version occupied space depends on the number of equal shingles (the more they are the less space occupied) and by the empty space allocated by the set class.  


## MinHash
Assume there are n documents and the signature has k elements.

### Time complexity

### Space complexity
Using a tree to store all the signatures the space occupied is n * (k + 1) times the space occupied by each integer, the plus 1 is due to the document id.
Using a hash table the space should be much more if we don't want to have many collision, for example, if the 70% of the hash table was empty the total occupied space would be about n * (k + 1) / 0.3.

## LSH
