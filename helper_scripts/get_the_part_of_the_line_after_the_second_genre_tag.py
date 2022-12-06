"""
    This is a script I wrote to split a preprocessed movie script line into two parts (with the genre being the word to split on).

    I wrote this to get the splitting to work locally first, so that I don't waste my Google Collab resources if I don't have to.
"""

import os

PREPROCESSED_FILES_DIRECTORY = os.path.join("dataset", "txt_preprocessed_v2")

# go into the PREPROCESSED_FILES_DIRECTORY directory
dataset_subdir_list = [subdirectory_name for subdirectory_name in os.listdir(PREPROCESSED_FILES_DIRECTORY)]
os.chdir(PREPROCESSED_FILES_DIRECTORY)

# enter each subdirectory (genre folder)
for subdirectory_name in dataset_subdir_list:
    genre_name = subdirectory_name.upper()
    os.chdir(subdirectory_name)
    txt_filenames_list = [txt_file_name for txt_file_name in os.listdir(os.getcwd()) if txt_file_name.endswith(".txt")]
    for txt_file_name in txt_filenames_list:
        print("Opening " + txt_file_name + " in folder " + subdirectory_name + "...")
        txt_file = open(txt_file_name, "r")
        txt_file_lines = txt_file.readlines()
        for movie_script_line in txt_file_lines:
            movie_script_line_parts = movie_script_line.split(genre_name)
            print(movie_script_line_parts)
        break
    os.chdir("..")
