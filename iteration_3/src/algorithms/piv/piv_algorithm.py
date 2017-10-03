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
        self.frame_rate = frame_rate
        self.white_threshold = 0.8
        self.x_offset = 20
        self.y_offset = 5
        logger.info("PIV Algorithm initiated.")

    def configure(self, frame_rate):
        self.frame_rate = frame_rate
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

        x_min,x_max,y_min,y_max=self.find_template(self.prev_mask)
        y_max = y_max + self.y_offset
        x_max = x_max + self.x_offset
        if y_min - self.y_offset  < 0:
            y_min = 0
        else:
            y_min = y_min - self.y_offset
        if x_min - self.x_offset  < 0:
            x_min = 0
        else:
            x_min = x_min - self.x_offset

        template = self.prev_mask[y_min:y_max, x_min:x_max]
        features = (template > 0)
        white_pixel_count = cv2.countNonZero(template[features])
        total = template.size
        if total == 0:
            pass
        white_percentage = white_pixel_count * 100.0 / total

        if self.debug:
            self.prev_display = self.prev
            self.current_display = self.current
            self.current_display = Filters.apply_mask_filter(self.current_display, self.current_mask)
            self.prev_display = Filters.apply_mask_filter(self.prev_display, self.prev_mask)

        if white_percentage > self.white_threshold:
            correlation_values = cv2.matchTemplate(self.current_mask, template, method=cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
            ref_point_x = x_min
            x_distance = maxLoc[0] - ref_point_x
            self.pixels_per_second = x_distance * self.frame_rate

            if self.debug:
                self.prev_display = cv2.rectangle(self.prev_display, (x_min, y_min),
                                                  (x_max, y_max), (255, 255, 0), 1)
                self.current_display = cv2.rectangle(self.current_display, (maxLoc[0], maxLoc[1]), (
                    maxLoc[0] + (x_max - x_min), maxLoc[1] + (y_max - y_min)),
                                                     (255, 255, 0), 1)
                display_text='Distance   : ' + str(x_distance) + '\nMax Score : '+ str(maxVal*10)
        else:
                display_text='Template rejected'

        if self.debug:
            self.visualization = np.hstack(( self.prev_display,self.current_display))
            for row, txt in enumerate(display_text.split('\n')):
                self.visualization = cv2.putText(self.visualization, txt, (10, 25 + 25 * row), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 128), 1)

        return self.pixels_per_second

    def find_template(self,frame):
        x_min, x_max, y_min, y_max =self.cluster(frame)
        return x_min,x_max,y_min,y_max

    def cluster(self,frame):
        data_set = np.argwhere(frame > 0)
        if not len(data_set) :
            return 0, 0, 0,0
        db = DBSCAN(eps=3, min_samples=10).fit(data_set)
        labels = db.labels_
        self.n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        self.clusters = [data_set[labels == i] for i in xrange(self.n_clusters_)]
        if self.n_clusters_ == 0:
            return 0, 0, 0,0

        cluster_index=0
        cluster_size=0
        i = 0
        for c in self.clusters:
            if cluster_size < c.size:
                cluster_size=c.size
                cluster_index=i
            i+=1
        max_cluster = self.clusters[cluster_index]
        y_min, x_min = np.min(max_cluster, axis=0)
        y_max, x_max = np.max(max_cluster, axis=0)
        # for c in self.clusters:
        #     for p in c:
        #         cv2.circle(self.prev_display, tuple(p[::-1]), 1, (255, 0, 0), -1)

        return x_min, x_max, y_min, y_max




