import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import train_face

# A class in which we test functions of our module
class trainFaceTest(unittest.TestCase):

    def test_createImageDir(self):
        path = "./Images"

        res = train_face.createImageDir(path)
        self.assertEqual(res, 0)

if __name__ == "__main__":
    unittest.main()