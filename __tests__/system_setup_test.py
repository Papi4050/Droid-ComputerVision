import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import system_setup

# A class in which we test functions of our module
class systemSetupTest(unittest.TestCase):

    # Test function goes here


if __name__ == "__main__":
    unittest.main()
