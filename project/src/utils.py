# useful function for real data scripts
import os
import shutil
import json

# General ----------------------------------------------
def MakeDir(path):
    os.makedirs(path, exist_ok=True)
    
def JoinPaths(path1, path2):
    return(os.path.join(path1, path2))

def CopyFile(src, dst):
    shutil.copy(src, dst)
    
# Metadata --------------------------------------------------
def LoadMetadata(file_path):
    with open(file_path) as file:
        return json.load(file)
    
def WriteMetadata(file_path, metadata_dict):
    with open(file_path, "w") as file:
        json.dump(metadata_dict, file)

# Already done folders --------------------------------------
def LoadCompletedFolders(file_path):
    with open(file_path) as file:
        return set(line.strip() for line in file)

def UpdateCompletedFolders(file_path, completed_folders):
    with open(file_path, "w") as file:
        for folder in completed_folders:
            file.write(folder + "\n")

# Signatures ------------------------------------------------
def MakeRelativeSignatureFolderPath(shingle_len: int,
                                    signature_len: int,
                                    bit_type):
    
    return("_".join([f"sgn_shl_{shingle_len}",
                     f"sigl_{signature_len}",
                     f"bit_{bit_type}"]))