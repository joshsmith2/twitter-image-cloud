from base import *
import sqlite3

class InputTest(GeneralTest):

    def test_exits_if_input_file_does_not_exist(self):
        silly_path = '/tmp/juj/hug/juj/hhh'
        self.assertFalse(os.path.exists(silly_path))
        with self.assertRaises(OSError):
            main.get_lines_from_csv(silly_path)

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
        csv_generator = main.get_lines_from_csv(multi_csv)
        main.convert_csv_to_images(multi_csv, csv_generator)
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
        all_results = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual([('a_url', 5, 'string')], all_results)

        # Initialise database again, check that value's still there
        main.initialise_sqlite_database(self.database)
        _line = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual([('a_url', 5, 'string')], _line)

    def test_can_write_csv_chunks_to_database(self):
        # Generator needs to be at top level.
        # TODO: Make this an object of a class
        _generator = main.get_lines_from_csv(self.test_csv_in)
        main.initialise_sqlite_database(self.database)
        main.write_csv_chunk_to_database(self.database, _generator,
                                         8, 'media_urls')
        sister_pic_url = 'http://pbs.twimg.com/media/B0vMX4nCQAEK63o.jpg'
        penny_pic_url = 'http://pbs.twimg.com/media/B2PlfAkCUAE0886.png'
        line_3 = ('http://pbs.twimg.com/media/Ajxb2c6CQAAzQTg.jpg', 1, 'share')
        sister_pic = (sister_pic_url, 2, 'shares')

        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        db_contents = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual(len(db_contents), 7) # The number of unique URLs
        self.assertEqual(line_3, db_contents[2])
        self.assertEqual(sister_pic, db_contents[-1])

        main.write_csv_chunk_to_database(self.database, _generator,
                                         8, 'media_urls')
        sister_pic_expected = (sister_pic_url,
                               4, 'shares')
        penny_pic_expected = (penny_pic_url, 1, 'share')
        db_contents = cur.execute("SELECT * FROM images").fetchall()
        self.assertEqual(len(db_contents), 10)
        sister_pic_observed = cur.execute("SELECT * FROM images WHERE url = '%s'"
                                          % sister_pic_url).fetchone()
        penny_pic_observed = cur.execute("SELECT * FROM images WHERE url = '%s'"
                                          % penny_pic_url).fetchone()
        self.assertEqual(sister_pic_expected, sister_pic_observed)
        self.assertEqual(penny_pic_expected, penny_pic_observed)

        main.write_csv_chunk_to_database(self.database, _generator,
                                         8, 'media_urls')
        final_pic_url = 'http://pbs.twimg.com/media/777777777777777.png'
        final_pic_expected = (final_pic_url, 1, 'share')
        final_pic_observed = cur.execute("SELECT * FROM images WHERE url = '%s'"
                                         % final_pic_url).fetchone()
        self.assertEqual(final_pic_expected, final_pic_observed)

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