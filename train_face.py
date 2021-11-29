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

    maxVal = []
    for str in faceNames:
        temp = str.split('-')[1]
        maxVal.append(temp)

    maxVal.sort(key=int)
    print(maxVal)

    if not maxVal:
        uniqueID = 0
    else:
        uniqueID = int(maxVal[-1]) + 1

    success = True
    count = 0
    while success:
        success, image = cap.read()
        cv2.imwrite(path + "/face-%d.png" % uniqueID, image)
        print('Read a new frame: ', success)
        count += 1
        uniqueID += 1
        if count == 10:
            success = False
        time.sleep(1)

def main():
    path = './Images'
    createImageDir(path)
    captureFace(path)

if __name__ == "__main__":
    main()  
