from . import make_collection as mc
# files referenced are not included in the project folder
 
# params for first_50.json
# don't write original lines
first_50_dict_params_no_original = {"file_in": "Data_Creation\\first_50.json",
                                    "file_out_collection": "first_50_edit_1.json",
                                     "file_out_index": "first_50_edit_1_index.csv",
                                    "n_random_lines": 10,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0.1, 0.1, 0.5]],
                                    "write_original_lines": False,
                                    "n_lines_in_file": 50,
                                    "id_int_unique_last_index": 49}

# write the original lines
first_50_dict_params_yes_original = {"file_in": "Data_Creation\\first_50.json",
                                    "file_out_collection": "first_50_edit_1.json",
                                     "file_out_index": "first_50_edit_1_index.csv",
                                    "n_random_lines": 10,
                                    "edit_dict_fun" : mc.EditDictOCR,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "edit_text_function": mc.EditTextOCR,
                                    "content_field_name": "content",
                                    "error_params_list": [[0.1, 0.1, 0.5]],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 50,
                                    "id_int_unique_last_index": 49}


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