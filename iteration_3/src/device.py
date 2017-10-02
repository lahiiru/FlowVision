import logging
from algorithms.algorithm import *
from logging.config import fileConfig
from cameras import *
import cv2
import time
from config import DevConfig
from algorithms import *

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')

class Device:

    camera = FromFileCamera(DevConfig.VIDEO_DIR + "01.mp4")
    algorithm = ParticleImageVelocimetryAlgorithm()
    communicator = None
    id = ""
    logger = None

    def __init__(self, id):
        self.id = id

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

        self.camera.start()
        self.algorithm.debug=True
        while True :
            frame = self.camera.get_frame()
            if not frame is None:
                self.algorithm.receive_frame(frame)
                self.algorithm.update()

    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device(1)
        device.start()

if __name__ == '__main__':
    Device.main()