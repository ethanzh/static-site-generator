import os
import json
import markdown
import re
import shutil
import time

start_time = time.time()

DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory

BLOG_DIR = os.path.join(CURRENT_DIR, "content")  # Gets path to blog folder
BLOG_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                BLOG_DIR, i) for i in os.listdir(BLOG_DIR)]

WPM = 275
WORD_LENGTH = 5

markdown_file_locations = []


class PostObject(object):

    def __init__(self, title, link, date, summary, post_time, reading_time, private, tags):
        self.title = title
        self.link = link
        self.date = date
        self.summary = summary
        self.time = post_time
        self.reading_time = reading_time
        self.private = private
        self.tags = tags

    def set_link(self, link):
        self.link = link


def get_template(template):
    with open(os.path.join("templates", template + ".html"), "r") as html_file:
        return html_file.read()


def process_markdown(current_directory):  # Returns [json, text]
    return get_metadata_as_json(current_directory), get_md_as_text(current_directory)


def get_metadata_as_json(current_directory):
    with open(current_directory, "r") as md_file:
        metadata = md_file.read().rsplit('---END_METADATA---', 1)[0].split("---START_METADATA---", 1)[1]  # Get metadata

        json_metadata = json.loads(metadata)

        return json_metadata


def get_md_as_text(current_directory):
    with open(current_directory, "r") as md_file:
        body_text = md_file.read().split("---END_METADATA---", 1)[1]

        length = len(body_text)

        word_count = length / WORD_LENGTH  # Assuming average word length is 5

        reading_time = calculate_reading_time(word_count, WPM, body_text)

        return_list = [body_text, reading_time]

        return return_list  # Gets all text after END_METADATA


def calculate_reading_time(word_count, wpm, text):
    number_images = text.count("![")
    total_time = 0

    if number_images > 10:
        total_time += 1.25
        total_time += (number_images - 10)

    elif number_images != 1:
        total_time += 0.01667 * ((number_images * 12) - (((number_images ** 2) + number_images) / 2))

    else:
        total_time += 0.2

    total_time += (word_count / wpm)

    return total_time


def build_lists():
    for i in BLOG_FILE_NAMES:
        if i[-2:] == "md":  # Finds all .md files in blog directory
            markdown_file_locations.append(i)


def md_to_html(md_string):
    return markdown.markdown(md_string)


def create_post_object(path):

    directory_so_far = "posts"

    template_html = get_template("post")

    processed = process_markdown(path)  # [json, text]
    processed_json = processed[0]
    text = processed[1][0]

    title = processed_json['title']

    spaceless_title = title.replace(" ", "-")
    lower_title = spaceless_title.lower()
    final_title = re.sub(r'[^a-zA-Z0-9-]', '', lower_title)

    body_html = md_to_html(text)

    final_html = template_html.replace("{BODY}", body_html)

    print(final_html)

    try:

        os.makedirs(os.path.join(directory_so_far, final_title))

        new_html_location = os.path.join("posts", final_title, "index.html")

        new_html_file = open(new_html_location, "w", encoding='utf-8')
        new_html_file.write(final_html)

    except OSError as e:
        print('uh oh')


def reset_dirs():
    folders_to_reset = ["posts"]

    for i in folders_to_reset:
        if os.path.exists(i):
            shutil.rmtree(i)
            os.makedirs(i)


def run():
    build_lists()

    reset_dirs()

    for i in markdown_file_locations:  # Goes through locations and creates .html files
        create_post_object(i)

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    run()
