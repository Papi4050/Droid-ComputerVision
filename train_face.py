'''
This file is a collection of functions used to provide
the image capturing mechanism required for recognizing faces
in LiveTracking.py.

This includes the creation of a standard folder in which the files will be
saved in, and a protocol to collect a predetermined amount of pictures with a
uniqueID.
'''


import os
import cv2
import time
import platform


def running_on_jetson_nano():
    '''
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


def get_jetson_gstreamer_source(capture_width=1280, capture_height=720,
                                display_width=1280, display_height=720,
                                framerate=60, flip_method=0):
    """
    Return an OpenCV-compatible video source description that uses gstreamer
    to capture video from the camera on a Jetson Nano.
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, ' +
            f'height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )


def createImageDir(path):
    '''
    Parameters
    ----------
    path : string
        File path to the images folder
    '''
    if os.path.isdir(path) is not True:
        os.makedirs(path)
        print("Dir created!")
    else:
        print("Dir already exist")


def captureFace(path, name):
    '''
    Parameters
    ----------
    path : string
        File path to the images folder
    
    name : string
        Contains the name of the person who is being saved
    '''
     # Initialize webcam
    if running_on_jetson_nano():
        # Accessing the camera with OpenCV on a Jetson Nano requires gstreamer
        # with a custom gstreamer source string
        cap = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)
        print('Jetson Nano detected!')
    else:
        # Accessing the camera with OpenCV on a laptop just requires passing in the
        # number of the webcam (usually 0)
        # Note: You can pass in a filename instead if you want to process a video
        # file instead of a live camera stream
        cap = cv2.VideoCapture(0)
        print('Running on laptop!')


    cap = cv2.VideoCapture(0)
    time.sleep(1)

    faceNames = []
    images = []
    myList = os.listdir(path)

    # Get name of faces in the folder
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        faceNames.append(os.path.splitext(cl)[0])

    # Check if name already exists in the files, if name exists, add unique ID
    maxVal = []
    print(faceNames)
    for str in faceNames:
        temp = str.split('-')

        if temp[0] == name:
            maxVal.append(temp[1])
            print(temp[1])

    maxVal.sort(key=int)
    print(f'maxVal = {maxVal}')

    if not maxVal:
        uniqueID = 0
    else:
        uniqueID = int(maxVal[-1]) + 1

    # Prepare for taking the photo
    for countdown in range(5,0,-1):
        print(f'Image will be taking in {countdown} seconds...')
        time.sleep(1)
    
    # Take the photo
    success, image = cap.read()
    final_path = f'{path}/{name}-{uniqueID}.png'
    cv2.imwrite(final_path, image)
    print('New Photo: ', success)

def main():
    path = './Images'
    name = 'JohnDoe'
    
    createImageDir(path)
    captureFace(path, name)

if __name__ == "__main__":
    main()  
