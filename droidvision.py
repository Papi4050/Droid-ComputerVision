import argparse
import configparser
import sys
import train_face as tf
import live_tracking


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

    # CONNECTION
    portNo = (my_config['CONNECTION']['port_no'])
    baudRate = int(my_config['CONNECTION']['baud_rate'])

    config_list = [imagePath, portNo, baudRate]

    return config_list


def main():
    my_args = input_parser()

    config_args = config_input()
    imagePath = config_args[0]
    portNo = config_args[1]
    baudRate = config_args[2]

    if my_args.learn is True:
        tf.createImageDir(imagePath)
        tf.captureFace(imagePath)
    else:
        live_tracking.main()

    return 0


if __name__ == "__main__":
    main()
