from base import *

class FunctionalTest(GeneralTest):

    def test_can_get_help_from_command_line(self):
        output  = str(sp.check_output([self.script, '-h']))
        message = 'show this help message and exit'
        self.assertIn(message, output)

    def test_whole_process(self):
        main.print_index(self.test_csv_in, self.test_index)
        self.assertTrue(os.path.exists(self.test_index))

if __name__ == '__main__':
     unittest.main()