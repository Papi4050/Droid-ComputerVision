import unittest
import com_module as cm

# A class in which we test functions of our module
class ComModuleTest(unittest.TestCase):

    def sendData(self):
        
        myString = cm.sendData("", 555, 3)
        self.assertEqual(myString, '555')

if __name__ == "__main__":
    unittest.main()