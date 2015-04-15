#!/usr/bin/env python3

import argparse

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input-csv', metavar='PATH', dest='input_csv',
                   help='CSV file containing urls to images')
    return p.parse_args()

def main():
    get_arguments()

if __name__ == '__main__':
    main()
