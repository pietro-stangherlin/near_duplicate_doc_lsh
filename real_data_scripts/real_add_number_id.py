from near_duplicate_doc_lsh.data_creation.src import add_num_ids as an

# instructions:
# exectute from LSH folder with:
# > python -m near_duplicate_doc_lsh.real_data_scripts.real_add_number_id

collection_params_dict = {"file_in" : "data_near_duplicate\\robust\\tipster_45_all_docs.json",
                     "file_out" : "data_near_duplicate\\robust\\robust_id2.json",
                     "id_old_name" : "id",
                     "id_new_name" : "id2"}

an.ConvertID(file_in = collection_params_dict["file_in"],
             file_out = collection_params_dict["file_out"],
             id_new_name = collection_params_dict["id_new_name"])