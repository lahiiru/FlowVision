import logging
from logging.config import fileConfig
from cameras import *
import time
from config import DevConfig
from algorithms import *
from debuggers import *
import cv2

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')


class Device:

    camera = FromVideoCamera(DevConfig.TEST_VIDEO)
    # camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)

    # algorithm = ParticleImageVelocimetryAlgorithm(camera.frame_rate)
    # algorithm = ColorChannelsPIV()
    algorithm = PIVThreeFramesAlgorithm(camera.frame_rate)

    communicator = None
    id = ""
    logger = None
    debugger = None

    def __init__(self, id):
        self.id = id

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

        self.debugger = DisplayDebugger(self)

        self.camera.start()
        time.sleep(5)

        self.algorithm.debug = True
        self.algorithm.visualization_mode = 0

        self.debugger.start()

        while True:
            frame = self.camera.get_frame()
            if frame is not None:
                self.algorithm.receive_frame(frame)
                self.algorithm.update()
                time.sleep(1)

                # cv2.imshow('frame', frame)
                # cv2.waitKey(0)

    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device(1)
        device.start()


if __name__ == '__main__':
    Device.main()