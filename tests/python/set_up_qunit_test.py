import os
try:
    import main
except ImportError:
    import sys
    file_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    sys.path.append(base_dir)
    import main

current_dir = os.path.dirname(os.path.abspath(__file__))
files = os.path.join(current_dir, 'files')
tests = os.path.dirname(current_dir)

test_csv_in = os.path.join(files, 'twitter_sample.csv')

qunit_db_path = os.path.join(files, 'qunit_test_out.db')
qunit_test_file = os.path.join(tests, 'js', 'qunit_test.html')
qunit_cloud = main.ImageCloud(test_csv_in, qunit_db_path,
                        url_column_name='media_urls',
                        html_template='qunit_test.html',
                        html_output_file=qunit_test_file)
qunit_cloud.write_csv_file_to_database()
qunit_cloud.print_images()

merge_db_path = os.path.join(files, 'merge_test.db')
merge_test_file = os.path.join(tests, 'js', 'merge_tests.html')
merge_template = 'merge_tests.html'

merge_cloud = main.ImageCloud(test_csv_in, merge_db_path,
                              url_column_name='media_urls',
                              html_template='merge_tests.html',
                              html_output_file=merge_test_file)
merge_cloud.write_csv_file_to_database()
merge_cloud.print_images()

os.remove(qunit_db_path)
os.remove(merge_db_path)