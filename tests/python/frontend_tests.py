from base import *
import re

class DatabaseTests(GeneralTest):

    def setUp(self):
        super().setUp()
        self.cloud = main.ImageCloud(self.test_csv_in,
                                     self.database,
                                     'media_urls')
        self.cloud.write_csv_file_to_database()

    def test_images_load_ok_from_database(self):
        expected = [{'url': 'http://pbs.twimg.com/media/AoxQ3CECIAAsArF.jpg',
                     'count': 1,
                     'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B2PlfAkCUAE0886.png',
                     'count': 1,
                     'share_text': "share"},
                    {'url': 'http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg',
                     'count': 5,
                     'share_text': "shares"}]
        result = self.cloud.get_images_from_database()
        for e in expected:
            match = [r for r in result if r['url'] == e['url']][0]
            self.assertEqual(e['count'], match['count'])

    def test_images_sorted_by_count_from_database(self):
        result = self.cloud.get_images_from_database()
        previous_count = 100000  # Initialise this very high indeed
        for r in result:
            current_count = r['count']
            self.assertLessEqual(current_count, previous_count)
            previous_count = current_count

    def test_can_limit_results_from_db(self):
        self.cloud.image_limit = 2
        result = self.cloud.get_images_from_database()
        self.assertEqual(len(result), 2)


class JinjaTests(DatabaseTests):

    def test_can_render_test_template(self):
        self.cloud.html_template = 'test.html'
        test_template = self.cloud.load_template()
        rendered = test_template.render(worked_goes_here='worked')
        self.assertIn("<h1>This has worked</h1>", rendered)

    def test_can_render_loops(self):
        self.cloud.html_template = 'loop_test.html'
        loop_template = self.cloud.load_template()
        felonies = ['pig', 'hog', 'brine']
        rendered = loop_template.render(book=felonies)
        for crime in felonies:
            self.assertIn('<h1>I got %s felonies</h1>' % crime, rendered)

class ImageTests(DatabaseTests):

    def test_images_end_up_on_the_page(self):
        images = self.cloud.get_images_from_database()
        index_template = self.cloud.load_template()
        rendered = index_template.render(twitter_images=images)
        tag = '<img src="http://pbs.twimg.com/media/B51oL3fIcAA9j9L.png">'
        self.assertIn(tag, rendered)

    def test_counts_get_there_too(self):
        images = self.cloud.get_images_from_database()
        index_template = self.cloud.load_template()
        rendered = index_template.render(twitter_images=images)
        match_string = '<img src="http://pbs\.twimg\.com/media/B4boCpyCEAExIYo\.jpg">' \
                       '(?:(?!img).)*' \
                       '<span class="count">5</span> shares'
        rendered_stripped = re.sub(r' +', ' ', rendered)
        assert(re.search(match_string, rendered_stripped, re.S))

    def test_images_idd_by_rank(self):
        images = self.cloud.get_images_from_database()
        index_template = self.cloud.load_template()
        rendered = index_template.render(twitter_images=images)
        rendered_stripped = re.sub(r' +', ' ', rendered)
        tag = '<div id="item1" class="packery-item">\n ' \
              '<img src="http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg">\n '
        self.assertIn(tag, rendered_stripped)

if __name__ == '__main__':
     unittest.main()
