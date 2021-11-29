'''
This file is a collection of functions used to provide
the image capturing mechanism required for recognizing faces in LiveTracking.py.

This includes the creation of a standard folder in which the files will be saved in,
and a protocol to collect a predetermined amount of pictures with a uniqueID.
'''


import os
import cv2
import time

path = './Images'

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

def captureFace(path):
    '''
    Parameters
    ----------
    path : string
        File path to the images folder
    '''
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

    faceNames.sort()
    print(faceNames)

    if not faceNames:
        uniqueID = 0
    else:
        temp = faceNames[-1].split('-')
        uniqueID = int(temp[1]) + 1

    success = True
    count = 0
    while success:
        success,image = cap.read()
        cv2.imwrite(path + "/face-%d.png" % uniqueID, image)     # save frame as PNG file 
        print('Read a new frame: ', success)
        count += 1
        uniqueID += 1
        if count == 10:
            success = False
        time.sleep(1)

createImageDir(path)

captureFace(path)