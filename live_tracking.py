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
import system_setup
import com_module


def findObjects(img, objectCascade, scaleF=1.1, minN=4):
    '''
    This functions finds the desired object in the current frame

    Parameters
    ----------
    img : photo frame
        The image that contains one or more faces

    objectCascade : object
        This object contains the specific cascade to find the object

    scaleF : int
        Parameter specifying how much the image size is reduced at each
        image scale (Default = 1.1)

    minN : int
        Minimum possible object size. Objects smaller than that are ignored
        (Default = 4)

    Returns
    -------
    imgObjects : image
        Original frame but with the found objects marked inside a rectangle

    objectsOut : list
        Contains the detected objects as a list of rectangles
    '''
    imgObjects = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    objectsOut = []
    objects = objectCascade.detectMultiScale(imgGray, scaleF, minN)
    for (x, y, w, h) in objects:
        cv2.rectangle(imgObjects, (x, y), (x+w, y+h), (255, 0, 255), 2)
        objectsOut.append([[x, y, w, h], w*h])

    objectsOut = sorted(objectsOut, key=lambda x: x[1], reverse=True)

    return imgObjects, objectsOut


# Get all encodings from the faces in the folder
def findEncodings(images):
    '''
    This functions finds all the encodings for the knownFaceTrack() from the
    created Images folder.

    Parameters
    ----------
    images : photo files
        The image that contains one or more faces

    Returns
    -------
    encodeList: list
        A list of 128-dimensional face encodings (one for each face in
        the image)
    '''
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def findCenter(imgObjects, objects):
    '''
    This function finds the center of the identified face in the given frame.

    Parameters
    ----------
    imgObjects : image file
        Current frame seen by live-feed with known face

    objects : list
        A list of tuples of found face locations in css (top, right, bottom,
        left) order

    Returns
    -------
    cx : float
        Off-center information of knonwn face in x-direction
    cy : float
        Off-center information of knonwn face in y-direction
    imgObjects : image file
        Current frame seen by live-feed with known face including off-center
        information
    '''
    cx, cy = -1, -1
    if len(objects) != 0:
        y1, x2, y2, x1 = objects
        # Multiply by 4 to account for image scaling from above
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cx = x1 + ((x2-x1)/2)
        cy = y1 + ((y2-y1)/2)
        cv2.circle(imgObjects, (int(cx), int(cy)), 2, (0, 255, 0), cv2.FILLED)
        ih, iw, ic = imgObjects.shape
        cv2.line(imgObjects, (int(iw//2), int(cy)), (int(cx), int(cy)),
                 (0, 255, 0), 1)
        cv2.line(imgObjects, (int(cx), int(ih//2)), (int(cx), int(cy)),
                 (0, 255, 0), 1)
    return cx, cy, imgObjects


def estDistance(y1, x2, y2, x1, h, w):
    '''
    This function estimates the distance of the identified face in the frame
    relative to the current camera position. Needs to be calibrated for every
    camera individually.

    Parameters
    ----------
    y1 : int
        Top point of face

    x2 : int
        Right point of face

    y2 : int
        Bottom point of face

    x1 : int
        Left point of face

    h : int
        Height of the original frame

    w : int
        Width of the original frame

    Returns
    -------
    dist : float
        Off-center information of knonwn face in x-direction
    '''
    orig_size = h*w

    y_length = y2 - y1
    x_length = x2 - x1

    area = y_length * x_length
    area_uncovered = orig_size - area

    # 22 = distance measured in inches during trial
    # 860096 = pixels covered at this specific distance
    # This approach is chosen for now to scale distance
    # IS NOT ROBUST but works
    dist = (area_uncovered*22)/860096

    return dist


def findCenterHaar(imgObjects, objects):
    '''
    This function finds the center of the identified face in the given frame.

    Parameters
    ----------
    imgObjects : image file
        Current frame seen by live-feed with known face

    objects : list
        A list of tuples of found face locations in css (top, right, bottom,
        left) order

    Returns
    -------
    cx : float
        Off-center information of knonwn face in x-direction
    cy : float
        Off-center information of knonwn face in y-direction
    imgObjects : image file
        Current frame seen by live-feed with known face including off-center
        information
    '''
    cx, cy = -1, -1
    if len(objects) != 0:
        x, y, w, h = objects[0][0]
        cx = x + w/2
        cy = y + h/2
        cv2.circle(imgObjects, (int(cx), int(cy)), 2, (0, 255, 0), cv2.FILLED)
        ih, iw, ic = imgObjects.shape
        cv2.line(imgObjects, (int(iw//2), int(cy)), (int(cx), int(cy)),
                 (0, 255, 0), 1)
        cv2.line(imgObjects, (int(cx), int(ih//2)), (int(cx), int(cy)),
                 (0, 255, 0), 1)
    return cx, cy, imgObjects


def unknownFaceTrack(ser, cascade_path):
    '''
    This function tracks all faces found across the camera feed.

    Parameters
    ----------
    ser : string
        Contains all serial connection information

    cascade_path : string
        Contains the path to the haar cascade

    objects : list
        A list of tuples of found face locations in css (top, right, bottom,
        left) order
    '''

    cap = system_setup.configurator()

    faceCascade = cv2.CascadeClassifier(cascade_path)

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (0, 0), None, 0.3, 0.3)
        imgObjects, objects = findObjects(img, faceCascade, 1.1, 5)
        cx, cy, imgObjects = findCenterHaar(imgObjects, objects)

        h, w, c = imgObjects.shape
        cv2.line(imgObjects, (int(w/2), 0), (int(w//2), int(h)),
                 (255, 0, 255), 1)
        cv2.line(imgObjects, (0, int(h//2)), (int(w), int(h)//2),
                 (255, 0, 255), 1)

        img = cv2.resize(imgObjects, (0, 0), None, 3, 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def calculateTurnInput(driveConfig, width, cx, ser):
    '''
    Function calculates what serial commands to send to Arduino for turning

    Parameters
    ----------
    driveConfig : string
        Contains all drive configuration (max input values) information

    width : float
        Width of camera screen

    cx : float
        x location of face center on camera screen
    '''

    turn_input = (driveConfig["left_max"] + ((abs(driveConfig["left_max"] -
                                                  driveConfig["right_max"])
                                              / width) * cx))

    if turn_input > .25:
        print("drive left")
        return com_module.sendData(ser, [333, 27], 3)

    elif turn_input < -.25:
        print("drive right")
        return com_module.sendData(ser, [222, 27], 3)

    else:
        print("good enough")
        return com_module.sendData(ser, [000, 000], 3)


def knownFaceTrack(ser, driveConfig):
    '''
    This function tracks only known faces found across the camera feed.

    Parameters
    ----------
    ser : string
        Contains all serial connection information

    driveConfig : string
        Contains all drive configuration (max input values) information

    objects : list
        A list of tuples of found face locations in css (top, right, bottom,
        left) order
    '''

    path = 'Images'
    images = []
    classNames = []
    myList = os.listdir(path)

    # Get name of faces in the folder
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    print(classNames)

    # Create Encodings
    encodeListKnown = findEncodings(images)  # Images is empty
    print('Encoding Complete')

    cap = system_setup.configurator()

    while True:
        success, img = cap.read()
        # Scale image to .25 optimize processing
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Get faces in current frame
        facesCurFrame = face_recognition.face_locations(imgS)
        # Encode faces in current frame
        encodesCurFrame = face_recognition.face_encodings(imgS,
                                                          facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            # Check current faces in frame for similarity
            matches = face_recognition.compare_faces(encodeListKnown,
                                                     encodeFace)
            # Get distance for faces in current frame
            faceDis = face_recognition.face_distance(encodeListKnown,
                                                     encodeFace)
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
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0),
                              cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6),
                            cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)

                h, w, c = img.shape
                cv2.line(img, (int(w/2), 0), (int(w//2), int(h)),
                         (255, 0, 255), 1)
                cv2.line(img, (0, int(h//2)), (int(w), int(h)//2),
                                              (255, 0, 255), 1)

                # Driving calculations
                distance = estDistance(y1, x2, y2, x1, h, w)
                calculateTurnInput(driveConfig, w, cx, ser)

            else:
                print("nofaceeeeeeeeee")
                com_module.sendData(ser, [000, 000], 3)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    ser = com_module.initSerialConnection("/dev/ttyACM2", 19200)
    driveConfig = {
        "left_max": -30,
        "right_max": 30,
        "forward_max": 30,
        "back_max": -30
    }
    knownFaceTrack(ser, driveConfig)
