from ..src import add_num_ids as an

# arxiv abstract collection
# (NOTE: this step could be avoided since the file already has an integer id)
# we do it anyway for clarity

# arxiv parameters:
# arxiv_first_1000.json id id2
# from command line:
# python .\data_creation\tests\test_add_num_ids.py .\test_data\arxiv_first_1000.json .\test_data\arxiv_first_1000_id2.json id id2


# from near_duplicate_doc_lsh folder folder
# python -m data_creation.tests.test_add_num_ids

arxiv_params_dict = {"file_in" : ".\\test_data\\arxiv_first_1000.json",
                     "file_out" : ".\\test_data\\arxiv_first_1000_id2.json",
                     "id_old_name" : "id",
                     "id_new_name" : "id2"}

an.ConvertID(file_in = arxiv_params_dict["file_in"],
             file_out = arxiv_params_dict["file_out"],
             id_new_name = arxiv_params_dict["id_new_name"])