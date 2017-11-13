import logging
from _threading_local import local
from logging.config import fileConfig
from cameras import *
import time
from config import DevConfig
from algorithms import *
from debuggers import *
from utilities import *
from communicator import *

if __name__ == '__main__':
    logger = logging.getLogger()
    fileConfig('logging.ini')


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super(Singleton, cls).__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Device():
    __metaclass__ = Singleton
    camera = FromVideoCamera(DevConfig.VIDEO3)
    # camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)

    # algorithm = ParticleImageVelocimetryAlgorithm(camera.frame_rate)
    # algorithm = ColorChannelsPIV()
    algorithm = PIVThreeFramesAlgorithm(camera.frame_rate)

    # communicator = Communicator()
    id = "FlowMeter-local"
    logger = None
    debuggers = []

    device = None

    def __init__(self, id):
        self.id = id

    def attach_debugger(self, debugger_instance):
        self.debuggers += [debugger_instance]

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

        self.attach_debugger(DisplayDebugger(self))
        # self.attach_debugger(TelnetDebugger(self))

        self.camera.start()
        time.sleep(5)

        self.algorithm.debug = True
        self.algorithm.visualization_mode = 0

        for debugger in self.debuggers:
            debugger.start()

        # self.communicator.start()
        self.meters_per_second = 0

        while True:
            frame = self.camera.get_frame()
            if frame is not None:
                self.algorithm.receive_frame(frame)
                self.algorithm.update()
                # time.sleep(1)
                self.meters_per_second  = round(Converter.convert_meters_per_second(self.algorithm.get_pixels_per_second()),2)
                print (str(self.meters_per_second) + ' m/s')
                # cv2.imshow('frame', frame)
                # cv2.waitKey(0)

    def return_one(self):
        return 1

    @staticmethod
    def main():
        device = Device("FlowMeter-local")
        device.start()


if __name__ == '__main__':
    Device.main()