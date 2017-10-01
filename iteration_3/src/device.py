import logging
from algorithms.algorithm import *
from logging.config import fileConfig

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')

class Device:

    camera = None
    algorithm = Algorithm()
    communicator = None
    id = ""
    logger = None

    def __init__(self, id):
        self.id = id

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device(1)
        device.start()

if __name__ == '__main__':
    Device.main()