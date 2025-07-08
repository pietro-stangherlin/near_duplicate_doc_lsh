from near_duplicate_doc_lsh.data_creation.src import make_collection as mc
from near_duplicate_doc_lsh.real_data_scripts_arxiv.params import parameters as pm

arxiv_path = "data_near_duplicate\\arxiv\\"
arxiv_clones_path = arxiv_path + "\\arxiv_clones\\"


arxiv_no_duplicates_nlines = 2776569

# percentace on total number of duplicates

SMALL_NOISE_PER_a = 0.02

# 1%
per1 = int(arxiv_no_duplicates_nlines * 0.01)
# 5%
per5 = int(arxiv_no_duplicates_nlines * 0.05)
# 10 %
per10 = int(arxiv_no_duplicates_nlines * 0.1)
# 25 %
per25 = int(arxiv_no_duplicates_nlines * 0.25)
# 50 %
per50 = int(arxiv_no_duplicates_nlines * 0.5)


# No noise: exact duplicates -----------------------------------------------------

no_noise_per1_path = arxiv_clones_path + "no_noise_per1\\"

arxiv_only_clones_no_noise_per1 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per1_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per1,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

# make this first as a test
no_noise_per5_path = arxiv_clones_path + "no_noise_per5\\"

arxiv_only_clones_no_noise_per5 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per5_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}


no_noise_per10_path = arxiv_clones_path + "no_noise_per10\\"

arxiv_only_clones_no_noise_per10 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per10_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per10,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

no_noise_per25_path = arxiv_clones_path + "no_noise_per25\\"

arxiv_only_clones_no_noise_per25 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per25_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per25,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}


no_noise_per50_path = arxiv_clones_path + "no_noise_per50\\"

arxiv_only_clones_no_noise_per50 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": no_noise_per50_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per50,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, 0],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

# Small noise: not exact duplicates -----------------------------------------------------

small_noise_per1_path = arxiv_clones_path + "small_noise_per1\\"

arxiv_only_clones_small_noise_per1 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per1_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per1,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

small_noise_per5_path = arxiv_clones_path + "small_noise_per5\\"

arxiv_only_clones_small_noise_per5 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per5_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per5,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}


small_noise_per10_path = arxiv_clones_path + "small_noise_per10\\"
arxiv_only_clones_small_noise_per10 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per10_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per10,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}


small_noise_per25_path = arxiv_clones_path + "small_noise_per25\\"
arxiv_only_clones_small_noise_per25 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per25_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per25,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

small_noise_per50_path = arxiv_clones_path + "small_noise_per50\\"
arxiv_only_clones_small_noise_per50 = {"file_in": pm.ARXIV_ORIGINAL_PATH,
                                    "folder_path_out": small_noise_per50_path,
                                    "relative_file_out_collection": "arxiv_duplicates.json",
                                    "relative_file_out_index": "arxiv_index.csv",
                                    "n_random_lines": per50,
                                     "id_int_unique_field_name": pm.ID_FIELD_NAME,
                                    "id_int_link_field_name": "id3",
                                    "content_field_name": pm.CONTENT_FIELD_NAME,
                                    "functions_edit_list": mc.ocr_functions_list,
                                    "functions_params_list": [0, 0, SMALL_NOISE_PER_a],
                                    "write_original_lines": False,
                                    "n_lines_in_file": arxiv_no_duplicates_nlines,
                                    "id_int_unique_last_index": arxiv_no_duplicates_nlines}

# error prone, to be changed
all_config_list = [arxiv_only_clones_no_noise_per1,
                  arxiv_only_clones_no_noise_per5,
                  arxiv_only_clones_no_noise_per10,
                  arxiv_only_clones_no_noise_per25,
                  arxiv_only_clones_no_noise_per50,
                  arxiv_only_clones_small_noise_per1,
                  arxiv_only_clones_small_noise_per5,
                  arxiv_only_clones_small_noise_per10,
                  arxiv_only_clones_small_noise_per25,
                  arxiv_only_clones_small_noise_per50]

all_config_path_list = [no_noise_per1_path,
                        no_noise_per5_path,
                        no_noise_per10_path,
                        no_noise_per25_path,
                        no_noise_per50_path,
                        small_noise_per1_path,
                        small_noise_per5_path,
                        small_noise_per10_path,
                        small_noise_per25_path,
                        small_noise_per50_path]