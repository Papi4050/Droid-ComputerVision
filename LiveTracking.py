'''
This file is a collection of functions used
to provide live tracking funcitonality.

They include methods to configure the environment correctly, recognize faces,
and track those faces in a given live-feed. Additionally, the software will
provide an accurate meassurement of the location of the face in the frame
and display the off-set.
'''

import cv2
import numpy as np
import face_recognition
import os
import platform


path = 'Images'
images = []
classNames = []
myList = os.listdir(path)


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


def get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=0):
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture
    video from the camera on a Jetson Nano.
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, '+ 
            f'height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )


# Get name of faces in the folder
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)


# Get all encodings from the faces in the folder
def findEncodings(images):
    '''
    Parameters
    ----------
    images : photo files
        The image that contains one or more faces

    Returns
    -------
    encodeList: list
        A list of 128-dimensional face encodings (one for each face in the image)
    '''
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)  # Images is empty
print('Encoding Complete')


def findCenter(imgObjects, objects):
    '''
    Parameters
    ----------
    imgObjects : image file
        Current frame seen by live-feed with known face

    objects : list
        A list of tuples of found face locations in css (top, right, bottom, left) order

    Returns
    -------
    cx : float
        Off-center information of knonwn face in x-direction
    cy : float
        Off-center information of knonwn face in y-direction
    imgObjects : image file
        Current frame seen by live-feed with known face including off-center information
    '''
    cx, cy = -1, -1
    if len(objects) != 0:
        y1, x2, y2, x1 = objects
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4  # Multiply by 4 to account for image scaling from above
        cx = x1 + ((x2-x1)/2)
        cy = y1 + ((y2-y1)/2)
        cv2.circle(imgObjects, (int(cx), int(cy)), 2, (0, 255, 0), cv2.FILLED)
        ih, iw, ic = imgObjects.shape
        cv2.line(imgObjects, (int(iw//2), int(cy)), (int(cx), int(cy)), (0, 255, 0), 1)
        cv2.line(imgObjects, (int(cx), int(ih//2)), (int(cx), int(cy)), (0, 255, 0), 1)
    return cx, cy, imgObjects


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


while True:
    success, img = cap.read()
    # Scale image to .25 optimize processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Get faces in current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    # Encode faces in current frame
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # Check current faces in frame for similarity
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        # Get distance for faces in current frame
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # Will simply select the lowest match
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            # Match Name and convert to upper
            name = classNames[matchIndex].upper()
            # Get location of faces in the frame (top, right, bottom, left)
            y1, x2, y2, x1 = faceLoc
            # Multiply by 4 to account for image scaling from above
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cx, cy, img = findCenter(img, faceLoc)
            print(name)

            # Draw identifier on image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            h, w, c = img.shape
            cv2.line(img, (int(w/2), 0), (int(w//2), int(h)), (255, 0, 255), 1)
            cv2.line(img, (0, int(h//2)), (int(w), int(h)//2), (255, 0, 255), 1)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
