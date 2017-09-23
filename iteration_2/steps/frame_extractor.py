import cv2
import os
import shutil
import numpy as np

cap = cv2.VideoCapture(0)
frameNo=0
isWrite = False
seperatChannels = True

while(1):
    r, img = cap.read()
    vis = img
    if seperatChannels:
        h, w = img.shape[:2]
        img = cv2.resize(img, (int(640*0.75), int(480*0.75)))
        b,g,r = cv2.split(img)
        b = cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)
        b[:,:,2]=0
        b[:, :, 1] = 0
        g = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
        g[:, :, 0] = 0
        g[:, :, 2] = 0
        r = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        vis = np.vstack((np.hstack((img,g)),np.hstack((b,r))))
    cv2.imshow('Press S to switch view. C to start/stop capturing frames',vis)

    ch = cv2.waitKey(1)

    if ch & 0xFF == ord('s'):
        seperatChannels = not seperatChannels

    if ch & 0xFF==ord('c'):

        isWrite = not isWrite
        if isWrite:
            frameNo = 0
            if not os.path.isdir('frames'):
                os.mkdir('frames')
            else:
                shutil.rmtree('frames')

    if isWrite:
        cv2.imwrite('frames/' + str(frameNo) + '.jpg', img)
        frameNo += 1