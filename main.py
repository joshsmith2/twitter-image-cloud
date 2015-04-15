#!/usr/bin/env python3

import os
import argparse
import csv

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input-csv', metavar='PATH', dest='input_csv',
                   help='CSV file containing urls to images')
    return p.parse_args()

def get_urls_from_csv(csv_file,
                      url_column_name='media_urls',
                      news_column_name='NewsNotNews'):
    """
    Return a list of image paths, given a csv file
r r nvn
    :param csv_file: Path to csv file to get paths from
    :param url_column_name: Name of column containing urls
    :param news_column_name: Name of column name containing relevance data
    :return dict in format {'url':url, 'relevant':bool, 'count':int}
    """
    results = []
    if not os.path.exists(csv_file):
        raise OSError('Input file %s does not exist' % csv_file)
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for an existing result for this url
            url_already_found = False
            for result in results:
                if result['url'] == row[url_column_name]:
                    current_count = result['count']
                    result['count'] = current_count + 1
                    url_already_found = True

            if not url_already_found:
                new_url = {}
                new_url['url'] = row[url_column_name]
                new_url['count'] = 1
                if row[news_column_name].lower() == 'news':
                    new_url['relevant'] = True
                else:
                    new_url['relevant'] = False
                results.append(new_url)
    return results


def main():
    get_arguments()

if __name__ == '__main__':
    main()
