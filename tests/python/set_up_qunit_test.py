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
js_test_file = os.path.join(tests, 'js', 'qunit_test.html')
merge_test_file = os.path.join(tests, 'js', 'merge_tests.html')
main.print_index(test_csv_in, js_test_file,
                 template='qunit_test.html',
                 url_media_column='media_urls')
main.print_index(test_csv_in, merge_test_file,
                 template='merge_tests.html',
                 url_media_column='media_urls')
