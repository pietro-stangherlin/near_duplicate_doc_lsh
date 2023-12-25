# Near duplicate text document detection using LSH

## Description
We use LSH and Minhash to find near duplicate text documents.
The language used is python.

## Evaluation
A document dataset is used. Each document is assigned an id, then some documents are duplicated and changed with "random noise" (i.e some random characters are changed or deleted). So a new collection (dataset) is made where each new document has also the id of the document from which it was generated.

This way we can evaluate Recall and Precision.

