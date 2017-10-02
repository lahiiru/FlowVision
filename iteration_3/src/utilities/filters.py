import cv2
from cv2 import *


class Filters:
    background_substractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
    morphological_opening_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    def __init__(self):
        pass

    @staticmethod
    def background_substractor_filter(frame):
        return Filters.background_substractor.apply(frame)

    @staticmethod
    def morphological_opening_filter(frame):
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, Filters.morphological_opening_kernel)

    @staticmethod
    def illumination_filter(original_frame, backSub_frame):
        original_frame = cv2.cvtColor(original_frame, cv2.COLOR_RGB2GRAY)
        backSub_frame[original_frame > 250] = 0
        return backSub_frame
