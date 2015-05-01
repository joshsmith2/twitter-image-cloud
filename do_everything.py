#!/usr/bin/env python3

import main
import os

in_file = os.path.abspath('/twitter_image_cloud/files/csv/Final data from BBC debate.csv')
out_file = os.path.abspath('/twitter_image_cloud/live.html')
main.print_index(in_file, output_file=out_file)