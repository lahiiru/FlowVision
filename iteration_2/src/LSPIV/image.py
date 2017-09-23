from core import FrameComparator
import cv2
import numpy as np

debug = True
path = '../../resources/double_exposed_webcam/'
frame = cv2.imread(path+'7.jpg')

b,g,r = cv2.split(frame)
prev,frame = b,r
frame_hieght, frame_width = frame.shape[:2]
frame_comparator = FrameComparator(frame_hieght, frame_width, grid_columns=1, grid_rows=2, ratio=0.7, white_threshold=0, raw_values=True)
ret = frame_comparator.compare(frame, prev, debug)
prev = cv2.cvtColor(prev, cv2.COLOR_GRAY2RGB)
frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
vis = np.hstack((ret,frame,prev))
if debug:
    # function returned vis frame
    cv2.imshow('frame', ret)
    cv2.waitKey(0)

else:
    # function returned distance matrix
    print ret


