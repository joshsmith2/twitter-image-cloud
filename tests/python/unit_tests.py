from base import *
import re

class InputTest(GeneralTest):

    def test_exits_if_input_file_does_not_exist(self):
        silly_path = '/tmp/juj/hug/juj/hhh'
        self.assertFalse(os.path.exists(silly_path))
        with self.assertRaises(OSError):
            main.get_urls_from_csv(silly_path)

    def test_can_get_urls_from_csv_file(self):
        response = main.get_urls_from_csv(self.test_csv_in)
        expected = [{'url': 'http://pbs.twimg.com/media/AoxQ3CECIAAsArF.jpg',
                     'relevant': False,
                     'count': 1},
                    {'url': 'http://pbs.twimg.com/media/B2PlfAkCUAE0886.png',
                     'relevant': True,
                     'count': 1},
                    {'url': 'http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg',
                     'relevant': True,
                     'count': 4}]
        for e in expected:
            self.assertIn(e, response)

    def test_wrong_key_raises_error(self):
        with self.assertRaises(KeyError):
            main.get_urls_from_csv(self.test_csv_in, 'bumbag')

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
        urls = main.get_urls_from_csv(self.test_csv_in)
        index_template = main.load_template()
        rendered = index_template.render(twitter_images=urls)
        tag = '<img src="http://pbs.twimg.com/media/B51oL3fIcAA9j9L.png">'
        self.assertIn(tag, rendered)

    def test_counts_get_there_too(self):
        urls = main.get_urls_from_csv(self.test_csv_in)
        index_template = main.load_template()
        rendered = index_template.render(twitter_images=urls)
        tag = '<img src="http://pbs.twimg.com/media/B4boCpyCEAExIYo.jpg">\n' \
              ' <div class="count">4</div>'
        rendered_stripped = re.sub(r' +', ' ', rendered)
        self.assertIn(tag, rendered_stripped)

if __name__ == '__main__':
     unittest.main()
