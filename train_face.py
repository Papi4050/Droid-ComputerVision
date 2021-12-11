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
import system_setup
import face_recognition as fr


def createImageDir(path):
    '''
    This function creates the necessary local directory for the known face
    tracking functionality

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

    return 0


def captureFace(path, name):
    '''
    This functions executes the image capturing process

    Parameters
    ----------
    path : string
        File path to the images folder

    name : string
        Contains the name of the person who is being saved
    '''
    cap = system_setup.configurator()

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

    faceDetected = False
    while not faceDetected:
        # Prepare for taking the photo
        for countdown in range(5, 0, -1):
            print(f'Image will be taking in {countdown} seconds...')
            time.sleep(1)

        # Take the photo
        success, image = cap.read()
        print("Checking if a face was detected within image")

        try:
            fr.face_encodings(image)[0]
            print("Successful photo with face captured!")
            faceDetected = True

        except IndexError:
            print("Face not detected in image, another photo will be taken")
            time.sleep(2)

    final_path = f'{path}/{name}-{uniqueID}.png'
    cv2.imwrite(final_path, image)


def checkFaceInImage(path, name, image):
    '''
    This functions checks if a face is present in the current frame

    Parameters
    ----------
    path : string
        File path to the images folder

    name : string
        Contains the name of the person who is being saved
    '''

    try:
        fr.face_encodings(image)[0]
        print("Successful photo with face captured!")

    except IndexError:
        print("Face not detected in image, another photo will be taken")
        captureFace(path, name)


def main():
    path = './Images'
    name = 'JohnDoe'

    createImageDir(path)
    captureFace(path, name)


if __name__ == "__main__":
    main()
