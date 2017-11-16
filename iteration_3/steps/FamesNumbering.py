import cv2
import os
import shutil
import numpy as np
import datetime
import time

cap = cv2.VideoCapture('01.mp4')
frame_height, frame_width = 640, 480 #2048, 1536 or 640, 480

# say camera to adjust resolution
cap.set(3, frame_width)
cap.set(4, frame_height)
# see whether camera has adjusted the resolution
print (cap.get(3),cap.get(4))

frameNo = 0
isWrite = True
separateChannels = False
record = True
frame_rate = 30

if record:
    if not os.path.isdir('records'):
        os.mkdir('records')

while True:
    r, img = cap.read()
    vis = cv2.resize(img, (640,480))
    txt = "hkjhdskjhdk"
    cv2.putText(img, str(frameNo), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                                 1, (255, 255, 128), 1)
    #cv2.imshow('Press S to switch view. C to %s capturing real_frames'%(['start','stop'][int(isWrite)]),vis)

    ch = 1

    if ch & 0xFF == ord('c'):
        isWrite = not isWrite
        cv2.destroyAllWindows()
        if isWrite:
            frameNo = 0
            if not os.path.isdir('real_frames'):
                os.mkdir('real_frames')
            else:
                shutil.rmtree('real_frames')
                time.sleep(2)
                os.mkdir('real_frames')
        else:
            out.release()
    if isWrite:
        if frameNo == 0:
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('records\\' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.avi', fourcc,
                                  frame_rate, (img.shape[1], img.shape[0]))

        
        out.write(img)
        #cv2.imwrite('real_frames/' + str(frameNo) + '.jpg', img)
        frameNo += 1
