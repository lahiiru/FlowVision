import cv2
from cv2 import *
import numpy as np
from iteration_3.src.algorithms.algorithm import Algorithm


class PIVAlgorithm(object, Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.latest_frame=None
        self.background_subtract = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=True)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        self.start_y = 20
        self.end_y = -20
        self.start_x = -300
        self.end_x = -100


    def receive_frame(self, frame):
        self.prev_frame = self.latest_frame
        self.latest_frame = frame

    def update(self,**kwargs):
        print("to be implemented")

    def matchTemplate(self):

        if(self.latest_frame != None and self.prev_frame !=None):
            self.prev_frame = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
            self.raw_frame = self.latest_frame
            self.current_frame = cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2GRAY)
            self.fg_mask = self.background_subtract.apply(self.current_frame)
            self.current_frame = cv2.morphologyEx(self.fg_mask, cv2.MORPH_OPEN, self.kernel)
            self.prev_fg_mask = self.background_subtract.apply(self.prev_frame)
            self.prev_frame = cv2.morphologyEx(self.prev_fg_mask, cv2.MORPH_OPEN, self.kernel)
            template = self.prev_frame[self.start_y:self.end_y, self.start_x:self.end_x]

