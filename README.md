# Near duplicate text document detection using LSH

## Description
We use LSH and Minhash to find near duplicate text documents.
The language used is python 3.12.

### Folders
- **data_creation** folder contains some script to produce an experimental collection to test the method
from an existing collection
- **slides** folder contains the slides used to present the project
- **Project** folder is where the actual scripts implementing the method are

### External modules used
This project uses **Numba** (https://numba.pydata.org/) and **Numpy** (https://numpy.org/) to speed up numeric computations, a version of **MurmurHashing** (https://pypi.org/project/mmh3/) is used to hash shingles strings .
Signatures data structure inherits a **BTrees** (https://github.com/zopefoundation/BTrees) class.

## data_creation
The data_creation folder is not the project core, but it's needeed in order to evaluate the results, also the code used is specific for the collection used.
Here's a brief description, for pratical details see the instruction.md file in data_creation.

Our starting collection (which we can't publish due to its license) is a json like document in which each line is like
{"id": "some id", "content": "some content"} where both "id" and "content" are text.

We need to create some new documents which are similar (in content) to some of the old documents.
1) In order to guarantee each id is unique we make a new id ("id2") which is the row number (int) of the document.
2) We randomly extract some documents, we modify them introducing some noise (based on parameters), and add them to the collections: each has a unique int id ("id2") and another id ("id3") which refers to the unique id ("id2") from which they were generated.

NOTE: all non modified documents have value "None" in the third id ("id3").

Example with a starting toy collection of three documents:

```json
{"id" = "aab6": "content": "the apple is green"},
{"id" = "ahb8": "content": "eternal sunshine"},
{"id" = "hrr93": "content": "dust in the wind"}
```
Suppose we randomly choose document with "id" = "aab6", add some noise and make the new collection:

```json
{"id" = "aab6": "content": "the apple is green", "id2" = 1, "id3" = "None"},
{"id" = "ahb8": "content": "eternal sunshine", "id2" = 2, "id3" = "None"},
{"id" = "hrr93": "content": "dust in the wind", "id2" = 3, "id3" = "None"},
{"id" = "aab6": "content": "the appty i gr@en", "id2" = 4, "id3" = 1"}
```
The two new ids are needed in the evaluation step: each bucket contains the ids ("id2") of estimated similar documents, so we can check which "id2" == "id3" are in each bucket.

NOTE: "id2" and "id3" are arbitrary names that can be changed, see instructions.md.

## How to use


## Evaluation
A document dataset is used. Each document is assigned an id, then some documents are duplicated and changed with "random noise" (i.e some random characters are changed or deleted). So a new collection (dataset) is made where each new document has also the id of the document from which it was generated.

This way we can evaluate Recall and Precision.
