import os
import sys
import unittest
from datetime import datetime

from ConfigParser import SafeConfigParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

import generate_countdown_image as gci

class TestCsvToJson(unittest.TestCase):

    def test_control(self):
        self.assertTrue(True, 'Control test successful!')

    def test_get_reddit_properties(self):
        conf = SafeConfigParser()
        conf.read('test/settings.cfg')
        props = gci.get_reddit_properties(conf)
        assert props['username'] == 'user'
        assert props['password'] == 'password'
        assert props['subreddit'] == 'subreddit'

    def test_get_image_properties(self):
        conf = SafeConfigParser()
        conf.read('test/settings.cfg')
        props = gci.get_image_properties(conf)
        assert props['location'] == './header.png'

    def test_get_text_properties(self):
        conf = SafeConfigParser()
        conf.read('test/settings.cfg')
        props = gci.get_text_properties(conf)

        assert props['enabled'] == 'true'
        assert props['text'] == 'Hello World! :D'
        assert props['pos'] == {
                'x': 535,
                'y': 50,
            }
        assert props['colour'] == '250,250,255'
        assert props['font'] == './Montserrat-Regular.otf'

    def test_makes_image_countdown(self):
        conf = SafeConfigParser()
        conf.read('test/settings.cfg')

        reddit_cfg = gci.get_reddit_properties(conf)
        image_cfg = gci.get_image_properties(conf)
        countdown_cfg = gci.get_countdown_properties(conf)

        target_datetime = datetime.strptime(countdown_cfg['target'], '%Y %m %d %H:%M:%S')
        timediff = gci.remaining_time(target_datetime)
        image = gci.apply_text_on_image(image_cfg['location'], gci.format_time_simple(timediff), countdown_cfg['font'], countdown_cfg['pos'], countdown_cfg['colour'])
        image.save('test/result.png')

        assert os.path.exists('test/result.png')
        os.remove('test/result.png')

if __name__ == '__main__':
    unittest.main()
