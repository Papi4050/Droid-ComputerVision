import argparse
import configparser
import sys


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
