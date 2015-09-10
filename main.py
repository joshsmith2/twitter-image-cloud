#!/usr/bin/env python3

import os
import argparse
import csv
import jinja2
import sqlite3
from multiprocessing import Pool

#TODO: CLASSES! Get this rabble in shape.

SOURCE_ROOT = os.path.dirname(os.path.realpath(__file__))

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input-csv', metavar='PATH', dest='input_csv',
                   help='CSV file containing urls to images')
    p.add_argument('-o' '--output-file', metavar='PATH', dest='output_file')
    return p.parse_args()


def get_lines_from_csv(csv_file):
    """
    :return: A generator to enable grabbing chunks of files
    """
    if not os.path.exists(csv_file):
        raise OSError
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

class ImageCloud:

    def __init__(self, csv_file, db_path,
                 url_column_name='twitter.tweet/mediaUrls',
                 html_output_file='./images.html',
                 html_template = 'index.html',
                 chunk_size=1000,
                 image_limit=2000):
        self.csv_file = os.path.abspath(csv_file)
        self.db_path = os.path.abspath(db_path)
        self.chunk_size = chunk_size
        self.url_column_name = url_column_name
        self.end_of_csv_file_found = False
        self.csv_generator = get_lines_from_csv(self.csv_file)
        self.image_limit = image_limit
        self.html_output_file = os.path.abspath(html_output_file)
        self.html_template = html_template

        # initialise_sqlite_database
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        create_statement = "CREATE TABLE IF NOT EXISTS images(" \
                           "url TEXT UNIQUE," \
                           "count INTEGER," \
                           "share_text TEXT)"
        cur.execute(create_statement)
        conn.commit()
        conn.close()


    # The two functions below primarily split up to aid testing
    def get_image_counts_from_csv_generator(self):
        image_chunk = []
        for i in range(self.chunk_size):
            try:
                next_item = next(self.csv_generator)
                image_chunk.append(next_item)
            except StopIteration as e:
                self.end_of_csv_file_found = True
        urls = [image[self.url_column_name] for image in image_chunk]
        debraced_urls = [remove_matching_braces(u) for u in urls if u != '']
        counts = get_url_counts(debraced_urls)
        return counts

    def update_database(self, images):
        """
        Take a list of images and update the database to reflect them

        :param db_path: Path to database to update
        :param images: List of image distionaries
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        images_to_insert = []
        for image in images:
            count_selector = "SELECT count FROM images WHERE url = '%s'" \
                             % image['url']
            current_count = cur.execute(count_selector).fetchone()
            if current_count:
                current_count = current_count[0]
                # Image is present in database, so update it
                new_count = current_count + image['count']
                if current_count > 1:
                    update_statement = "UPDATE images " \
                                       "SET count = '%i' " \
                                       "WHERE url = '%s'" \
                                       % (new_count, image['url'])
                else:
                    update_statement = "UPDATE images " \
                                       "SET count = '%i', " \
                                       "share_text = 'shares'" \
                                       "WHERE url = '%s'" \
                                       % (new_count, image['url'])
                cur.execute(update_statement)
            else:
                images_to_insert.append(image)
        if images_to_insert:
            insert_list = ["('%s','%s','%s')"
                           % (i['url'],
                              i['count'],
                              i['share_text']) for i in images_to_insert]
            insert_statement = "INSERT INTO images VALUES %s" % ','.join(insert_list)
            cur.execute(insert_statement)
        conn.commit()

    def write_csv_chunk_to_database(self):
        images = self.get_image_counts_from_csv_generator()
        self.update_database(images)

    def write_csv_file_to_database(self):
        while not self.end_of_csv_file_found:
            self.write_csv_chunk_to_database()

    def get_images_from_database(self):
        """
        :param limit: How many rows to return
        :return: A sqlite3 row object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        select = "SELECT * FROM images ORDER BY count DESC LIMIT %i" \
                 % self.image_limit
        images = cur.execute(select).fetchall()
        return images

    def print_images(self):
        images = self.get_images_from_database()
        template = self.load_template()
        rendered = template.render(twitter_images=images)
        with open(self.html_output_file, 'w') as f:
            f.write(rendered)

    def load_template(self):
        template_dir = os.path.join(SOURCE_ROOT, 'templates')
        loader = jinja2.FileSystemLoader(searchpath=template_dir)
        env = jinja2.Environment(loader=loader)
        return env.get_template(self.html_template)

def remove_matching_braces(from_string):
    braces = [('[', ']'), ('{','}'), ('(', ')')]
    debraced_string = from_string
    for pair in braces:
        if from_string:
            if from_string[0] == pair[0] and from_string[-1] == pair[1]:
                debraced_string = from_string[1:-1]
    return debraced_string

def get_url_counts(from_list):
    """
    Given a list of urls, count each one and return an object
    containing this count

    :param from_list: List of urls harvested from csv column,
        without brackets
    :return: List of dictionaries containing url, count and 'share
        text' info (this last to be removed very soon)
    """
    results = []
    for l in from_list:
        image_urls = l.split(', ')
        for image_url in image_urls:
            if image_url != '':
                # Check for an existing result for this url
                url_already_found = False
                for result in results:
                    if result['url'] == image_url:
                        current_count = result['count']
                        result['count'] = current_count + 1
                        result['share_text'] = "shares"
                        url_already_found = True
                if not url_already_found:
                    new_url = {}
                    new_url['url'] = image_url
                    new_url['count'] = 1
                    new_url['share_text'] = "share"
                    results.append(new_url)
    return results

def combine_urls(url_lists):
    """
    Combine multiple lists of URLs into one - make counts add up etc
    This written for multiprocessing and may be used later whern I've proved
    that I can speed things up with it.

    :param url_lists: List of lists of urls
    :return: Combined list of urls
    """
    list_to_return = url_lists[0][:]
    if len(url_lists) > 1:
        for url_list in url_lists[1:]:
            for url in url_list:
                url_found = False
                for l in list_to_return:
                    if url['url'] == l['url']:
                        new_count = l['count'] + url['count']
                        l['count'] = new_count
                        if new_count > 1:
                            l['share_text'] = "shares"
                        url_found = True
                if not url_found:
                    list_to_return.append(url)
    return list_to_return


def main():
    get_arguments()

if __name__ == '__main__':
    main()
