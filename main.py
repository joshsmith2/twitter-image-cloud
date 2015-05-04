#!/usr/bin/env python3

import os
import argparse
import csv
import jinja2
import sqlite3
from multiprocessing import Pool

SOURCE_ROOT = os.path.dirname(os.path.realpath(__file__))

def get_lines_from_csv(from_file):
    """
    :return: A generator to enable grabbing chunks of files
    """
    with open(from_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def get_chunk_from_csv_generator(_generator, count):
    out_list = []
    for i in range(count):
        next_item = next(_generator)
        out_list.append(next_item)
    return out_list

def initialise_sqlite_database(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    create_statement = "CREATE TABLE IF NOT EXISTS images(" \
                       "url TEXT UNIQUE," \
                       "count INTEGER," \
                       "share_text TEXT)"
    cur.execute(create_statement)
    conn.commit()
    conn.close()

def write_csv_chunk_to_database(csv_file, db_path, chunk_size=1000):
    csv_generator = get_lines_from_csv(csv_file)
    image_chunk = get_chunk_from_csv_generator(csv_generator, chunk_size)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    urls_to_update = []
    urls_to_insert = []
    # Read database into list. Might have to change this tactic
    # if we get low on memory
    url_result = cur.execute('SELECT url FROM images').fetchall()
    db_urls = [u[0] for u in url_result]
    # Find out if this url is already in the database
    for image in image_chunk:
        if image['url'] in db_urls:
            urls_to_update.append(image)
        else:
            urls_to_insert.append(image)
    for u in urls_to_update:
        count_selector = "SELECT count FROM images WHERE url = %s" % url['url']
        current_count = cur.execute(count_selector)
        new_count = current_count + url['count']
        if current_count > 1:
            update_statement = "UPDATE images " \
                               "SET count = %i " \
                               "WHERE url = %s" \
                               % (url['count'], url['url'])
        else:
            update_statement = "UPDATE images " \
                               "SET count = %i, " \
                               "share_text = 'shares'" \
                               "WHERE url = %s" \
                               % (url['count'], url['url'])
        cur.execute(update_statement)
    if urls_to_insert:
        insert_list = ["(%s,%s,%s)" % (u['url'],
                                       u['count'],
                                       u['share_text']) for u in urls_to_insert]
        insert_statement = "INSERT INTO images VALUES %s" % ','.join(insert_list)
        cur.execute(insert_statement)
    conn.commit()


## DB SPIKE ENDS HERE

def print_index(input_file, output_file='index.html', template='index.html',
                url_media_column='twitter.tweet/mediaUrls'):
    urls = get_urls_from_csv(input_file, url_media_column)
    template = load_template(template)
    rendered = template.render(twitter_images=urls)
    with open(output_file, 'w') as f:
        f.write(rendered)

def load_template(template_name='index.html'):
    template_dir = os.path.join(SOURCE_ROOT, 'templates')
    loader = jinja2.FileSystemLoader(searchpath=template_dir)
    env = jinja2.Environment(loader=loader)
    return env.get_template(template_name)

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input-csv', metavar='PATH', dest='input_csv',
                   help='CSV file containing urls to images')
    p.add_argument('-o' '--output-file', metavar='PATH', dest='output_file')
    return p.parse_args()

def remove_matching_braces(from_string):
    braces = [('[', ']'), ('{','}'), ('(', ')')]
    debraced_string = from_string
    for pair in braces:
        if from_string:
            if from_string[0] == pair[0] and from_string[-1] == pair[1]:
                debraced_string = from_string[1:-1]
    return debraced_string

def get_urls(from_list):
    results = []
    for l in from_list:
        image_urls = l.split(', ')
        for image_url in image_urls:
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

def get_urls_from_csv(csv_file,
                      url_column_name='twitter.tweet/mediaUrls'):
    """
    Return a list of image paths, given a csv file

    :param csv_file: Path to csv file to get paths from
    :param url_column_name: Name of column containing urls
    :param news_column_name: Name of column name containing relevance data
    :return dict in format {'url':url, 'relevant':bool, 'count':int}
    """
    if not os.path.exists(csv_file):
        raise OSError('Input file %s does not exist' % csv_file)
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        list_urls = [l[url_column_name] for l in reader]
    debraced_urls = [remove_matching_braces(r) for r in list_urls if r]
    thread_pool = Pool(processes=2)
    section_results = thread_pool.map(get_urls, [debraced_urls])
    results = combine_urls(section_results)
    ordered_results = sorted(results, key=lambda r:r['count'], reverse=True)
    return ordered_results

def create_database(db_path, csv_file, url_column_name='twitter.tweet/mediaUrls'):
    pass

def main():
    get_arguments()

if __name__ == '__main__':
    main()
