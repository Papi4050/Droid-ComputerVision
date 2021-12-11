import unittest

import os, sys
import serial


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import manual_drive

# A class in which we test functions of our module
class manualDriveTest(unittest.TestCase):

    def test_drive_controller_on(self):
        ser = serial.Serial()
        key = 100
        
        res = manual_drive.drive_controller_on(key, ser)
        self.assertEqual(res, 0)


    def test_drive_controller_off(self):
        ser = serial.Serial()
        key = 100
        
        res = manual_drive.drive_controller_on(key, ser)
        self.assertEqual(res, 0)

if __name__ == "__main__":
    unittest.main()
