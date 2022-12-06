# README

This is a movie script generator based on [GPT-2](https://en.wikipedia.org/wiki/GPT-2). The original idea was to fine-tune it to generate entire movie scripts, but that didn't work as planned, as it would generate garbage and repetitive output a fairly large number of times. It does generate (mostly) coherent text within its sequence length though.
 
## Files and folders description:

**The dataset can be found [here](https://drive.google.com/file/d/1au3Qk0OyPJ9Dcozu7yV7hzh6PX7j6CBF/view?usp=share_link). The model (version 1) can be found [here](https://drive.google.com/file/d/1P8CGGWo63UHYm_yeJlR7jBqkGLe9Yeuw/view?usp=share_link) and the model (version 2) can be found [here](https://drive.google.com/file/d/1mMG0O-TLQO2NXdDGYQH8pOC9mXM_lX9b/view?usp=share_link).**

The list below contains the description of files and folders in this repository I think are relevant. 

 - **deprecated** - contains code I haven't ultimately used; you can skip this folder
 - **Future_work.txt** - an unsorted list of things which could be tried in the future in order to improve the results
 - **helper_scripts/create_dataset_html_and_txt_folder_structure.py** - a script which creates the dataset folder structure
 - **helper_scripts/delete_empty_txt_files.py** - a helper script which deletes empty **.txt** files (empty movie scripts)
 - **helper_scripts/get_the_part_of_the_line_after_the_second_genre_tag.py** - string manipulation testing ground
 - **helper_scripts/preprocess_txt_movie_scripts_and_place_them_in_a_folder_v1.py** - pre-processes the dataset such that each line gets the genre name of the script as a prefix
 - **helper_scripts/preprocess_txt_movie_scripts_and_place_them_in_a_folder_v2.py** - pre-processes the dataset such that each resulting movie script line contains **MAX_WORDS_PER_LINE** words and adds the genre name of the script at the beginning and in the middle of the newly generated line
 - **huggingface_gpt2_fine_tuning.ipynb** - Jupyter notebook containing the fine-tuning code (multiple attempts of it) and the text generation code (heavily based on [this Colab notebook](https://reyfarhan.com/posts/easy-gpt2-finetuning-huggingface/))
 - **imsdb_scraper** - a folder which contains the [Scrapy](https://scrapy.org/) project for scraping [The Internet Movie Script Database (IMSDb)](https://imsdb.com/)
 - **imsdb_scraper/dataset.zip** - contains the dataset that hasn't yet been structured in appropriate folders via the **create_dataset_html_and_txt_folder_structure.py** script
 - **imsdb_scraper/imsdb_scraper/spiders/movie_scripts_spider.py** - contains the code for scraping movie scripts and storing them in **.txt** files
 - **Notes.txt** - contains (some) outputs that the model generated that I found interesting and some notes related to those outputs and the models themselves
 - **README.md** - this file
 
 
## Data scraper notes:

 - there's 11 movies that aren't enclosed in <pre> tags (either one or two); I ignored those
 - some scripts don't have a link which leads to the script reading page, so I ignored them
 - if a script belongs to multiple genres, I duplicated it so that it is contained in each genre folder it belongs to
 - within the **movie_scripts_spider.py**, I save the movie scripts into their own files in the **parse_movie_script_reading_page** function; as far as I know, this isn't idiomatic to Scrapy and things like [Item Pipelines](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) should be used; I decided to keep my code the way it is because it works, but I'm noting this here
 
## Movie Script Generator notes:
 
 - **huggingface_gpt2_fine_tuning.ipynb** contains all of the fine-tuning and text generation code; I like to believe that the code is readable and there's notes in the notebook as well; feel free to take a look
 - regardless of the prompt I use when generating the movie script, I can at best get coherent, non-repetitive output in about 40% of the cases
 - my two main approaches when generating movie scripts were using a prompt which has the following structure:
 
 `<genre name> | <second half of the generated movie line>`
 
 and
 
 `<first half of the generated movie line> | <genre name>`;
 
 the other approaches didn't pan out
 - prompt which had the structure of `<genre name> |  <second part of the generated text>` generated garbage output about 70% of the time
 - prompt which had the structure of `<first half of the generated movie line> | <genre name>` very often generated a dialogue in French; it sometimes generated a different genre in the generated line (i.e. the original prompt was **COMEDY** and it generated **FANTASY** in the middle of the line) and it generated good, but repetitive output about 40% of the time (where some of the lines where repeating themselves)
 - I also tried generating new lines with the prompt being `<second half of the generated movie line>`, but with no success
 - the best results I got was with the `<genre name> | <second half of the generated movie line>` prompt structure and **top_k = 100**
 - feel free to experiment with the prompts; and the parameters (I experimented with **top_k**, for example); maybe you find some great ones
 - **model_v1_save-20221029T144112Z-001** was fine-tuned for about 4 hours on the movie scripts preprocessed by **helper_scripts/preprocess_txt_movie_scripts_and_place_them_in_a_folder_v1.py**; **model_v2_save-20221101T214316Z-001.zip** was fine-tuned for about 5 hours and 15 minutes; it went over 3 epochs
