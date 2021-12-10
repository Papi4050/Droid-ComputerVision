import cv2
import platform


def running_on_jetson_nano():
    '''
    This function identifies if the code is running on the Jetson Nano

    Returns
    -------
    platform: boolean
        Returns 'True' if the current platform is AARCH64 based.
    '''

    # To make the same code work on a laptop or on a Jetson Nano, we'll detect
    # when we are running on the Nano so that we can access the camera
    # correctly in that case. On a normal Intel laptop, platform.machine()
    # will be "x86_64" instead of "aarch64"
    return platform.machine() == "aarch64"


def get_jetson_gstreamer_source(capture_width=640, capture_height=480,
                                display_width=640, display_height=480,
                                framerate=30, flip_method=0):

    '''
    This function creates an OpenCV-compatible video source description that 
    uses gstreamer to capture video from the camera on a Jetson Nano.

    Parameters
    ----------
    capture_width : int
        Sets webcam capture width

    capture_height : int
        Sets webcam capture height
    
    display_width : int
        Sets display width

    display_heigh : int
        Sets display height

    framerate : int
        Configures the system framerate

    flip_method : int
        Allows the image to be flipped horizontally.
        0 = Standard orientation, 1 = Flipped

    Returns
    -------
    '' : string
        G-streamer configuration based on input parameters
    '''

    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, ' +
            f'height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )


def configurator():
    '''
    This function configures the system based on the hardware architecture
    
    Returns
    -------
    cap : overloaded member function
        Configured function to open video file or a capturing device or a IP video stream for 
        video capturing with API Preference
    '''
    # Initialize webcam
    if running_on_jetson_nano():
        # Accessing the camera with OpenCV on a Jetson Nano requires gstreamer
        # with a custom gstreamer source string
        cap = cv2.VideoCapture(get_jetson_gstreamer_source(),
                               cv2.CAP_GSTREAMER)
        print('Jetson Nano detected!')
    else:
        # Accessing the camera with OpenCV on a laptop just requires passing 
        # in the number of the webcam (usually 0)
        # Note: You can pass in a filename instead if you want to process a
        # video file instead of a live camera stream
        cap = cv2.VideoCapture(0)
        print('Running on laptop!')

    return cap


if __name__ == "__main__":
    configurator()
