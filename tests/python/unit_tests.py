from base import *

class InputTest(GeneralTest):

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

if __name__ == '__main__':
     unittest.main()
