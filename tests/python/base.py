import unittest
import os
import subprocess as sp
try:
    import main
except ImportError:
    import sys
    file_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    sys.path.append(base_dir)
    import main

class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.dirname(os.path.dirname(self.current_dir))
        self.script = os.path.join(self.base_dir, 'main.py')
        self.minimal_command = [self.script, '-h']
        self.files = os.path.join(self.current_dir, 'files')
        self.test_csv_in = os.path.join(self.files, 'twitter_sample.csv')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()