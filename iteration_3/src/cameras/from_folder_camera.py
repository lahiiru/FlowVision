from camera import AbstractCamera
import glob
import cv2
import time
import logging
import os


class FromFolderCamera(AbstractCamera):

    def __init__(self, path):
        AbstractCamera.__init__(self)
        self.path = path

    def _process(self):

        if not os.path.isdir(self.path):
            raise IOError("Folder not found at " + self.path)

        for filename in os.listdir(self.path):
            img = cv2.imread(os.path.join(self.path, filename))
            if img is not None:
                self._put_frame(img)

    def _release(self):
        pass

