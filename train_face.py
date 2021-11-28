import os
import cv2
import time

path = './Images'

def createImageDir(path):
    if os.path.isdir(path) is not True:
        os.makedirs(path)
        print("Dir created!")
    else:
        print("Dir already exist")

def captureFace(path):
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    

    success = True
    count = 0
    while success:
        success,image = cap.read()
        cv2.imwrite(path + "/frame%d.png" % count, image)     # save frame as PNG file   
        #cv2.imwrite(os.path.join(path , '/frame%d.png'),count, image)   
        print('Read a new frame: ', success)
        count += 1
        if count == 10:
            success = False
        time.sleep(1)

createImageDir(path)

captureFace(path)