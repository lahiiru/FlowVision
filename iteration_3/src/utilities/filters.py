import cv2


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
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN,Filters.morphological_opening_kernel)


