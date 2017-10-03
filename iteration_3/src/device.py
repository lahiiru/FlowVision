import logging
from logging.config import fileConfig
from cameras import *
import time
from config import DevConfig
from algorithms import *
from debuggers import *

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')


class Device:

    camera = FromFileCamera(DevConfig.TEST_VIDEO)
    algorithm = ParticleImageVelocimetryAlgorithm(camera.frame_rate)
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

        self.debugger.start()

    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device(1)
        device.start()


if __name__ == '__main__':
    Device.main()