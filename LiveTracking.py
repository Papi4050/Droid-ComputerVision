import cv2
import numpy as np
import face_recognition
import os


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


# Get all encodings from the faces in the folder
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)  # Images is empty
print('Encoding Complete')


def findCenter(imgObjects, objects):
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
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Scale image to .25 optimize processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)  # Get faces in current frame
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # Encode faces in current frame

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # Check current faces in frame for similarity
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # Get distance for faces in current frame
        matchIndex = np.argmin(faceDis)  # Will simply select the lowest match

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()  # Match Name and convert to upper
            y1, x2, y2, x1 = faceLoc  # Get location of faces in the frame (top, right, bottom, left)
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4  # Multiply by 4 to account for image scaling from above

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
