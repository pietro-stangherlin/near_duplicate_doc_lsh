from . import make_collection as mc
# NOTE: some files referenced are not included in the project folder

arxiv_1000_only_duplicates = {"file_in": "test_data\\arxiv_first_1000_id2.json",
                              "folder_path_out": "test_data\\arxiv_duplicates",
                                "relative_file_out_collection": "arxiv_clones_1000_only_duplicates.json",
                                "relative_file_out_index": "arxiv_clones_1000_index.csv",                                    "n_random_lines": 100,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": "content",
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": 1000,
                                    "id_int_unique_last_index": 1000}

arxiv_1000_only_duplicates_noise = {"file_in": "test_data\\arxiv_first_1000_id2.json",
                                    "file_out_collection": "test_data\\arxiv_clones_first_1000_only_duplicates_noise.json",
                                     "file_out_index": "test_data\\arxiv_clones_first_1000_index_noise.csv",
                                    "n_random_lines": 100,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": "content",
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0.1, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": 1000,
                                    "id_int_unique_last_index": 1000}
 


robust_yes_original = {"file_in": "data_near_duplicate\\robust_2.json",
                                    "file_out_collection": "robust_clones.json",
                                     "file_out_index": "robust_clones_index.csv",
                                    "n_random_lines": 100000,
                                     "id_int_unique_field_name": "id2",
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": "content",
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": True,
                                    "n_lines_in_file": 528155,
                                    "id_int_unique_last_index": 528155}