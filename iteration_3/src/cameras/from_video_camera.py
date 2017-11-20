from camera import AbstractCamera
import cv2
import time
import logging

logger = logging.getLogger()


class FromVideoCamera(AbstractCamera):

    def __init__(self, path):
        AbstractCamera.__init__(self)
        self.path = path
        self.frame_rate = 50
        logger.debug("From video camera initiated.")

    def get_name(self):
        return 'From Video Camera'

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
            # logger.debug("Put frame. Queue size :" + str(self.frames.qsize()))

    def _release(self):
        self.cap.release()

    def get_bulk_frames(self, bulk_size):
        self.cap = cv2.VideoCapture(self.path)
        r, img = self.cap.read()

        if not r:
            raise IOError("File not found at " + self.path)

        for i in range(bulk_size):
            r, img = self.cap.read()
            if not r:
                logger.warn("EOF of video found. Exiting. ")
                break

            img = cv2.resize(img, self.resolution)
            self.frame_array.append(img)
            time.sleep(1.0 / self.frame_rate)
            i +=1

        array = self.frame_array[:bulk_size]
        self.frame_array = []
        return array