"""
A script which defines how to load this dataset so that it's compatible with Hugging Face
Based on : https://github.com/huggingface/datasets/blob/main/templates/new_dataset_script.py
"""

# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Address all TODOs and remove all explanatory comments


import os

import datasets

_DESCRIPTION = """\
This dataset is a collection of movie scripts scraped from https://imsdb.com/
"""

# TODO: Name the class differently?
class Txt(datasets.GeneratorBasedBuilder):
    """This dataset is a collection of movie scripts scraped from https://imsdb.com/"""

    VERSION = datasets.Version("1.0.0")

    # This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
    def _info(self):
        features = datasets.Features(
            {
                "label": datasets.ClassLabel(names=["action", "adventure", "animation", "comedy", "crime", "drama", "family", "fantasy", "film-noir", "horror", "musical", "mystery", "romance", "sci-fi", "short", "thriller", "war", "western"]),
                "script": datasets.Value("string")
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features
        )

    # This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
    def _split_generators(self, dl_manager):
        data_dir = "."
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train",
                },
            )#,
            # TODO: see if I should add the val and the test split as well
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
    def _generate_examples(self, filepath, split):
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        genre_subdirectories_in_the_dataset_directory = [directory_name for directory_name in os.listdir(filepath) if os.path.isdir(directory_name)]
        key = 0
        for genre_subdirectory in genre_subdirectories_in_the_dataset_directory:
            os.chdir(genre_subdirectory)
            label = str(genre_subdirectory)
            scripts_in_this_genre_subdirectory = [txt_file for txt_file in os.listdir(os.getcwd()) if txt_file.endswith(".txt")]
            for script_name in scripts_in_this_genre_subdirectory:
                # load the script as a string
                script_txt_file = open(script_name, "r")
                script = script_txt_file.read()
                script_txt_file.close()
                yield key, {
                    "label" : label,
                    "script": script
                }
                # yield the result
                key = key + 1
            os.chdir("..")
