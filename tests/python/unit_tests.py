from base import *
import re
import sqlite3

class InputTest(GeneralTest):

    def test_exits_if_input_file_does_not_exist(self):
        silly_path = '/tmp/juj/hug/juj/hhh'
        self.assertFalse(os.path.exists(silly_path))
        with self.assertRaises(OSError):
            main.get_urls_from_csv(silly_path)

    def test_can_get_urls_from_csv_file(self):
        response = main.get_urls_from_csv(self.test_csv_in, 'media_urls')
        expected = [{'url': 'http://pbs.twimg.com/media/AoxQ3CECIAAsArF.jpg',
                     'count': 1,
                      'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B2PlfAkCUAE0886.png',
                     'count': 1,
                    'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg',
                     'count': 5,
                    'share_text': "shares"}]
        for e in expected:
            self.assertIn(e, response)

    def test_brackets_removed(self):
        no_brackets = "husspag"
        observed = main.remove_matching_braces(no_brackets)
        self.assertEqual(no_brackets, observed)

        square_brackets = "[bumbag]"
        observed = main.remove_matching_braces(square_brackets)
        self.assertEqual("bumbag", observed)

    def test_multiple_images_loaded_correctly(self):
        multi_csv = os.path.join(self.files, 'urls_with_multiple_pics.csv')
        response = main.get_urls_from_csv(multi_csv)
        expected = [{'url': 'http://pbs.twimg.com/media/B869DjjCYAAnDg6.jpg',
                     'count': 1,
                     'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B6c2wYAIUAAaoIA.jpg',
                     'count': 1,
                     'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B6c1ulkCYAALNBV.jpg',
                     'count': 1,
                     'share_text': "share"}]
        self.assertEqual(expected, response)

    def test_csv_generator_only_returns_n_elements_raises_stop_iteration(self):
        _generator = main.get_lines_from_csv(self.test_csv_in)
        first_5 = main.get_chunk_from_csv_generator(_generator, 5)
        self.assertEqual(len(first_5), 5)
        self.assertEqual("http://pbs.twimg.com/media/A4nysuNCQAERXAW.jpg", first_5[0]['media_urls'])
        self.assertEqual("http://pbs.twimg.com/media/B05WaEVIQAA9JMu.jpg", first_5[-1]['media_urls'])

        second_5 = main.get_chunk_from_csv_generator(_generator, 5)
        self.assertEqual("http://pbs.twimg.com/media/B0nPH21IIAAeHiw.jpg", second_5[0]['media_urls'])

        # Attempt to consume 20 more to get to the end - there are only 22 in total
        with self.assertRaises(StopIteration):
            main.get_chunk_from_csv_generator(_generator, 20)

class SqliteTests(GeneralTest):
    def test_database_created_once(self):
        self.assertFalse(os.path.exists(self.database))

        main.initialise_sqlite_database(self.database)
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        insert_row = "INSERT INTO images VALUES('a_url','5','string')"
        cur.execute(insert_row) # shouldn't error
        conn.commit()
        # Check that insert worked
        _line = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual([('a_url', 5, 'string')], _line)

        # Initialise database again, check that value's still there
        main.initialise_sqlite_database(self.database)
        _line = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual([('a_url', 5, 'string')], _line)


class JinjaTests(GeneralTest):

    def test_can_render_test_template(self):
        test_template = main.load_template('test.html')
        rendered = test_template.render(worked_goes_here = 'worked')
        self.assertIn("<h1>This has worked</h1>", rendered)

    def test_can_render_loops(self):
        loop_template = main.load_template('loop_test.html')
        felonies = ['pig', 'hog', 'brine']
        rendered = loop_template.render(book=felonies)
        for crime in felonies:
            self.assertIn('<h1>I got %s felonies</h1>' % crime, rendered)


class ImageTests(GeneralTest):

    def test_images_end_up_on_the_page(self):
        urls = main.get_urls_from_csv(self.test_csv_in, 'media_urls')
        index_template = main.load_template()
        rendered = index_template.render(twitter_images=urls)
        tag = '<img src="http://pbs.twimg.com/media/B51oL3fIcAA9j9L.png">'
        self.assertIn(tag, rendered)

    def test_counts_get_there_too(self):
        urls = main.get_urls_from_csv(self.test_csv_in, 'media_urls')
        index_template = main.load_template()
        rendered = index_template.render(twitter_images=urls)
        tag = '<img src="http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg">\n ' \
              '<button class="merge">Merge</button>\n ' \
              '<div class="image-footer">\n '\
              '<div class="share-count">\n ' \
              '<span class="count">5</span> shares'
        rendered_stripped = re.sub(r' +', ' ', rendered)
        self.assertIn(tag, rendered_stripped)

    def test_images_idd_by_rank(self):
        urls = main.get_urls_from_csv(self.test_csv_in, 'media_urls')
        index_template = main.load_template()
        rendered = index_template.render(twitter_images=urls)
        rendered_stripped = re.sub(r' +', ' ', rendered)
        tag = '<div id="item1" class="packery-item">\n ' \
              '<img src="http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg">\n '
        self.assertIn(tag, rendered_stripped)

class ListProcessingTask(GeneralTest):
    def test_lists_can_be_combined(self):
        urls = main.get_urls_from_csv(self.test_csv_in, 'media_urls')
        extra_url = {'url': 'http://www.leekspin.jpg',
                     'count': 89,
                     'share_text': 'shares'}
        urls_plus = urls
        urls_plus.append(extra_url)
        combined = main.combine_urls([urls, urls_plus])
        expected_urls = [extra_url,
            {'url': 'http://pbs.twimg.com/media/AoxQ3CECIAAsArF.jpg',
            'count': 2,
            'share_text': "shares"},
            {'url': 'http://pbs.twimg.com/media/B2PlfAkCUAE0886.png',
             'count': 2,
            'share_text': "shares"},
            {'url': 'http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg',
             'count': 10,
            'share_text': "shares"}]
        for expected_url in expected_urls:
            self.assertIn(expected_url, combined)

if __name__ == '__main__':
     unittest.main()
