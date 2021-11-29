import serial 

def initSerialConnection(portNo, baudRate):
    try:
        ser = serial.Serial(portNo,baudRate,timeout=1)
        print("Device Connected")
        return ser
    except:
        print("Not connected")

if __name__ == "__main__":
    # TODO: set up the port right
    ser = initSerialConnection("//dev/ttyACM0", 115200)
