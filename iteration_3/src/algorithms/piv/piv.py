import cv2
from cv2 import *
import numpy as np
from iteration_3.src.algorithms.algorithm import Algorithm


class PIVAlgorithm(object, Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.latest_frame=None
        self.background_subtract = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=True)
        self.prev_background_subtract = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=True)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        self.start_y = 20
        self.end_y = 440
        self.start_x = 340
        self.end_x = 520
        self.frame_rate = 27
        self.white_threshold = 2
        self.count = 0

    def configure(self,frame_rate = 27,start_y = 20,end_y = 440,start_x = 340,end_x = 520):
        self.frame_rate=frame_rate
        self.start_y=start_y
        self.end_y=end_y
        self.start_x=start_x
        self.end_x=end_x

    def receive_frame(self, frame):
        self.prev_frame = self.latest_frame
        self.latest_frame = frame
        self.count += 1

    def update(self,**kwargs):
        self.matchTemplate()

    def matchTemplate(self):

        if(self.count>1):
            self.prev_frame = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
            self.raw_frame = self.latest_frame
            self.current_frame = cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2GRAY)

            self.fg_mask = self.background_subtract.apply(self.current_frame)
            self.current_frame = cv2.morphologyEx(self.fg_mask, cv2.MORPH_OPEN, self.kernel)
            self.prev_fg_mask = self.prev_background_subtract.apply(self.prev_frame)
            self.prev_frame = cv2.morphologyEx(self.prev_fg_mask, cv2.MORPH_OPEN, self.kernel)

            template = self.prev_frame[self.start_y:self.end_y, self.start_x:self.end_x]
            correlation_values = cv2.matchTemplate(self.current_frame, template, method=cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)

            features = (template > 250)
            white_pixel_count = cv2.countNonZero(template[features])
            total = template.shape[:2][0] * template.shape[:2][1]
            white_percentage = white_pixel_count * 100.0 / total
            if white_percentage > self.white_threshold :
                ref_point_x = self.start_x
                ref_point_y = self.start_y
                x_distance = maxLoc[0] - ref_point_x
                y_distance = maxLoc[1] - ref_point_y
                self.pixels_per_second = x_distance*self.frame_rate

                if self.debug :
                    self.prev_frame = cv2.cvtColor(self.prev_frame, cv2.COLOR_GRAY2RGB)
                    self.prev_frame= cv2.rectangle(self.prev_frame, ( self.start_x,self.start_y), (self.end_x,self.end_y), (255, 255, 0), 1)

                    self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_GRAY2RGB)
                    self.current_frame = cv2.rectangle(self.current_frame, (maxLoc[0], maxLoc[1]), (maxLoc[0]+(self.end_x-self.start_x), maxLoc[1]+(self.end_y-self.start_y)),
                                                    (255, 255, 0), 1)
                    vis = np.hstack((self.current_frame,self.prev_frame))
                    vis = cv2.putText(vis, str(x_distance), (10, 50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 128), 2)
                    cv2.imshow('preview window', vis)
                    # ch = cv2.waitKey(int(1000.0 / self.frame_rate))
                    ch = cv2.waitKey(0)

            return self.pixels_per_second