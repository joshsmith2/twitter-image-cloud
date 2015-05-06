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
db_path = os.path.join(files, 'js_test_out.db')
test_csv_in = os.path.join(files, 'twitter_sample.csv')

qunit_test_file = os.path.join(tests, 'js', 'qunit_test.html')
merge_test_file = os.path.join(tests, 'js', 'merge_tests.html')
merge_template = 'merge_tests.html'

cloud = main.ImageCloud(test_csv_in, db_path,
                        url_column_name='media_urls',
                        html_template='qunit_test.html',
                        html_output_file=qunit_test_file)
cloud.print_images()
cloud.html_template = 'merge_tests.html'
cloud.html_output_file = merge_test_file
cloud.print_images()
