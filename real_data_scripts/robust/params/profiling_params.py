from near_duplicate_doc_lsh.project.src import minhash as mh

N_BANDS = 20
TIMES_BUCKET = 25

DB_PATH = "data_near_duplicate\\robust\\signatures_db_duplicates\\sgn_shl_9_sigl_200_bit_uint32_mid_noise_per25\\signature_db"

OUT_FOLDER = "data_near_duplicate\\robust\\profiling\\"


collection_dict = mh.SignatureSQLIterator(DB_PATH)

OUT_RELATIVE_PATH = f"nba_{N_BANDS}_nbu_{TIMES_BUCKET}_sigl_{collection_dict['signature_len']}_ndoc_{collection_dict['n_rows']}.log"
OUT_COMPLETE_PATH = OUT_FOLDER + OUT_RELATIVE_PATH