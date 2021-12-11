import unittest
import os
import sys
import droidvision

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# A class in which we test functions of our module
class droidvisionTest(unittest.TestCase):

    # Test function goes here
    def test_input_parser(self):
        # TODO: Fill test
        config_list = []


if __name__ == "__main__":
    unittest.main()
