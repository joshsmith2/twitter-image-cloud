from base import *

class FunctionalTest(GeneralTest):
    def test_whole_process(self):
        main.print_index(self.test_csv_in, self.test_index,
                         url_media_column='media_urls' )
        self.assertTrue(os.path.exists(self.test_index))

if __name__ == '__main__':
     unittest.main()