import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import datetime
import os

try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "..\\01.mp4"

fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

c = cv2.VideoCapture(video_src)
flag, prev = c.read()
prev = cv2.resize(prev, (640, 480))
frame_hieght, frame_width = prev.shape[:2]
prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
print prev.shape

cam_angle = 28
frame_rate = 7
drain_d = 30

ratio = 0.7
grid_columns = 5
grid_rows = 2
grid_height = frame_hieght / grid_rows
grid_width = frame_width / grid_columns
spot_height = int(grid_height * ratio)
spot_width = int(grid_width * ratio)

white_threshold = 5


def speedCalc(avg_d, angle, drain_d, frame_rate, frame_width):
    speed = (avg_d * 2 * drain_d * math.tan(math.radians(angle / 2)) * frame_rate) / frame_width
    return speed


def gridDetails(img, grid_columns, grid_rows, i, j):
    frame_hieght, frame_width = img.shape[:2]
    grid_height = frame_hieght / grid_rows
    grid_width = frame_width / grid_columns
    return img[j * grid_height:(j + 1) * grid_height, i * grid_width:(i + 1) * grid_width]

#print grid_height, grid_width

while (1):

    rect, frame = c.read()
    frame = cv2.resize(frame, (640, 480))
    if not rect:
        cv2.destroyAllWindows()
        break
    raw_frame = frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    frame = fgmask
    raw_frame = frame


    def spotMatching(i, j, spot_height, spot_width, grid_rows, grid_columns):
        startIndex_h = (grid_height / 2) - spot_height / 2
        endIndex_h = (grid_height / 2) + spot_height / 2
        startIndex_w = (grid_width / 2) - spot_width / 2
        endIndex_w = (grid_width / 2) + spot_width / 2
        template = gridDetails(frame, grid_columns, grid_rows, i, j)[startIndex_h:endIndex_h, startIndex_w:endIndex_w]
        res = cv2.matchTemplate(gridDetails(prev, grid_columns, grid_rows, i, j), template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        return maxLoc, startIndex_w, startIndex_h, endIndex_h, endIndex_w, template


    for i in range(1, grid_columns):
        frame = cv2.line(frame, (grid_width * i, 0), (grid_width * i, frame_hieght), (255, 255, 0), 1, cv2.LINE_AA)
    for i in range(1, grid_rows):
        frame = cv2.line(frame, (0, grid_height * i), (frame_width, grid_height * i), (255, 255, 0), 1, cv2.LINE_AA)

    distance_matrix = np.zeros((grid_columns * grid_rows, 2))
    count = 0
    vis = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    for i in range(grid_columns):
        for j in range(grid_rows):

            maxLoc, startIndex_w, startIndex_h, endIndex_h, endIndex_w, spot = spotMatching(i, j, spot_height,
                                                                                            spot_width, grid_rows,
                                                                                            grid_columns)
            ref_point_x = startIndex_w
            ref_point_y = startIndex_h
            x_distance = maxLoc[0] - ref_point_x
            y_distance = maxLoc[1] - ref_point_y
            # print x_distance,y_distance
            x1 = grid_width * i + (grid_width / 2)
            y1 = grid_height * j + (grid_height / 2)
            a = (spot > 250)
            white = cv2.countNonZero(spot[a])
            tot = spot.shape[:2][0] * spot.shape[:2][1]
            perc = white * 1000.0 / tot

            font = cv2.FONT_HERSHEY_SIMPLEX
            if (perc > white_threshold):
                inst_x_speed = speedCalc(x_distance, cam_angle, drain_d, frame_rate, frame_width)
                inst_y_speed = speedCalc(y_distance, cam_angle, drain_d, frame_rate, frame_hieght)
                # print inst_x_speed, inst_y_speed
                text = 'Speed_x: %d cm/s\nSpeed_y: %d cm/s' % (inst_x_speed, inst_y_speed)
                for row, txt in enumerate(text.split('\n')):
                    vis = cv2.putText(vis, txt, (grid_width * i + 1, (grid_height * j + 20) + 25 * row), font, 0.4,
                                      (255, 255, 128), 1)
                vis = cv2.line(vis, (x1, y1), (x1 - x_distance, y1), (255, 255, 128), 2, cv2.LINE_8)
                vis = cv2.line(vis, (x1, y1 - y_distance), (x1, y1), (255, 0, 255), 2, cv2.LINE_8)
                vis = cv2.rectangle(vis, (startIndex_w, startIndex_h), (endIndex_w, endIndex_h), (255, 0, 0), 1)
            distance_matrix[count, 0] += x_distance
            distance_matrix[count, 1] += y_distance
            count += 1

    prev = frame

    cv2.imshow('frame', vis)
    ch = cv2.waitKey(int(1000.0 / frame_rate))
    if ch == 27:
        cv2.destroyAllWindows()
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
c.release()
