import com_module

def drive_controller():
    # This function only needs to be sent once
    # TODO: Determine proper location for this
    ser = com_module.initSerialConnection("//dev/ttyACM0", 115200)


    # This is the command to send data via the serial terminal
    # 'ser' needs to set to provide connection info
    # 'data' is the information you are trying to send via serial
    # 'digits is transfer length
    com_module.sendData(ser, data, digits)
    return 0


if __name__ == "__main__":
    drive_controller()  
