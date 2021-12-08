'''
This file is a collection of functions used
to provide communication functionality.

This includes methods to establish the connection and send data
'''
import serial 

def initSerialConnection(portNo, baudRate):
    '''
    Parameters
    ----------
    portNo : string
        Provides the local port information for the sending device

    baudRate : int
        Defines the serial baudRate

    Returns
    -------
    ser : string
        Connection information
    '''
    try:
        ser = serial.Serial(portNo,baudRate,timeout=100)
        print("Device Connected")
        return ser
    except:
        print("Not connected")


def sendData(se, data, digits):
    '''
    Parameters
    ----------
    se : string
        Provides the local port information for the sending device
    
    data : string
        Contains the data which will be sent 

    digits : int
        Determines transfer length
    '''
    myString = "$"
    for d in data:
        myString += str(d).zfill(digits)
    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("Data Transmission failed!")
    
    return myString


if __name__ == "__main__":
    # TODO: set up the port right
    ser = initSerialConnection("/dev/ttyACM1", 115200)
