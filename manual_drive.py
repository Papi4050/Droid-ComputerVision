import com_module
from pynput import keyboard


'''
This file contains a function used to transfer keyboard inputs
(up down left and right) to the com module to be sent to R2.
This will be used in case a manual mode is required to control the robot

'''


def drive_controller_on(key, ser):
    '''
    This functions sends serial commands to the motor driver depending
    on what keyboard keys are pressed

    Parameters
    ----------
    key : listens to the key being pressed and passes along that key

    ser : serial information for when the com_module is called in order
          to send info to the arduino

    Returns
    -------
    None
    '''
    # this listens to see if keys are pressed
    try:
        # if w key is pressed
        if key.vk == 119:
            print("drive forward")
            com_module.sendData(ser, [111, 111], 3)
        # if a key is pressed
        if key.vk == 97:
            print("drive left")
            com_module.sendData(ser, [222, 222], 3)
        # if s key is pressed
        if key.vk == 115:
            print("drive backward")
            com_module.sendData(ser, [444, 444], 3)
        # if d key is pressed
        if key.vk == 100:
            print("drive right")
            com_module.sendData(ser, [333, 333], 3)
    # if special key is pressed such as ctrl or alt
    except AttributeError:
        print('special key {0} pressed'.format(key))

    # This is the command to send data via the serial terminal
    # 'ser' needs to set to provide connection info
    # 'data' is the information you are trying to send via serial
    # 'digits is transfer length
    # com_module.sendData(ser, data, digits)
    return 0


def drive_controller_off(key, ser):
    '''
    This functions sends serial commands to the motor driver to stop
    R2 anytime that a key is released.  This prevents continuous driving

    Parameters
    ----------
    key : listens to the key being pressed and passes along that key

    ser : serial information for when the com_module is called in order
          to send info to the arduino

    Returns
    -------
    None
    '''
    print("released")
    # sends 000, 000 to com module, then to ardunio, stopping R2
    com_module.sendData(ser, [000, 000], 3)
    return 0


def main(ser):
    '''
    This functions starts the keyboard listender and passes keys to
    drive_controller_on and drive_controller_off

    Parameters
    ----------
    ser : serial information for when the com_module is called in order
          to send info to the arduino

    Returns
    -------
    None
    '''
    with keyboard.Listener(on_press=lambda event: drive_controller_on
                           (event, ser),
                           on_release=lambda event:
                           drive_controller_off(event, ser)) as listener:
        listener.join()

# This statement starts the main function if this script is run from
# the terminal


if __name__ == "__main__":
    ser = com_module.initSerialConnection("/dev/ttyACM2", 2400)
    main(ser)
