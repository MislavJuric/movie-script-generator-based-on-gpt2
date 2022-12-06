import scrapy
import os
import traceback

class QuotesSpider(scrapy.Spider):
    name = "movie_scripts"
    start_urls = [
        "https://imsdb.com/"
    ]
    custom_settings = { # makes scrapy crawl same URLs twice or more (which is OK since one movie can be in multiple genres)
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        GENRE_TABLE_INDEX = 2 # the index of the table which stores the genres

        try:
            # TODO: see if putting the folder creation idea here (in the spider) is good (idiomatic) or no
            DATASET_ROOT_FOLDER_NAME = "dataset"
            if not os.path.exists(DATASET_ROOT_FOLDER_NAME):
                os.makedirs(DATASET_ROOT_FOLDER_NAME)
            os.chdir(DATASET_ROOT_FOLDER_NAME)

            genre_table = response.xpath('//table[@class="body"]')[GENRE_TABLE_INDEX]
            links_to_categories = genre_table.xpath("//a[starts-with(@href, '/genre')]/@href").getall()
            yield from response.follow_all(links_to_categories, callback=self.parse_genre_page)
        except:
            print("Failed to fetch the genre table")
            print(traceback.format_exc())

    def parse_genre_page(self, response):
        try:
            # get the genre name
            page_title = response.xpath("//title").get()
            page_title_elements = page_title.split(sep=" ")
            page_title = page_title_elements[0]
            page_title = page_title[7:] # removes the <title> tag
            genre_name = page_title.lower()

            links_to_movie_scripts = response.xpath("//p/a/@href")[1:] # first link is to a steam store, so that's why 0th index is not included
            yield from response.follow_all(links_to_movie_scripts, callback=self.parse_movie_script_page, cb_kwargs=dict(genre=genre_name))
        except:
            print("Failed to fetch the genre page for genre with title:")
            print(str(response.xpath("//title").get()))
            print(traceback.format_exc())


    def parse_movie_script_page(self, response, genre):
        try:
            link_to_movie_script_reading_page = response.xpath("//a[contains(text(),'Read')]/@href").get()
            yield response.follow(link_to_movie_script_reading_page, callback=self.parse_movie_script_reading_page, cb_kwargs=dict(genre=genre))
        except:
            print("Failed to fetch the script reading page for movie with title:")
            print(str(response.xpath("//title").get()))
            print(traceback.format_exc())

    def parse_movie_script_reading_page(self, response, genre):
        try:
            GENRE_FOLDER_NAME = genre
            # check if you're in the dataset folder; if yes, then
            if (os.path.basename(os.getcwd()) == "dataset"):
                # create the genre name folder if it doesn't exist and move into it
                if not os.path.exists(GENRE_FOLDER_NAME):
                    os.makedirs(GENRE_FOLDER_NAME)
                os.chdir(GENRE_FOLDER_NAME)
            # if you're not in the dataset folder and the genre name is different from the folder name you are currently in
            if ((os.path.basename(os.getcwd()) != "dataset") and (os.path.basename(os.getcwd()) != GENRE_FOLDER_NAME)):
                # go up one folder (to the root dataset folder)
                os.chdir("..")
                # create the new genre folder (if it doesn't exist) and enter it
                if not os.path.exists(GENRE_FOLDER_NAME):
                    os.makedirs(GENRE_FOLDER_NAME)
                os.chdir(GENRE_FOLDER_NAME)
            movie_script = response.xpath("//pre/pre").get()
            if (movie_script is None): # some scripts are in nested <pre> tags, some are in the first one
                movie_script = response.xpath("//pre").get()
            # save the movie script to a file named after the movie
            movie_name = response.request.url.split(sep="/")[-1][:-5] # gets the name of the movie from the last part of the URL and removes the trailing .html
            txt_file_name = movie_name + ".txt"
            html_file_name = movie_name + ".html"
            with open(txt_file_name, "w") as txt_file:
                txt_file.write(movie_script)
            with open(html_file_name, "w") as html_file:
                html_file.write(movie_script)
        except:
            print("Failed to parse the movie script reading page for movie:")
            print(str(response.xpath("//title").get()))
            print(traceback.format_exc())
