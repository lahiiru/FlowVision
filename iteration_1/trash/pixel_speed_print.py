import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from common import anorm2, draw_str

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "01.mp4"
    
c = cv2.VideoCapture(video_src)

rect, prev = c.read()
prev=cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
values = []
means = []
i=0
while(1):
    rect, frame = c.read()
    raw_frame = frame
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    current = fgmask
    template = prev[20:-20,-300:-100]
    diff=cv2.matchTemplate(current,template,method=cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(diff)
    minVal, maxVal, minLoc, maxLoc = loc

    vis = np.hstack((frame,current))
    draw_str(vis, (20, 20), 'speed: %d' % maxLoc[0])
    cv2.imshow('lk_track', vis)
    
    i+=1
    prev = current   

    ch = cv2.waitKey(143)
    if ch == 27:
        break
    
cv2.destroyAllWindows()
c.release()
