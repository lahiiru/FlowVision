from camera import AbstractCamera
import cv2
import time

class FromFileCamera(AbstractCamera):

    def __init__(self, path):
        AbstractCamera.__init__(self)
        self.path = path
        self.frame_rate = 30

    def run(self):
        cap = cv2.VideoCapture(self.path)
        while True:
            r, img = cap.read()
            time.sleep(1.0/self.frame_rate)
            self._put_frame(img)