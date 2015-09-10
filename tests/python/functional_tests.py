from base import *

class FunctionalTest(GeneralTest):
    def test_whole_process(self):
        cloud = main.ImageCloud(csv_file=self.test_csv_in,
                                html_output_file=self.test_index,
                                url_column_name='media_urls',
                                db_path='/tmp/db.db')
        cloud.write_csv_file_to_database()
        cloud.print_images()
        # OK this isn't a great test.
        self.assertTrue(os.path.exists(self.test_index))

if __name__ == '__main__':
     unittest.main()