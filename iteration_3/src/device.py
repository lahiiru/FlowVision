import logging
from algorithms.algorithm import *
from logging.config import fileConfig
from cameras import *
import cv2
import time
from config import DevConfig

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')

class Device:

    camera = FromFileCamera(DevConfig.VIDEO_DIR+ "01.mp4")
    algorithm = Algorithm()
    communicator = None
    id = ""
    logger = None

    def __init__(self, id):
        self.id = id

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

        self.camera.start()
        time.sleep(10)
        frame = self.camera.get_frame()


    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device(1)
        device.start()

if __name__ == '__main__':
    Device.main()