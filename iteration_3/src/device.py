import logging
from algorithms.algorithm import *
from logging.config import fileConfig

fileConfig('logging.ini')
logger = logging.getLogger()


class Device:

    camera = None
    algorithm = Algorithm()
    communicator = None
    id = ""

    def __init__(self, id):
        self.id = id
        logger.info("Device with id {0} initiated.".format(self.id))

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

    @staticmethod
    def main():
        device = Device(1)
        device.start()

if __name__ == '__main__':
    Device.main()