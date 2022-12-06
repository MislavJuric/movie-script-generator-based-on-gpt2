"""
    This script combines multiple movie lines until it reaches MAX_WORDS_PER_LINE. It adds the genre name at the beginning and in the middle
    of the newly created movie line. I decided to do this since in version 1 of this script GPT2 seems to struggle to generate coherent movie
    script and my hypothesis is that it lacks previous context (i.e. if I prompt it with just genre name every time) it generates plausible
    lines every time, but they are incoherent when viewed as a whole.

    I decided to keep the tags (such as <b>) and the blank lines because they add structure to the movie script.
    Also, it is hard to detect different movie script elements (character lines, interior / exterior descriptions etc.) from the HTML markup, since
    most of the movie script is raw text and some of it is delineated by <b> tags. There's no other markup (other than a <pre> at the beginning of the
    movie script), which makes it hard to detect movie script elements by looking at the HTML markup.

    TODO: Better variable naming? (instead of subdirectory_name write genre_folder_name); the first one isn't wrong
    per se, but maybe it's a bit unclear
"""

import os

PREPROCESSED_FILES_DIRECTORY = os.path.join("dataset", "txt_preprocessed_v2")
DATASET_DIRECTORY = os.path.join("dataset", "txt")
START_OF_TEXT_TOKEN = "<|startoftext|>"
END_OF_TEXT_TOKEN = "<|endoftext|>"
MAX_WORDS_PER_LINE = 768 # since word == token (https://jalammar.github.io/illustrated-gpt2/)
MIDDLE_OF_A_LINE = MAX_WORDS_PER_LINE / 2

# go into the DATASET_DIRECTORY
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
        # initialize a new variable for the same modified (preprocessed) txt file (movie script)
        modified_txt_file = ""
        # read it line by line
        txt_file = open(txt_file_name, "r")
        txt_file_lines = txt_file.readlines()
        genre_name = subdirectory_name.upper()
        current_txt_file_line_index = 0

        while (current_txt_file_line_index < (len(txt_file_lines) - 1)):
            new_line = ""
            current_token_count = 0
            already_added_genre_in_the_middle = False
            if (current_txt_file_line_index == 0): # first line, add start token
                new_line += START_OF_TEXT_TOKEN + " "
                current_token_count += 1
            new_line += genre_name + " | "
            current_token_count += 2
            while ((current_token_count <= MAX_WORDS_PER_LINE) and (current_txt_file_line_index < (len(txt_file_lines) - 1))):
                if ((current_token_count >= MIDDLE_OF_A_LINE) and (already_added_genre_in_the_middle == False)):
                    new_line += genre_name + " | "
                    current_token_count += 2
                    already_added_genre_in_the_middle = True
                current_line = txt_file_lines[current_txt_file_line_index]
                if ((current_token_count + len(current_line.split())) > MAX_WORDS_PER_LINE):
                    break
                current_line_tokens = current_line.split()
                for token in current_line_tokens:
                    new_line += token + " "
                current_token_count = current_token_count + len(current_line.split())
                current_txt_file_line_index += 1
            if (current_txt_file_line_index < (len(txt_file_lines) - 1)):
                modified_txt_file += new_line + "\n"
            elif (current_txt_file_line_index == (len(txt_file_lines) - 1)):
                if (current_token_count < MAX_WORDS_PER_LINE):
                    modified_txt_file += new_line + " " + END_OF_TEXT_TOKEN + "\n"
                else:
                    modified_txt_file += new_line + "\n" + END_OF_TEXT_TOKEN + "\n"

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
