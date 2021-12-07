import argparse
import configparser
import sys
import train_face as tf
import live_tracking
import manual_drive
import com_module


def input_parser():
    """
    This function imports all the input arguments needed.

    Returns
    -------
    counter_inputs : 'argparse.Namespace' object
        Convert argument strings to objects and assign them as attributes
        of the namespace. Populates the namespace with the command line inputs
    """

    my_parser = argparse.ArgumentParser()

    my_parser.add_argument(
        '-l',
        '--learn',
        action='store_true',
        help='Initiates learning mode for a new face',
        required=False
    )

    my_parser.add_argument(
        '-n',
        '--name',
        type=str,
        action='store',
        help='Specifies the name for the trained face',
        required='-l' in sys.argv
    )

    my_parser.add_argument(
        '-m',
        '--manual',
        action='store_true',
        help='Initiates manual drive mode',
        required=False
    )

    my_parser.add_argument(
        '-u',
        '--unknown_face',
        action='store_true',
        help='Initiates tracking of unknown face',
        required=False
    )

    counter_inputs = my_parser.parse_args()

    return counter_inputs


def config_input():
    """
    This function imports all parameters from the config file.

    Returns
    -------
    config_list : list
        Returns a list that contains all the arguments from
        the config file.
    """

    config_list = []

    my_config = configparser.ConfigParser()
    my_config.read("./droidvision_config.ini")

    # PATH PARSING
    imagePath = my_config['PATH']['image_path']
    cascadePath = my_config['PATH']['cascade_path']

    # CONNECTION
    portNo = (my_config['CONNECTION']['port_no'])
    baudRate = int(my_config['CONNECTION']['baud_rate'])

    # DRIVECONFIG
    left_max = int(my_config['DRIVECONFIG']['left_max'])
    right_max = int(my_config['DRIVECONFIG']['right_max'])
    forward_max = int(my_config['DRIVECONFIG']['forward_max'])
    back_max = int(my_config['DRIVECONFIG']['back_max'])

    config_list = [imagePath, cascadePath, portNo, baudRate, left_max,
                   right_max, forward_max, back_max]

    return config_list


def main():
    my_args = input_parser()

    config_args = config_input()
    imagePath = config_args[0]
    cascadePath = config_args[1]
    portNo = config_args[2]
    baudRate = config_args[3]
    driveConfig = {"left_max":config_args[4], "right_max":config_args[5],
                   "forward_max":config_args[6], "back_max":config_args[7]}
    
    # Connect to serial communication
    ser = com_module.initSerialConnection(portNo, baudRate)

    if my_args.learn is True:
        tf.createImageDir(imagePath)
        tf.captureFace(imagePath, my_args.name)
    elif my_args.manual is True:
        manual_drive.drive_controller(ser)
    elif my_args.unknown_face is True:
        live_tracking.unknownFaceTrack(ser, cascadePath)
    else:
        live_tracking.knwonFaceTrack(ser, driveConfig)

    return 0


if __name__ == "__main__":
    main()
