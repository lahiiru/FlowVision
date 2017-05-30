import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

frame_rate = 7

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "01.mp4"
    
c = cv2.VideoCapture(video_src)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) #optional

while(1):
    rect, frame = c.read()
    if not rect:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            #optional
    
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel) #optional

    cv2.imshow('preview window', fgmask)
    
    ch = cv2.waitKey(int(1000.0/frame_rate))

    if ch == 27:
        break

cv2.destroyAllWindows()
c.release()
