import cv2
from cv2 import *
import numpy as np
import logging
from algorithms.piv.piv_algorithm import ParticleImageVelocimetryAlgorithm
from algorithms.piv.frame_wallet import FrameWallet
# from iteration_3.src.utilities import *
from utilities import *
import math
import matplotlib.pyplot as plt



logger = logging.getLogger()
logger.debug('imports done')

UNKNOWN_SPEED = None


class PIVThreeFramesAlgorithm(ParticleImageVelocimetryAlgorithm):
    def __init__(self, frame_rate):
        ParticleImageVelocimetryAlgorithm.__init__(self, frame_rate)
        self.direction_filter = DirectionFilter()
        self.frame_wallet = FrameWallet(3)
        self.x_tolerance = 4
        self.y_tolerance = 4
        self.f_count = 0
        self.count = 0
        self.direction_angles = []
        self.angle = 0
        logger.debug("PIVThreeFrames Algorithm initiated.")

    def get_name(self):
        return 'PIV three frame algorithm '


    def update(self, **kwargs):
        self.original_frames = self.frame_wallet.get_original_frames()
        self.masked_frames = self.frame_wallet.get_masked_frames()

        if len(self.original_frames) < self.frame_wallet.wallet_size:
            logger.warn("trying to update before receiving frames. returning 0.")
            return UNKNOWN_SPEED

        self._process_pre_filters()

        if self.debug:
            for i in range(self.frame_wallet.wallet_size):
                self.original_frames[i] = Filters.apply_mask_filter(self.original_frames[i], self.masked_frames[i])
                # clear debug text for the current frame
                self.debug_vis_text = ""
                self.template_color = (255, 255, 0)

        self.pixels_per_second = UNKNOWN_SPEED
        # for i in range(self.frame_wallet.wallet_size - 1) :

        pixels_per_second = self._match_template(0, 1)

        if self.debug:
            displays = []
            for i in range(self.frame_wallet.wallet_size):
                resized = cv2.resize(self.original_frames[i], (480, 360))
                resized[:, -1, :] = 255
                displays.append(resized)

            self.visualization = np.hstack(displays)
            for row, txt in enumerate(self.debug_vis_text.split('\n')):
                self.visualization = cv2.putText(self.visualization, txt, (10, 15 + 15 * row), cv2.FONT_HERSHEY_SIMPLEX,
                                                 0.5, (255, 255, 128), 1)

        self.f_count = self.f_count + 1
        return pixels_per_second

    def _match_template(self, pre_index, current_index):
        logger.debug("template matching process started")
        template_top_conner_pairs = self._find_good_templates(pre_index)

        if len(template_top_conner_pairs) == 0:
            logger.debug("no good templates found, skipping frame")
            return UNKNOWN_SPEED

        (x_min, y_min), template = template_top_conner_pairs[0]

        correlation_values = cv2.matchTemplate(self.masked_frames[current_index], template, method=cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(correlation_values)
        ref_point_x = x_min
        ref_point_y = y_min
        x_distance = maxLoc[0] - ref_point_x
        y_distance = ref_point_y - maxLoc[1]
        first_location = x_distance, y_distance

        # find the template for the second time
        updated_template = self._find_second_template(1, template, maxLoc)
        correlation_values_updated = cv2.matchTemplate(self.masked_frames[2], updated_template,
                                                       method=cv2.TM_CCOEFF_NORMED)
        n_minVal, n_maxVal, n_minLoc, n_maxLoc = cv2.minMaxLoc(correlation_values_updated)
        ref_x = maxLoc[0]
        ref_y = maxLoc[1]
        n_x_distance = n_maxLoc[0] - ref_x
        n_y_distance = ref_y - n_maxLoc[1]
        second_location = n_x_distance,n_y_distance

        x_value_difference = abs(x_distance - n_x_distance)
        y_value_difference = abs(y_distance - n_y_distance)

        direction_flag = self.find_direction(first_location, second_location)
        # print direction_flag

        avg_x = (x_distance + n_x_distance) / 2
        avg_y = (y_distance + n_y_distance) / 2

        if (avg_x != 0):
            self.angle = np.arctan2(avg_y, avg_x) * 180 / np.pi

            # self.angle = math.degrees(np.arctan(avg_y / avg_x))
            self.direction_angles.append(self.angle)

        # print(self.f_count)
        # if(self.f_count==100):
        #     plt.xlabel("Direction angle")
        #     plt.ylabel("No of matches")
        #     x = self.direction_angles
        #     bins = np.linspace(-10, 10, 100)
        #     plt.hist(x, bins, alpha=0.5)
        #     plt.show()

        if (x_value_difference < self.x_tolerance and y_value_difference < self.y_tolerance and direction_flag ):
            self.matching_distances.append([avg_x, avg_y])
            self.isPaused=True
            # print self.direction_angles

            # if (avg_x != 0):
            #     self.angle = math.degrees(np.arctan(avg_y / avg_x))
            #     self.direction_angles.append(self.angle)

            if(len(self.direction_angles)==30):
                # print self.direction_angles
                plt.xlabel("Direction angle")
                plt.ylabel("No of matches")
                x = self.direction_angles
                bins = np.arange(-180,180,1)
                hist = plt.hist(x, bins, alpha=0.5)
                maxBinUpper = np.argmax(hist[0])
                globalDirection = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2
                # print globalDirection
                #angle_radian = np.deg2rad(globalDirection)
                print ref_x, ref_y
                x,y = self.find_frame_lane(globalDirection,ref_x,ref_y)
                print x,y
                plt.show()

        self.template_color = (255, 0, 255)

        if self.debug:
            self.original_frames[pre_index] = cv2.rectangle(self.original_frames[pre_index], (x_min, y_min),
                                                            (x_min + template.shape[1], y_min + template.shape[0]),
                                                            self.template_color, 1)
            self.original_frames[current_index] = cv2.rectangle(self.original_frames[current_index],
                                                                (maxLoc[0], maxLoc[1]), (
                                                                    maxLoc[0] + (template.shape[1]),
                                                                    maxLoc[1] + (template.shape[0])),
                                                                self.template_color, 1)
            self.original_frames[current_index + 1] = cv2.rectangle(self.original_frames[current_index + 1],
                                                                    (n_maxLoc[0], n_maxLoc[1]), (
                                                                        n_maxLoc[0] + (updated_template.shape[1]),
                                                                        n_maxLoc[1] + (updated_template.shape[0])),
                                                                    self.template_color, 1)

            self.debug_vis_text += 'Distance X : ' + str(
                x_distance) + '\nDistance Y : ' + str(y_distance) + '\nMax Score : ' + str(
                maxVal * 10) + '\n' + '\nDistance X : ' + str(n_x_distance) + '\nDistance Y : ' + str(
                n_y_distance) + '\nMax Score : ' + str(n_maxVal * 10) + '\n'
        logger.debug("end template matching ")

        return self.pixels_per_second

    def _find_second_template(self, current_index, pre_template, maxLoc):
        current_y_min = maxLoc[1]
        current_y_max = maxLoc[1] + pre_template.shape[0]
        current_x_min = maxLoc[0]
        current_x_max = maxLoc[0] + pre_template.shape[1]
        template = (self.masked_frames[current_index])[current_y_min:current_y_max, current_x_min:current_x_max]
        return template

    def find_direction(self, first_location, second_location):

        same_bucket_flag = False
        x1, y1 = first_location
        x2, y2 = second_location
        if(y1==0 or y2==0):
            return same_bucket_flag

        # print x1, y1 , x2, y2
        first_direction = x1 / y1
        second_direction = x2 / y2

        if (first_direction > 0 and second_direction > 0 and y1 > 0 and y2 > 0):
            same_bucket_flag = True
        elif (first_direction > 0 and second_direction > 0 and y1 < 0 and y2 < 0):
            same_bucket_flag = True
        elif (first_direction < 0 and second_direction < 0 and y1 < 0 and y2 < 0):
            same_bucket_flag = True
        elif (first_direction < 0 and second_direction < 0 and y1 > 0 and y2 > 0):
            same_bucket_flag = True

        return same_bucket_flag

    def bulk_receive(self, frames):
        self.matching_distances=[]
        for frame in frames[:3]:
            self.receive_frame(frame)
        for frame in frames[3:]:
            self.receive_frame(frame)
            self.update()
        self.reset_fields()
        return self.matching_distances

    def reset_fields(self):
        self.frame_wallet = FrameWallet(3)
        self.frame_count = 0




