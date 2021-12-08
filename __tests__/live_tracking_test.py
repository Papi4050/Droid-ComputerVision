import unittest

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# A class in which we test functions of our module
class liveTrackingTest(unittest.TestCase):

    # Test function goes here


if __name__ == "__main__":
    unittest.main()