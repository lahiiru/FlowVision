import cv2
import os
import shutil

cap = cv2.VideoCapture(0)
frameNo=0
isWrite = False

while(1):
    r, img = cap.read()
    cv2.imshow('video',img)

    ch = cv2.waitKey(1)
    if ch & 0xFF==ord('c'):

        isWrite = not isWrite
        if isWrite:
            frameNo = 0
            shutil.rmtree('frames')
            if not os.path.isdir('frames'):
                os.mkdir('frames')

    if isWrite:
        cv2.imwrite('frames/' + str(frameNo) + '.jpg', img)
        frameNo += 1