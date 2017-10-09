import cv2
from cv2 import *
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from iteration_3.src.algorithms.algorithm import Algorithm
from frame_wallet import FrameWallet
from iteration_3.src.utilities import *
import math

logger = logging.getLogger()

UNKNOWN_SPEED = None


class ParticleImageVelocimetryAlgorithm(object, Algorithm):

    def __init__(self, frame_rate):
        Algorithm.__init__(self)
        self.direction_filter = DirectionFilter()
        self.frame_wallet = FrameWallet(2)
        self.frame_rate = frame_rate
        self.white_threshold = 0.8
        self.x_offset = 20
        self.y_offset = 5
        self.debug_vis_text = ""
        self.x_distance = 0
        self.y_distance = 0
        logger.info("PIV Algorithm initiated.")

    def configure(self, frame_rate):
        self.frame_rate = frame_rate
        logger.info("PIV Algorithm configured.")

    def receive_frame(self, frame):
        self.frame_count+=1
        current_fg_mask = Filters.background_substractor_filter(frame)
        current_mask = Filters.morphological_opening_filter(current_fg_mask)
        self.frame_wallet.put_masked_frame(current_mask)
        self.frame_wallet.put_original_frame(frame)


    def update(self, **kwargs):
        self.original_frames = self.frame_wallet.get_original_frames()
        self.masked_frames = self.frame_wallet.get_masked_frames()

        if len(self.original_frames) < self.frame_wallet.wallet_size:
            logger.warn("trying to update before receiving real_frames. returning 0.")
            return UNKNOWN_SPEED

        self._process_pre_filters()

        # if self.debug:
        #     for i in range(self.frame_wallet.wallet_size):
        #         self.original_frames[i] = Filters.apply_mask_filter(self.original_frames[i], self.masked_frames[i])
        #         # clear debug text for the current frames
        #         self.debug_vis_text = ""

        self.pixels_per_second = UNKNOWN_SPEED
        for i in range(self.frame_wallet.wallet_size - 1):
            pixels_per_second = self._match_template(i, i + 1)
            self.get_mode_distance(self.pixel_distances)

        if self.debug:
            for i in range(self.frame_wallet.wallet_size):
                self.original_frames[i]=cv2.resize(self.original_frames[i],(640,480))
            self.visualization = np.hstack(self.original_frames)
            for row, txt in enumerate(self.debug_vis_text.split('\n')):
                self.visualization = cv2.putText(self.visualization, txt, (10, 15 + 15 * row), cv2.FONT_HERSHEY_SIMPLEX,
                                                 0.5, (255, 255, 128), 1)

        return pixels_per_second

    def _process_pre_filters(self):
        for i in range(self.frame_wallet.wallet_size):
            self.masked_frames[i] = Filters.illumination_filter(self.original_frames[i], self.masked_frames[i])

    def _match_template(self, pre_index, current_index):
        template_top_conner_pairs = self._find_good_templates(pre_index)

        if len(template_top_conner_pairs) == 0:
            logger.info("no good templates found, skipping frame")
            return UNKNOWN_SPEED

        for i in range(len(template_top_conner_pairs)):
            (x_min, y_min), template = template_top_conner_pairs[i]
            matching_area = self.find_matching_area(self.masked_frames[current_index],ref_point=(x_min,y_min))
            correlation_values = cv2.matchTemplate(self.masked_frames[current_index], template,
                                                   method=cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
            ref_point_x = x_min
            ref_point_y = y_min
            x_distance = maxLoc[0] - ref_point_x
            y_distance = ref_point_y - maxLoc[1]
            self.update_pixel_distances([x_distance, y_distance])
            self.direction_filter.update((x_distance, y_distance))
            if self.debug:
                self.draw_templates(pre_index=pre_index, current_index=current_index, template=template,
                                    ref_point=(ref_point_x, ref_point_y), match_point=maxLoc, score=maxVal)

        return self.pixels_per_second

    def _find_good_templates(self, pre_index):
        # will store each template with global coordinates of it's top left conner.
        template_top_conner_pairs = []

        # calculate set of template bounds relative to the given image frame
        bounds = self._calculate_template_bounds(self.masked_frames[pre_index])

        if len(bounds) == 0:
            return []

        for i in range(len(bounds)):
            x_min, x_max, y_min, y_max = bounds[i]

            if (x_max - x_min) <= 0 or (y_max - y_min) <= 0:
                logger.warn("unexpected template bounds found. skipping template.")
                return []
            template = (self.masked_frames[pre_index])[y_min:y_max, x_min:x_max]

            if self._template_qa_passed(template):
                template_top_conner_pairs += [[(x_min, y_min), template]]

        return template_top_conner_pairs

    def _template_qa_passed(self, template):
        total = template.size
        if total == 0:
            logger.warn("unexpected template size, 0.")
            return False

        features = (template > 0)
        white_pixel_count = cv2.countNonZero(template[features])
        white_percentage = white_pixel_count * 100.0 / total
        if white_percentage < self.white_threshold:
            logger.info("template white percentage check failed.")
            if self.debug:
                self.debug_vis_text = "Template rejected."
            return False

        return True

    def _calculate_template_bounds(self, frame):
        # array of bounds of templates
        bounds = []
        # obtaining cluster bounds
        cluster_x_min, cluster_x_max, cluster_y_min, cluster_y_max = self.__cluster(frame)
        # placing offsets
        y_max = cluster_y_max + self.y_offset
        x_max = cluster_x_max + self.x_offset
        y_min = cluster_y_min - int(min(self.y_offset, cluster_y_min)[0][0])
        x_min = cluster_x_min - int(min(self.x_offset, cluster_x_min)[0][0])
        # appending bounds
        bounds += [(x_min, x_max, y_min, y_max)]

        return bounds

    def __cluster(self, frame):
        data_set = np.argwhere(frame > 0)
        if not len(data_set):
            return 0, 0, 0, 0
        db = DBSCAN(eps=3, min_samples=10).fit(data_set)
        labels = db.labels_
        self.n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        self.clusters = [data_set[labels == i] for i in xrange(self.n_clusters_)]
        if self.n_clusters_ == 0:
            return 0, 0, 0, 0

        cluster_index = 0
        cluster_size = 0
        i = 0
        for c in self.clusters:
            if cluster_size < c.size:
                cluster_size = c.size
                cluster_index = i
            i += 1
        max_cluster = self.clusters[cluster_index]
        y_min, x_min = np.min(max_cluster, axis=0)
        y_max, x_max = np.max(max_cluster, axis=0)
        # for c in self.clusters:
        #     for p in c:
        #         cv2.circle(self.prev_display, tuple(p[::-1]), 1, (255, 0, 0), -1)

        return x_min, x_max, y_min, y_max

    def draw_templates(self, **kwargs):
        pre_index = kwargs['pre_index']
        current_index = kwargs['current_index']
        template = kwargs['template']
        ref_point = kwargs['ref_point']
        x_ref = ref_point[0]
        y_ref = ref_point[1]
        match_point = kwargs['match_point']
        x_match = match_point[0]
        y_match = match_point[1]
        score = kwargs['score']
        self.original_frames[pre_index] = cv2.rectangle(self.original_frames[pre_index], (x_ref, y_ref),
                                                        (x_ref + template.shape[1], y_ref + template.shape[0]),
                                                        (255, 255, 0), 1)
        self.original_frames[current_index] = cv2.rectangle(self.original_frames[current_index], (x_match, y_match),
                                                            (
                                                                x_match + (template.shape[1]),
                                                                y_match + (template.shape[0])),
                                                            (255, 255, 0), 1)
        self.debug_vis_text += 'Indices :(' + str(pre_index) + str(current_index) + ')\nDistance X : ' + str(
            x_match - x_ref) + '\nDistance Y : ' + str(y_ref - y_match) + '\nMax Score : ' + str(score * 10) + '\n'

    def get_mode_distance(self, distances):
        pass

    def find_matching_area(self,frame,**kwargs):
        ref_point=kwargs['ref_point']
        return frame

    def update_pixel_distances(self, point):
        self.pixel_distances.append(point)

        if self.frame_count >= 100:
            x_distances = zip(*self.pixel_distances)[0]
            y_distances = zip(*self.pixel_distances)[1]
            x_hist = np.histogram(x_distances)
            y_hist = np.histogram(y_distances)

            self.x_distance = (x_hist[1][np.argmax(x_hist[0])] + x_hist[1][np.argmax(x_hist[0]) + 1]) / 2
            self.y_distance = (y_hist[1][np.argmax(y_hist[0])] + y_hist[1][np.argmax(y_hist[0]) + 1]) / 2

            if self.history_pixel_distances.full():
                self.history_pixel_distances.get()

            self.history_pixel_distances.put((round(self.x_distance, 2), round(self.y_distance, 2), len(self.pixel_distances)))

            self.frame_count = 0
            self.pixel_distances = []

    def calculate_pixels_per_second(self):
        self.pixels_per_second = math.sqrt(math.pow(self.x_distance, 2) + math.pow(self.y_distance, 2))*self.frame_rate
