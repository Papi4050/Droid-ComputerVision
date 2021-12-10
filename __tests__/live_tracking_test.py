import unittest

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import live_tracking
import serial

# A class in which we test functions of our module
class liveTrackingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img = live_tracking.face_recognition.load_image_file("./__tests__/resources/Luke.jpeg")
        cls.faceCascade = live_tracking.cv2.CascadeClassifier("./__tests__/resources/haarcascade_frontalface_default.xml")


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
        # This is a right turn!
        res_right = live_tracking.calculateTurnInput(driveConfig, 1280, 10, "")
        res_left = live_tracking.calculateTurnInput(driveConfig, 1280, 1270, "")
        self.assertEqual(res_right, "$222027")
        self.assertEqual(res_left, "$333027")



    def test_findObjects(self):
        imgObjects, objectsOut = live_tracking.findObjects(self.img, self.faceCascade)
        self.assertIsNot(imgObjects, self.img)
        self.assertIsNotNone(objectsOut)

    
    def test_findEncodings(self):
        images = []
        images.append(self.img)
        encodeList = live_tracking.findEncodings(images)
        self.assertIsNotNone(encodeList)


    def test_findCenter(self):
        faceObjects = [330, 178, 208, 208]
        cx, cy, imgObjects = live_tracking.findCenter(self.img, faceObjects)
        self.assertNotEqual(cx, -1)
        self.assertNotEqual(cy, -1)


if __name__ == "__main__":
    unittest.main()