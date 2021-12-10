import unittest

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import live_tracking
import serial

# A class in which we test functions of our module
class liveTrackingTest(unittest.TestCase):

    def test_estDistance(self):
        x1 = 10
        x2 = 210
        y1 = 10 
        y2 = 210 
        h = 1280
        w = 720

        res = live_tracking.estDistance(y1, x2, y2, x1, h, w)
        self.assertAlmostEqual(res, 22.55, 3)

    def test_calculateTurnInput(self):
        driveConfig = {
            "left_max":-1,
            "right_max": 1,
            "forward_max": 1,
            "back_max": -1
        }
        ser = serial.Serial()
        res = live_tracking.calculateTurnInput(driveConfig, 1, 1, 1)
        self.assertAlmostEqual(res, ser.write(333027))


if __name__ == "__main__":
    unittest.main()