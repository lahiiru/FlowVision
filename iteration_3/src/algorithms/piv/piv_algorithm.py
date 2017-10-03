import cv2
from cv2 import *
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from iteration_3.src.algorithms.algorithm import Algorithm
from iteration_3.src.utilities import *

logger = logging.getLogger()


class ParticleImageVelocimetryAlgorithm(object, Algorithm):
    def __init__(self, frame_rate):
        Algorithm.__init__(self)
        self.current = None
        self.current_mask = None
        self.start_y = 50
        self.end_y = 250
        self.start_x = 340
        self.end_x = 520
        self.frame_rate = frame_rate
        self.white_threshold = 0.8
        self.count = 0
        logger.info("PIV Algorithm initiated.")

    def configure(self, frame_rate, start_y=20, end_y=440, start_x=340, end_x=520):
        self.frame_rate = frame_rate
        self.start_y = start_y
        self.end_y = end_y
        self.start_x = start_x
        self.end_x = end_x
        logger.info("PIV Algorithm configured.")

    def receive_frame(self, frame):
        self.prev = self.current
        self.current = frame

        self.prev_mask = self.current_mask
        current_fg_mask = Filters.background_substractor_filter(frame)
        self.current_mask = Filters.morphological_opening_filter(current_fg_mask)

    def update(self, **kwargs):
        return self.match_template()

    def match_template(self):
        if self.prev is None:
            return self.pixels_per_second

        self.current_mask = Filters.illumination_filter(self.current, self.current_mask)

        template = self.prev_mask[self.start_y:self.end_y, self.start_x:self.end_x]
        features = (template > 0)
        white_pixel_count = cv2.countNonZero(template[features])
        total = template.shape[:2][0] * template.shape[:2][1]
        white_percentage = white_pixel_count * 100.0 / total

        if self.debug:
            self.prev_display = self.prev
            self.current_display = self.current
            self.current_display = Filters.apply_mask_filter(self.current_display, self.current_mask)
            self.prev_display = Filters.apply_mask_filter(self.prev_display, self.prev_mask)

        if white_percentage > self.white_threshold:
            correlation_values = cv2.matchTemplate(self.current_mask, template, method=cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
            ref_point_x = self.start_x
            x_distance = maxLoc[0] - ref_point_x
            self.pixels_per_second = x_distance * self.frame_rate
            self.cluster()

            if self.debug:
                self.prev_display = cv2.rectangle(self.prev_display, (self.start_x, self.start_y),
                                                  (self.end_x, self.end_y), (255, 255, 0), 1)
                self.current_display = cv2.rectangle(self.current_display, (maxLoc[0], maxLoc[1]), (
                    maxLoc[0] + (self.end_x - self.start_x), maxLoc[1] + (self.end_y - self.start_y)),
                                                     (255, 255, 0), 1)
                display_text=str(x_distance)
        else:
                display_text='Template rejected'

        if self.debug:
            self.visualization = np.hstack((self.current_display, self.prev_display))
            self.visualization = cv2.putText(self.visualization,display_text , (10, 50),
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 128), 2)
        return self.pixels_per_second

    def cluster(self):
        data_set = np.argwhere(self.prev_mask > 0)
        db = DBSCAN(eps=3, min_samples=10).fit(data_set)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        clusters = [data_set[labels == i] for i in xrange(n_clusters_)]
        i = 0
        for c in clusters:
            for p in c:
                cv2.circle(self.prev_display, tuple(p[::-1]), 1, (255, 0, 0), -1)

