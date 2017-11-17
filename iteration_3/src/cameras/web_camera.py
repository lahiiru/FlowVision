from camera import AbstractCamera
import cv2
import logging

logger = logging.getLogger()


class WebCamera(AbstractCamera):

    def __init__(self, index):
        AbstractCamera.__init__(self)
        self.cam_index = index
        logger.debug("Web camera initiated.")

    def get_name(self):
        return 'Web Camera'

    def _process(self):
        self.cap = cv2.VideoCapture(self.cam_index)
        frame_width, frame_height = 640, 480  # 2048, 1536 or 640, 480

        # say cameras to adjust resolution
        self.cap.set(3, frame_width)
        self.cap.set(4, frame_height)
        # see whether cameras has adjusted the resolution
        self.resolution = (int(self.cap.get(3)), int(self.cap.get(4)))

        while True:
            r, img = self.cap.read()
            if not r:
                logger.warn("Corrupted frame found. Exiting. ")
                break
            img = cv2.resize(img, self.resolution)
            self._put_frame(img)

    def _release(self):
        self.cap.release()

