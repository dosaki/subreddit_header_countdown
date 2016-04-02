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

    # Test configuration #######################################################
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
                'y': 20,
            }
        assert props['colour'] == '250,250,255'
        assert props['font'] == './Montserrat-Regular.otf'

    def test_get_countdown_properties(self):
        conf = SafeConfigParser()
        conf.read('test/settings.cfg')
        props = gci.get_countdown_properties(conf)

        assert props['enabled'] == 'true'
        assert props['target'] == '2016 05 09 17:00:00'
        assert props['pos'] == {
                'x': 535,
                'y': 50,
            }
        assert props['colour'] == '250,250,255'
        assert props['font'] == './Montserrat-Regular.otf'

    # Test Utilities ###########################################################
    def test_fake_time(self):
        date = gci.now("2016 05 09 17:00:00")
        assert date.year == 2016
        assert date.month == 5
        assert date.day == 9
        assert date.hour == 17
        assert date.minute == 0
        assert date.second == 0

    def test_force_number(self):
        assert gci.force_number("a") == 0
        assert gci.force_number("1") == 1
        assert gci.force_number("0") == 0

    def test_parse_rgb_colour(self):
        assert gci.parse_rgb_colour("255,255,255") == {'r':255, 'g':255, 'b':255}
        assert gci.parse_rgb_colour("255,255,255,255") == {'r':255, 'g':255, 'b':255}
        assert gci.parse_rgb_colour("0,0,0") == {'r':0, 'g':0, 'b':0}
        assert gci.parse_rgb_colour("a,b,c") == {'r':0, 'g':0, 'b':0}
        assert gci.parse_rgb_colour("5,b,c") == {'r':5, 'g':0, 'b':0}
        assert gci.parse_rgb_colour("a,5,c") == {'r':0, 'g':5, 'b':0}
        assert gci.parse_rgb_colour("a,b,5") == {'r':0, 'g':0, 'b':5}


    # Test actual stuff ########################################################
    def test_remaining_time(self):
        diff = gci.remaining_time(datetime.strptime("2016 05 09 17:00:00", '%Y %m %d %H:%M:%S'), "2016 05 09 17:00:00")
        assert diff['seconds'] == "00"
        assert diff['minutes'] == "00"
        assert diff['hours'] == "00"
        assert diff['days'] == 0

        diff2 = gci.remaining_time(datetime.strptime("2016 05 09 17:00:00", '%Y %m %d %H:%M:%S'), "2016 05 08 10:30:20")
        assert diff2['seconds'] == 40
        assert diff2['minutes'] == 29
        assert diff2['hours'] == "06"
        assert diff2['days'] == 1

    def test_makes_image_countdown(self):
        image = gci.apply_text_on_image("./header.png", {
            'seconds': 0,
            'minutes': 0,
            'hours': 0,
            'days': 0
        }, "./Montserrat-Regular.otf", {'x':535, 'y':50}, "250,250,255")
        image.save('test/result.png')

        assert os.path.exists('test/result.png')
        os.remove('test/result.png')

if __name__ == '__main__':
    unittest.main()
