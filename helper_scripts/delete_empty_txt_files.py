"""
    This script deletes empty .txt files in a dataset.
"""

import os

DATASET_DIRECTORY = os.path.join("dataset", "txt_preprocessed_v2")

os.chdir(DATASET_DIRECTORY)

dataset_subdir_list = [subdirectory_name for subdirectory_name in os.listdir(os.getcwd())]

for subdirectory_name in dataset_subdir_list:
    os.chdir(subdirectory_name)
    txt_filenames_list = [txt_file_name for txt_file_name in os.listdir(os.getcwd()) if txt_file_name.endswith(".txt")]
    for txt_file_name in txt_filenames_list:
        if os.path.getsize(txt_file_name) == 0:
            print(subdirectory_name + "/" + txt_file_name + " is empty. Deleting it.")
            os.remove(txt_file_name)
    os.chdir("..")
