#!/usr/bin/env python3

import main
import os

in_file = os.path.abspath('/twitter_image_cloud/files/csv/motherlode.csv')
out_file = os.path.abspath('/twitter_image_cloud/motherlode.html')
main.print_index(in_file, output_file=out_file)