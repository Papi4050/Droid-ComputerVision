import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import com_module as cm

# A class in which we test functions of our module
class ComModuleTest(unittest.TestCase):

    def test_sendData_string(self):
        myString = cm.sendData("", "555", 3)
        self.assertEqual(myString, '$005005005')


if __name__ == "__main__":
    unittest.main()
