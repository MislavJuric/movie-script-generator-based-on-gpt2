"""
This script creates separate html and txt folders, creates a genre subfolder in each of them and populates them with movie scripts
"""

import os
import subprocess

DATASET_FOLDER = "dataset"
HTML_FOLDER_NAME = "html"
TXT_FOLDER_NAME = "txt"

os.chdir(DATASET_FOLDER)
# creates the HTML and TXT folders
os.makedirs(HTML_FOLDER_NAME)
os.makedirs(TXT_FOLDER_NAME)

for directory in os.listdir(os.getcwd()):
    if ((directory == HTML_FOLDER_NAME) or (directory == TXT_FOLDER_NAME)): # skip over the newly created folders
        continue
    # creates genre name directories within HTML and TXT folders
    os.makedirs(os.path.join(HTML_FOLDER_NAME, directory))
    os.makedirs(os.path.join(TXT_FOLDER_NAME, directory))
    os.chdir(directory)
    subprocess.run(["cp *.html " + "../" + HTML_FOLDER_NAME + "/" + directory], shell=True)
    subprocess.run(["cp *.txt " + "../" + TXT_FOLDER_NAME + "/" + directory], shell=True)
    os.chdir("..")

# remove the genre name folders in the root dataset directory
for directory in os.listdir(os.getcwd()):
    if ((directory == HTML_FOLDER_NAME) or (directory == TXT_FOLDER_NAME)):
        continue
    subprocess.run(["rm", "-r", directory])
