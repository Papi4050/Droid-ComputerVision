import os

def createImageDir():
    path = './Images'

    if os.path.isdir(path) is not True:
        os.makedirs(path)