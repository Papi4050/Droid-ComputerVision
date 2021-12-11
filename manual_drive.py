import com_module
from pynput import keyboard


'''
This file contains a function used to transfer keyboard inputs 
(up down left and right) to the com module to be sent to R2.
This will be used in case a manual mode is required to control the robot

'''


def drive_controller_on(key, ser):
    '''
    This functions handles all the driving commands

    Parameters
    ----------
    Key : float
        Float value corresponding to the key pressed to control drive controller
        
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
    try:
        #print(key, type(key),key.vk)
        if key.vk == 119:
            print("drive forward")
            com_module.sendData(ser,[111,111],3)
        if key.vk == 97:
            print("drive left")
            com_module.sendData(ser,[222,222],3)
        if key.vk == 115:
            print("drive backward")
            com_module.sendData(ser,[444,444],3)
        if key.vk == 100:
            print("drive right")
            com_module.sendData(ser,[333,333],3)
    except AttributeError:
        print('special key {0} pressed'.format(key))

    # This is the command to send data via the serial terminal
    # 'ser' needs to set to provide connection info
    # 'data' is the information you are trying to send via serial
    # 'digits is transfer length
    #com_module.sendData(ser, data, digits)
    return 0

def drive_controller_off(key, ser):
    print("released")
    com_module.sendData(ser,[000,000],3)
    return 0

def main(ser):
    with keyboard.Listener(on_press=lambda event: drive_controller_on(event,ser), on_release=lambda event:drive_controller_off(event, ser)) as listener:
        listener.join()
#    with keyboard.Listener(
 #       on_press=drive_controller) as listener:
 #       listener.join()

# ...or, in a non-blocking fashion:
 #   listener = keyboard.Listener(
  #      on_press=drive_controller)
  #  listener.start()


if __name__ == "__main__":
    ser = com_module.initSerialConnection("/dev/ttyACM2", 2400)
    # TODO: Is the first variable actually needed? 
    #drive_controller('',ser)  
    main(ser)
