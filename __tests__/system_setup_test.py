import unittest

import os, sys
import platform


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import system_setup

# A class in which we test functions of our module
class systemSetupTest(unittest.TestCase):

    def test_running_on_jetson_nano(self):
        x86 = 'x86_64'
        jetson = "aarch64"

        res = system_setup.running_on_jetson_nano()
        self.assertEquals(res, platform.machine())


if __name__ == "__main__":
    unittest.main()
