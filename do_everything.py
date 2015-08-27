#!/usr/bin/env python3

import main
import os

in_file = os.path.abspath('/twitter_image_cloud/files/csv/motherlode.csv')
out_file = os.path.abspath('/twitter_image_cloud/motherlode.html')
cloud=main.ImageCloud(csv_file=in_file,html_output_file=out_file)
cloud.print_images()
