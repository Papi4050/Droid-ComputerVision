import unittest

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import live_tracking

# A class in which we test functions of our module
class liveTrackingTest(unittest.TestCase):

    def test_estDistance():
        temp = []


if __name__ == "__main__":
    unittest.main()