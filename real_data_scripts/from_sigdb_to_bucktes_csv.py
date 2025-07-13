from near_duplicate_doc_lsh.project.src import minhash as mh
from near_duplicate_doc_lsh.project.src import lsh

import argparse

in_file_name = "test.db"
out_file_name = "out.csv"

def WriteSignatureDbToBandBucketCsv(in_db_file_name: str,
                                    out_csv_file_name: str,
                                    n_bands: int = 10,
                                    times_buckets: int = 5,
                                    do_unpickle = True,
                                    seed: int = 123) -> None:
    '''
    Description:

    used to convert database.db to hadoop readable file system 

    Inputs: -----------------
    1) database.db with record
    key = document id, value = (pickled np.array) signature
    2) LSH parameters: number of bands, number of bucktes
    hash function for each band
    Writes ------------------
    file.csv with each row is a document
    first column is document 1
    all other columns are bucket ids
    Example --------------------------
    number of bands = 2, number of buckets per band = 3
    id_doc1, band1_bucket_id, band2_bucket_id


    Args:
        - in_db_file_name:
        - out_csv_file_name:
        - n_bands:
        - times_buckets
        - seed
        - do_unpickle
    
    Return: None
    '''

     
    SigSQL = mh.SignaturesSQLite(database_name = in_db_file_name)

    # get signature len
    # since it's a numpy array
    signature_len = SigSQL.fetch_first_rows(do_unpickle_col2 = do_unpickle, row_count = 1)[1].ndim

    n_rows = SigSQL.count_rows()
    n_buckets = times_buckets * n_rows


    # generate hash functions for lsh bands hashing ----------------------
    my_lsh_hash_fun_list = lsh.GenerateMotwaniHashFunctionsList(n_hash_functions = n_bands,
                                                                            band_size = signature_len // n_bands,
                                                                            modulo = n_buckets,
                                                                            seed = seed)

    my_break_points = lsh.GenerateBreakPoints(n = signature_len,
                                              n_bands = n_bands)
    

    # define rows iterator
    fetched_rows_iterator = SigSQL.fetch_all_rows(do_unpickle_col2 = do_unpickle)
    
    with open(out_csv_file_name, "w") as fout:
        for row in fetched_rows_iterator:
            temp_id = row[0]
            temp_signature = row[1]

            temp_bucket_id_list = lsh.ComputeAllHashBands(signature = temp_signature,
                                                          break_points = my_break_points,
                                                          hash_functions_list = my_lsh_hash_fun_list)
            
            # write csv line
            fout.write(f"{temp_id},")
            
            for i in range(len(temp_bucket_id_list) - 1):
                fout.write(f"{temp_bucket_id_list[i]},")
            
            fout.write(f"{temp_bucket_id_list[-1]}\n")
            
    SigSQL.close_database()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
    "--db_name_in",
    type=str,
    required=True)

    parser.add_argument(
    "--csv_name_out",
    type=str,
    required=True)

    parser.add_argument(
    "--n_bands",
    type=int,
    required=False)

    parser.add_argument(
    "--times_buckets",
    type=int,
    required=False)

    parser.add_argument(
    "--do_unpickle",
    type=bool,
    required=False)

    parser.add_argument(
    "--seed",
    type=int,
    required=False)

    args = parser.parse_args()

    WriteSignatureDbToBandBucketCsv(in_db_file_name = parser.db_name_in,
                                    out_csv_file_name = parser.csv_name_out,
                                    n_bands = parser.n_bands,
                                    times_buckets = parser.times_buckets,
                                    do_unpickle = parser.do_unpickle,
                                    seed = parser.seed)