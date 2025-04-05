from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
from near_duplicate_doc_lsh.real_data_scripts.params import parameters as pm

robust_path = "data_near_duplicate\\robust\\"
robust_clones_path = robust_path + "\\robust_clones\\"
file_in = robust_path + "robust_id2_unq.json"
robust_no_duplicates_nlines = 522281


# No noise: exact duplicates -----------------------------------------------------

no_noise_10k_path = robust_clones_path + "no_noise_10k\\"

robust_only_clones_no_noise_10k = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_10k_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": 10**4,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": robust_no_duplicates_nlines}

# make this first as a test
no_noise_100k_path = robust_clones_path + "no_noise_100k\\"

robust_only_clones_no_noise_100k = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_100k_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": 10**5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": robust_no_duplicates_nlines}

# Small noise: not exact duplicates -----------------------------------------------------

small_noise_10k_path = robust_clones_path + "small_noise_10k\\"

robust_only_clones_small_noise_10k = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_10k_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": 10**4,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0.05],
                                    "write_original_lines": False,
                                    "n_lines_in_file": robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": robust_no_duplicates_nlines}

small_noise_100k_path = robust_clones_path + "small_noise_100k\\"

robust_only_clones_small_noise_100k = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_100k_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": 10**5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0.05],
                                    "write_original_lines": False,
                                    "n_lines_in_file": robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": robust_no_duplicates_nlines}

# error prone, to be changed
all_config_list = [robust_only_clones_no_noise_10k,
                  robust_only_clones_no_noise_100k,
                  robust_only_clones_small_noise_10k,
                  robust_only_clones_small_noise_100k]

all_config_path_list = [no_noise_10k_path,
                        no_noise_100k_path,
                        small_noise_10k_path,
                        small_noise_100k_path]