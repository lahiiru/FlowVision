import cv2
from cv2 import *
import numpy as np
import math


class FrameComparator:

    def __init__(self, frame_height, frame_width, grid_columns, grid_rows, ratio=0.7, white_threshold=5, cam_angle=28, frame_rate=7, drain_d=30, raw_values=False , debug=True):
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.grid_columns = grid_columns
        self.grid_rows = grid_rows
        self.grid_height = frame_height / self.grid_rows
        self.grid_width = frame_width / self.grid_columns
        self.spot_height = int(self.grid_height * ratio)
        self.spot_width = int(self.grid_width * ratio)
        self.white_threshold = white_threshold
        self.debug = debug
        self.cam_angle = cam_angle
        self.frame_rate = frame_rate
        self.drain_d = drain_d
        self.raw_values = raw_values

    # this function calculates the speed of flow (cm/s)
    def speedCalc(self, avg_d, angle, drain_d, frame_rate, frame_width):
        speed = (avg_d * 2 * drain_d * math.tan(math.radians(angle / 2)) * frame_rate) / frame_width
        return speed

    # this function returns a region of interest
    def gridDetails(self, img, grid_columns, grid_rows, i, j):
        frame_height, frame_width = img.shape[:2]
        grid_height = frame_height / grid_rows
        grid_width = frame_width / grid_columns
        return img[j * grid_height:(j + 1) * grid_height, i * grid_width:(i + 1) * grid_width]


    # this function matches the selected template in the selected grid from previous frame
    def spotMatching(self, i, j, spot_height, spot_width, grid_rows, grid_columns, current_frame, prev_frame):
        startIndex_h = (self.grid_height / 2) - spot_height / 2
        endIndex_h = (self.grid_height / 2) + spot_height / 2
        startIndex_w = (self.grid_width / 2) - spot_width / 2
        endIndex_w = (self.grid_width / 2) + spot_width / 2
        template = self.gridDetails(current_frame, grid_columns, grid_rows, i, j)[startIndex_h:endIndex_h,
                   startIndex_w:endIndex_w]
        image = self.gridDetails(prev_frame, grid_columns, grid_rows, i, j)
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        return maxLoc, startIndex_w, startIndex_h, endIndex_h, endIndex_w, template

    def compare(self, current_frame, prev_frame, debug=True):
        # draw vertical and horizontal lines in the frames showing the grid selection
        for i in range(1, self.grid_columns):
            current_frame = cv2.line(current_frame, (self.grid_width * i, 0), (self.grid_width * i, self.frame_height), (255, 255, 0),
                                     1, cv2.LINE_AA)
        for i in range(1, self.grid_rows):
            current_frame = cv2.line(current_frame, (0, self.grid_height * i), (self.frame_width, self.grid_height * i), (255, 255, 0),
                                     1, cv2.LINE_AA)

        distance_matrix = np.zeros((self.grid_columns * self.grid_rows, 2))
        count = 0
        vis = np.empty_like(current_frame)
        vis[:] = current_frame
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2RGB)
        for i in range(self.grid_columns):
            for j in range(self.grid_rows):

                maxLoc, startIndex_w, startIndex_h, endIndex_h, endIndex_w, spot = self.spotMatching(i, j, self.spot_height,
                                                                                                     self.spot_width, self.grid_rows,
                                                                                                     self.grid_columns,current_frame,
                                                                                                    prev_frame)
                ref_point_x = startIndex_w
                ref_point_y = startIndex_h
                x_distance = maxLoc[0] - ref_point_x
                y_distance = maxLoc[1] - ref_point_y
                # print x_distance,y_distance
                x1 = self.grid_width * i + (self.grid_width / 2)
                y1 = self.grid_height * j + (self.grid_height / 2)
                a = (spot > 250)
                white = cv2.countNonZero(spot[a])
                tot = spot.shape[:2][0] * spot.shape[:2][1]
                perc = white * 1000.0 / tot

                font = cv2.FONT_HERSHEY_SIMPLEX
                if perc >= self.white_threshold:
                    # calculate the speed for both x and y directions
                    inst_x_speed = self.speedCalc(x_distance, self.cam_angle, self.drain_d, self.frame_rate, self.frame_width)
                    inst_y_speed = self.speedCalc(y_distance, self.cam_angle, self.drain_d, self.frame_rate, self.frame_height)
                    # visualize the speed value and speed vectors in each grid
                    if self.raw_values:
                        text = 'x: %d px\ny: %d px' % (x_distance, y_distance)
                    else:
                        text = 'Speed_x: %d cm/s\nSpeed_y: %d cm/s' % (inst_x_speed, inst_y_speed)
                    for row, txt in enumerate(text.split('\n')):
                        vis = cv2.putText(vis, txt, (self.grid_width * i + 1, (self.grid_height * j + 20) + 25 * row), font, 0.4,
                                          (255, 255, 128), 1)
                    vis = cv2.line(vis, (x1, y1), (x1 - x_distance, y1), (255, 255, 128), 2, cv2.LINE_8)
                    vis = cv2.line(vis, (x1, y1 - y_distance), (x1, y1), (255, 0, 255), 2, cv2.LINE_8)
                    vis = cv2.rectangle(vis, (startIndex_w, startIndex_h), (endIndex_w, endIndex_h), (255, 0, 0), 1)
                distance_matrix[count, 0] += x_distance
                distance_matrix[count, 1] += y_distance
                count += 1

        if debug:
            return vis
        return distance_matrix

