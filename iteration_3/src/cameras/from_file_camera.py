from camera import AbstractCamera
import cv2
import time
import logging

logger = logging.getLogger()


class FromFileCamera(AbstractCamera):

    def __init__(self, path):
        AbstractCamera.__init__(self)
        self.path = path
        self.frame_rate = 30

    def _process(self):
        self.cap = cv2.VideoCapture(self.path)
        r, img = self.cap.read()

        if not r:
            raise IOError("File not found at " + self.path)

        while True:
            r, img = self.cap.read()
            if not r:
                logger.warn("EOF of video found. Exiting. ")
                break
            img = cv2.resize(img, self.resolution)
            time.sleep(1.0 / self.frame_rate)
            self._put_frame(img)

    def _release(self):
        self.cap.release()

