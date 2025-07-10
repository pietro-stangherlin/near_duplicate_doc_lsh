from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
from near_duplicate_doc_lsh.real_data_scripts_robust.params import parameters as pm

robust_path = "data_near_duplicate\\robust\\"
robust_clones_path = robust_path + "\\robust_clones\\"

# percentace on total number of duplicates

SMALL_NOISE_PER_a = 0.02
MID_NOISE_PER_a = 0.05

# 1%
per1 = int(pm.robust_no_duplicates_nlines * 0.01)
# 5%
per5 = int(pm.robust_no_duplicates_nlines * 0.05)
# 10 %
per10 = int(pm.robust_no_duplicates_nlines * 0.1)
# 25 %
per25 = int(pm.robust_no_duplicates_nlines * 0.25)



# No noise: exact duplicates -----------------------------------------------------

no_noise_per1_path = robust_clones_path + "no_noise_per1\\"

robust_only_clones_no_noise_per1 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per1_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per1,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

# make this first as a test
no_noise_per5_path = robust_clones_path + "no_noise_per5\\"

robust_only_clones_no_noise_per5 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per5_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


no_noise_per10_path = robust_clones_path + "no_noise_per10\\"

robust_only_clones_no_noise_per10 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per10_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per10,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

no_noise_per25_path = robust_clones_path + "no_noise_per25\\"

robust_only_clones_no_noise_per25 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per25_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per25,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


# Small noise: not exact duplicates -----------------------------------------------------

small_noise_per1_path = robust_clones_path + "small_noise_per1\\"

robust_only_clones_small_noise_per1 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per1_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per1,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

small_noise_per5_path = robust_clones_path + "small_noise_per5\\"

robust_only_clones_small_noise_per5 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per5_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


small_noise_per10_path = robust_clones_path + "small_noise_per10\\"
robust_only_clones_small_noise_per10 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per10_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per10,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


small_noise_per25_path = robust_clones_path + "small_noise_per25\\"
robust_only_clones_small_noise_per25 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per25_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per25,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

# Mid noise: not exact duplicates -----------------------------------------------------

mid_noise_per1_path = robust_clones_path + "mid_noise_per1\\"

robust_only_clones_mid_noise_per1 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": mid_noise_per1_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per1,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, MID_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

mid_noise_per5_path = robust_clones_path + "mid_noise_per5\\"

robust_only_clones_mid_noise_per5 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": mid_noise_per5_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, MID_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


mid_noise_per10_path = robust_clones_path + "mid_noise_per10\\"
robust_only_clones_mid_noise_per10 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": mid_noise_per10_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per10,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, MID_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}


mid_noise_per25_path = robust_clones_path + "mid_noise_per25\\"
robust_only_clones_mid_noise_per25 = {"file_in": pm.ROBUST_ORIGINAL_PATH,
                                    "folder_path_out": mid_noise_per25_path,
                                    "relative_file_out_collection": "robust_duplicates.json",
                                    "relative_file_out_index": "robust_index.csv",
                                    "n_random_lines": per25,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, MID_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": pm.robust_no_duplicates_nlines,
                                    "id_int_unique_last_index": pm.robust_no_duplicates_nlines}

# error prone, to be changed
all_config_list = [robust_only_clones_no_noise_per1,
                  robust_only_clones_no_noise_per5,
                  robust_only_clones_no_noise_per10,
                  robust_only_clones_no_noise_per25,
                  robust_only_clones_small_noise_per1,
                  robust_only_clones_small_noise_per5,
                  robust_only_clones_small_noise_per10,
                  robust_only_clones_small_noise_per25,
                    robust_only_clones_mid_noise_per1,
                  robust_only_clones_mid_noise_per5,
                  robust_only_clones_mid_noise_per10,
                  robust_only_clones_mid_noise_per25]

all_config_path_list = [no_noise_per1_path,
                        no_noise_per5_path,
                        no_noise_per10_path,
                        no_noise_per25_path,
                        small_noise_per1_path,
                        small_noise_per5_path,
                        small_noise_per10_path,
                        small_noise_per25_path,
                        mid_noise_per1_path,
                        mid_noise_per5_path,
                        mid_noise_per10_path,
                        mid_noise_per25_path]