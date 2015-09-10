#!/usr/bin/env python3

import main
import os


in_file = os.path.abspath('/Users/josh/Desktop/Scripts/twitter-image-cloud/tests/python/files/Images.csv')
out_file = os.path.abspath('/Users/josh/Desktop/Scripts/twitter-image-cloud/Images.html')
cloud=main.ImageCloud(csv_file=in_file, html_output_file=out_file, url_column_name='T_URLS',db_path='/tmp/db.db')
cloud.write_csv_file_to_database()
cloud.print_images()
