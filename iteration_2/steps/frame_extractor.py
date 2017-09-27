import cv2
import os
import shutil
import numpy as np
import datetime

cap = cv2.VideoCapture(0)
frame_height, frame_width = 2048, 1536

# say camera to adjust resolution
cap.set(3, frame_width)
cap.set(4, frame_height)
# see whether camera has adjusted the resolution
print cap.get(3),cap.get(4)

frameNo=0
isWrite = False
separateChannels = False
record = True
frame_rate = 20

if record:
    if not os.path.isdir('records'):
        os.mkdir('records')

while True:
    r, img = cap.read()
    vis = cv2.resize(img, (640,480))
    if separateChannels:
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
    cv2.imshow('Press S to switch view. C to %s capturing frames'%(['start','stop'][int(isWrite)]),vis)

    ch = cv2.waitKey(1)

    if ch & 0xFF == ord('s'):
        separateChannels = not separateChannels

    if ch & 0xFF==ord('c'):
        isWrite = not isWrite
        cv2.destroyAllWindows()
        if isWrite:
            frameNo = 0
            if not os.path.isdir('frames'):
                os.mkdir('frames')
            else:
                shutil.rmtree('frames')
                os.mkdir('frames')
        else:
            out.release()
    if isWrite:
        if frameNo == 0:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('records\\' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.avi', fourcc,
                                  frame_rate, (img.shape[1], img.shape[0]))
        out.write(img)
        cv2.imwrite('frames/' + str(frameNo) + '.jpg', img)
        frameNo += 1
