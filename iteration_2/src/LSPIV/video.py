from config import DevConfig
import sys
import cv2
from core import FrameComparator

debug = True
frame_rate = 7

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = DevConfig.VIDEO_DIR+"01.mp4"

# removing the background
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

c = cv2.VideoCapture(video_src)
flag, prev = c.read()
# resizing the frame to a fixed size of (640, 480)
prev = cv2.resize(prev, (640, 480))
frame_hieght, frame_width = prev.shape[:2]
# converting the frame to gray scale
prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

frame_comparator = FrameComparator(frame_hieght, frame_width, 5, 2)

while (1):
    rect, frame = c.read()
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    frame = fgmask

    if not rect:
        cv2.destroyAllWindows()
        break

    ret = frame_comparator.compare(frame, prev, debug)
    if debug:
        # function returned vis frame
        cv2.imshow('frame', ret)
        ch = cv2.waitKey(int(1000.0 / frame_rate))
        if ch == 27:
            cv2.destroyAllWindows()
            break
    else:
        # function returned distance matrix
        print ret
    prev = frame

c.release()
