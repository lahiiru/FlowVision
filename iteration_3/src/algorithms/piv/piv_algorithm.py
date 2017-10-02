import cv2
from cv2 import *
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from iteration_3.src.algorithms.algorithm import Algorithm

logger = logging.getLogger()


class ParticleImageVelocimetryAlgorithm(object, Algorithm):
    def __init__(self,frame_rate):
        Algorithm.__init__(self)
        self.latest_frame = None
        self.current_masked_frame = None
        self.current_fg_mask = None
        self.background_subtract = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        self.start_y = 50
        self.end_y = 250
        self.start_x = 340
        self.end_x = 520
        self.frame_rate = frame_rate
        self.white_threshold = 0.8
        self.count = 0
        logger.info("PIV Algorithm initiated.")

    def configure(self, frame_rate,start_y=20, end_y=440, start_x=340, end_x=520):
        self.frame_rate = frame_rate
        self.start_y = start_y
        self.end_y = end_y
        self.start_x = start_x
        self.end_x = end_x
        logger.info("PIV Algorithm configured.")

    def receive_frame(self, frame):
        self.prev_frame = self.latest_frame
        self.latest_frame = frame

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.prev_fg_mask = self.current_fg_mask
        self.current_fg_mask = self.background_subtract.apply(gray_frame)

        self.prev_masked_frame = self.current_masked_frame
        gray_frame = cv2.morphologyEx(self.current_fg_mask, cv2.MORPH_OPEN, self.kernel)
        self.current_masked_frame = gray_frame

    def update(self, **kwargs):
        return self.match_template()

    def match_template(self):

        if self.prev_frame is None:
            return self.pixels_per_second, np.zeros_like(self.latest_frame.shape)
        self.previous_raw_frame = self.prev_frame
        self.raw_frame = self.latest_frame

        updated_fg_mask = self.current_fg_mask / 255
        rgb_mask = np.dstack((updated_fg_mask, updated_fg_mask, updated_fg_mask))
        self.raw_frame = (self.raw_frame * rgb_mask)

        self.prev_fg_mask = self.prev_fg_mask / 255
        rgb_mask = np.dstack((self.prev_fg_mask, self.prev_fg_mask, self.prev_fg_mask))
        self.previous_raw_frame = (self.previous_raw_frame * rgb_mask)

        template = self.prev_masked_frame[self.start_y:self.end_y, self.start_x:self.end_x]
        features = (template > 0)
        white_pixel_count = cv2.countNonZero(template[features])
        total = template.shape[:2][0] * template.shape[:2][1]
        white_percentage = white_pixel_count * 100.0 / total

        if white_percentage > self.white_threshold:
            correlation_values = cv2.matchTemplate(self.current_masked_frame, template, method=cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
            ref_point_x = self.start_x
            ref_point_y = self.start_y
            x_distance = maxLoc[0] - ref_point_x
            y_distance = maxLoc[1] - ref_point_y
            self.pixels_per_second = x_distance * self.frame_rate
            self.cluster()

            if self.debug:
                self.previous_raw_frame = cv2.rectangle(self.previous_raw_frame, (self.start_x, self.start_y),
                                                        (self.end_x, self.end_y), (255, 255, 0), 1)
                self.raw_frame = cv2.rectangle(self.raw_frame, (maxLoc[0], maxLoc[1]), (
                    maxLoc[0] + (self.end_x - self.start_x), maxLoc[1] + (self.end_y - self.start_y)),
                                               (255, 255, 0), 1)
                self.visualization = np.hstack((self.raw_frame, self.previous_raw_frame))
                self.visualization = cv2.putText(self.visualization, str(x_distance), (10, 50),
                                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 128), 2)
                return self.pixels_per_second

        return self.pixels_per_second

    def cluster(self):
        data_set = np.argwhere(self.prev_masked_frame > 0)
        db = DBSCAN(eps=3, min_samples=10).fit(data_set)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        clusters = [data_set[labels == i] for i in xrange(n_clusters_)]
        i = 0
        for c in clusters:
            for p in c:
                cv2.circle(self.previous_raw_frame, tuple(p[::-1]), 1, (255, 0, 0), -1)

        # logger.info("No of clusters : "+str(n_clusters_))
