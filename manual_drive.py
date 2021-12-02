import com_module
from pynput.keyboard import Key, Listener



'''
This file contains a function used to transfer keyboard inputs 
(up down left and right) to the com module to be sent to R2.
This will be used in case a manual mode is required to control the robot

'''


def drive_controller(Key):
    '''
    Parameters
    ----------
    Key : 

    Returns
    -------
    driveValue : int
        This is the value sent to the com_module for the magnitude of how much
        R2 will drive forward or backcommand sent to our control module which will tell
        the robot to go forward or backward
    turnValue : int
        This is the value sent to the com_module for the magnitude of how much
        R2 will drive left or right
    '''
    #this listens to see if keys are pressed
    if Key == keyboard.Key.w:
        print("forward Pressed")
    
    
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
