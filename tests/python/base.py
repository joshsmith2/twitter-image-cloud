import unittest
import os
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

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()