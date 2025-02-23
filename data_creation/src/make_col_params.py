from . import make_collection as mc
# some files referenced are not included in the project folder

arxiv_yes_original_first_1000 = {"file_in": "data_near_duplicate\\arxiv\\arxiv_cleaned_js_id2_first_1000.json",
                                    "file_out_collection": "near_duplicate_doc_lsh\\test_data\\arxiv_clones_first_1000.json",
                                     "file_out_index": "near_duplicate_doc_lsh\\test_data\\arxiv_clones_first_1000_index.csv",
                                    "n_random_lines": 100,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0, 0, 0]],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 1000,
                                    "id_int_unique_last_index": 999}

arxiv_yes_original = {"file_in": "data_near_duplicate\\arxiv\\arxiv_cleaned_js_id2.json",
                                    "file_out_collection": "arxiv_clones.json",
                                     "file_out_index": "arxiv_clones_index.csv",
                                    "n_random_lines": 10000,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0, 0, 0]],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 51774,
                                    "id_int_unique_last_index": 51773}
 
# params for first_50.json
# don't write original lines
first_100_dict_params_no_original = {"file_in": "data_near_duplicate\\robust2_first_100.json",
                                    "file_out_collection": "first_100_edit_1.json",
                                     "file_out_index": "first_50_edit_1_index.csv",
                                    "n_random_lines": 10,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0.1, 0.1, 0.5]],
                                    "write_original_lines": False,
                                    "n_lines_in_file": 100,
                                    "id_int_unique_last_index": 99}

# write the original lines
first_100_dict_params_yes_original = {"file_in": "data_near_duplicate\\robust2_first_100.json",
                                    "file_out_collection": "first_100_edit_1.json",
                                     "file_out_index": "first_50_edit_1_index.csv",
                                    "n_random_lines": 10,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0.1, 0.1, 0.5]],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 100,
                                    "id_int_unique_last_index": 99}


robust_yes_original = {"file_in": "data_near_duplicate\\robust_2.json",
                                    "file_out_collection": "robust_clones.json",
                                     "file_out_index": "robust_clones_index.csv",
                                    "n_random_lines": 100000,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0, 0, 0]],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 528155,
                                    "id_int_unique_last_index": 528154}