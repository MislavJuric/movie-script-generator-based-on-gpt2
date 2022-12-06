"""
    This script appends the genre name before every single line.

    I decided to keep the tags (such as <b>) and the blank lines because they add structure to the movie script.
    Also, it is hard to detect different movie script elements (character lines, interior / exterior descriptions etc.) from the HTML markup, since
    most of the movie script is raw text and some of it is delineated by <b> tags. There's no other markup (other than a <pre> at the beginning of the
    movie script), which makes it hard to detect movie script elements by looking at the HTML markup.

    TODO: Better variable naming? (instead of subdirectory_name write genre_folder_name); the first one isn't wrong
    per se, but maybe it's a bit unclear
"""

import os

PREPROCESSED_FILES_DIRECTORY = os.path.join("dataset", "txt_pruned")
DATASET_DIRECTORY = os.path.join("dataset", "txt")
START_TOKEN = "<|startoftext|>"
END_TOKEN = "<|endoftext|>"

# go into the dataset/txt directory
dataset_subdir_list = [subdirectory_name for subdirectory_name in os.listdir(DATASET_DIRECTORY)]
# create the PREPROCESSED_FILES_DIRECTORY if it doesn't exist
if not os.path.exists(PREPROCESSED_FILES_DIRECTORY):
    os.makedirs(PREPROCESSED_FILES_DIRECTORY)
os.chdir(DATASET_DIRECTORY)

# enter each subdirectory (genre folder)
for subdirectory_name in dataset_subdir_list:
    os.chdir(subdirectory_name)
    txt_filenames_list = [txt_file_name for txt_file_name in os.listdir(os.getcwd()) if txt_file_name.endswith(".txt")]
    for txt_file_name in txt_filenames_list:
        # initialize a new variable for the same modified txt file (movie script)
        modified_txt_file = ""
        # read it line by line
        txt_file = open(txt_file_name, "r")
        txt_file_lines = txt_file.readlines()
        genre_name = subdirectory_name.upper()
        for txt_file_line in txt_file_lines:
            # add subfolder name (in all caps), a space, a vertical line and a space (in that order) to the line
            modified_line = genre_name + " | " + txt_file_line
            modified_txt_file += modified_line
        # add the starting and the ending tokens
        modified_txt_file = START_TOKEN + modified_txt_file + END_TOKEN
        # store the modified txt file variable into the modified files directory (if it's a relative path be mindful)
        os.chdir(os.path.join("..", "..", "..")) # outside of the root dataset folder
        os.chdir(PREPROCESSED_FILES_DIRECTORY)
        if not os.path.exists(subdirectory_name):
            os.makedirs(subdirectory_name)
        os.chdir(subdirectory_name)
        with open(txt_file_name, "w") as modified_txt_file_to_write_to:
            modified_txt_file_to_write_to.write(modified_txt_file)
        os.chdir(os.path.join("..", "..", "..")) # outside of the root dataset folder
        os.chdir(os.path.join(DATASET_DIRECTORY, subdirectory_name)) # go back to the original genre folder
    os.chdir("..")
