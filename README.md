# Near duplicate text document detection using LSH

## Description
We use LSH and Minhash to find near duplicate text documents.
The language used is python 3.12.

### Folders
- **data_creation** folder contains some script to produce an experimental collection to test the method
from an existing collection
- **slides** folder contains the slides used to present the project
- **project** folder is where the actual scripts implementing the method are

### External modules used
Signatures data structure inherits a **BTrees** (https://github.com/zopefoundation/BTrees) class
Some ideas in the project are insipired from **datasketch** (https://github.com/ekzhu/datasketch).

## How to use


## Evaluation
A document dataset is used. Each document is assigned an id, then some documents are duplicated and changed with "random noise" (i.e some random characters are changed or deleted). So a new collection (dataset) is made where each new document has also the id of the document from which it was generated.

This way we can evaluate Recall and Precision.
