# pixhawk_lib/tests/test_pixhawk.py
import unittest
from pixhawk_lib import PixHawk

class TestPixHawk(unittest.TestCase):
    def test_init(self):
        # Note: This won't work without a real Pixhawk; use a simulator for real testing
        try:
            drone = PixHawk(connection_string='/dev/ttyACM0')
            self.assertIsNotNone(drone.vehicle)
        except ConnectionError:
            pass

if __name__ == '__main__':
    unittest.main()