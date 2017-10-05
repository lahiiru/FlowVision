import cv2
from cv2 import *
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from iteration_3.src.algorithms.algorithm import Algorithm
from iteration_3.src.utilities import *

logger = logging.getLogger()

UNKNOWN_SPEED = None


class ParticleImageVelocimetryAlgorithm(object, Algorithm):

    def __init__(self, frame_rate):
        Algorithm.__init__(self)
        self.current = None
        self.current_mask = None
        self.frame_rate = frame_rate
        self.white_threshold = 0.8
        self.x_offset = 20
        self.y_offset = 5
        self.debug_vis_text = ""
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
        if self.current is None:
            logger.warn("trying to update before receiving frames. returning 0.")
            return UNKNOWN_SPEED

        if self.prev is None:
            logger.warn("trying to update while empty previous frame, returning 0.")
            return UNKNOWN_SPEED

        self.process_pre_filters()

        if self.debug:
            self.current_display = Filters.apply_mask_filter(self.current, self.current_mask)
            self.prev_display = Filters.apply_mask_filter(self.prev, self.prev_mask)
            # clear debug text for the current frame
            self.debug_vis_text = ""

        pixels_per_second = self.match_template()

        if self.debug:
            for row, txt in enumerate(self.debug_vis_text.split('\n')):
                self.visualization = cv2.putText(self.visualization, txt, (10, 25 + 25 * row), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 128), 1)

        return pixels_per_second

    def process_pre_filters(self):
        self.current_mask = Filters.illumination_filter(self.current, self.current_mask)

    def match_template(self):
        template_top_conner_pairs = self.find_good_templates()

        if len(template_top_conner_pairs) == 0:
            logger.info("no good templates found, skipping frame")
            return UNKNOWN_SPEED

        # TODO: Extensible to several templates by iterating bounds array
        (x_min, y_min), template = template_top_conner_pairs[0]

        correlation_values = cv2.matchTemplate(self.current_mask, template, method=cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
        ref_point_x = x_min
        x_distance = maxLoc[0] - ref_point_x

        self.pixels_per_second = x_distance * self.frame_rate

        if self.debug:
            self.prev_display = cv2.rectangle(self.prev_display, (x_min, y_min),
                                              (x_min+template.shape[1], y_min+template.shape[0]), (255, 255, 0), 1)
            self.current_display = cv2.rectangle(self.current_display, (maxLoc[0], maxLoc[1]), (
                maxLoc[0] + (template.shape[1]), maxLoc[1] + (template.shape[0])),
                                                 (255, 255, 0), 1)
            self.debug_vis_text='Distance   : ' + str(x_distance) + '\nMax Score : '+ str(maxVal*10)

            self.visualization = np.hstack(( self.prev_display,self.current_display))
            self.ch = cv2.waitKey(0)

            if self.ch & 0xFF == ord('o'):
                print str(x_distance)+','+str(maxVal*10)+','+str(1)
            if self.ch & 0xFF == ord('r'):
                print str(x_distance)+','+str(maxVal*10)+','+str(0)

        return self.pixels_per_second

    def find_good_templates(self):
        # will store each template with global coordinates of it's top left conner.
        template_top_conner_pairs = []

        # calculate set of template bounds relative to the given image frame
        bounds = self.calculate_template_bounds(self.prev_mask)

        if len(bounds) == 0:
            return []

        # TODO: Extensible to several templates by iterating bounds array
        x_min, x_max, y_min, y_max = bounds[0]

        if (x_max - x_min) <= 0 or (y_max - y_min) <=0:
            logger.warn("unexpected template bounds found. skipping template.")
            return []

        template = self.prev_mask[y_min:y_max, x_min:x_max]

        if self.template_qa_passed(template):
            template_top_conner_pairs += [[(x_min, y_min), template]]

        return template_top_conner_pairs

    def template_qa_passed(self, template):
        total = template.size
        if total == 0:
            logger.warn("unexpected template size, 0.")
            return False

        features = (template > 0)
        white_pixel_count = cv2.countNonZero(template[features])
        white_percentage = white_pixel_count * 100.0 / total
        if  white_percentage < self.white_threshold:
            logger.info("template white percentage check failed.")
            if  self.debug:
                self.debug_vis_text = "Template rejected."
            return False

        return True

    def calculate_template_bounds(self, frame):
        # array of bounds of templates
        bounds = []
        # obtaining cluster bounds
        cluster_x_min, cluster_x_max, cluster_y_min, cluster_y_max = self.cluster(frame)
        # placing offsets
        y_max = cluster_y_max + self.y_offset
        x_max = cluster_x_max + self.x_offset
        y_min = cluster_y_min - int(min(self.y_offset, cluster_y_min)[0][0])
        x_min = cluster_x_min - int(min(self.x_offset, cluster_x_min)[0][0])
        # appending bounds
        bounds += [(x_min, x_max, y_min, y_max)]

        return bounds

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




