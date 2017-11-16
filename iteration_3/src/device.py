import sys
import os

# remote debug
if sys.platform == 'linux2':
    REMOTE_IP = '192.168.137.142'
    sys.path.insert(0, '/home/pi/Desktop/FlowVision/iteration_3/src/pycharm-debug.egg')
    import pydevd
    pydevd.settrace(REMOTE_IP, port=8888, stdoutToServer=True, stderrToServer=True)

import logging
from _threading_local import local
from logging.config import fileConfig
from cameras import *
import time
from config import DevConfig
from algorithms import *
from debuggers import *
from utilities import *
from communicators import *
from sensors import *

path = os.path.realpath(__file__)
if '.zip' in path:
    cur_dir = path.rsplit(os.sep, 2)[0]
else:
    cur_dir = path.rsplit(os.sep, 1)[0]

log_path = cur_dir + os.sep + 'logging.ini'

print ("Device initializing from, {0}".format(path))

if __name__ in ['__main__','device']:
    logger = logging.getLogger()
    fileConfig(log_path)

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
    if sys.platform == 'linux2':
        camera = RPiCamera()
        distance_sensor = DistanceOneFeet()
    else:
        camera = FromVideoCamera(DevConfig.VIDEO3)
        distance_sensor = DistanceOneFeet()
        # camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)
        #camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)


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

        self.algorithm.debug = False
        self.algorithm.visualization_mode = 0

        for debugger in self.debuggers:
            debugger.start()

        # self.communicator.start()
        self.meters_per_second = 0

        logger.info("Distance: {0}".format(self.distance_sensor.get_real_time_distance_cm()))
        while True:
            frame = self.camera.get_frame()

            if frame is not None:
                self.algorithm.receive_frame(frame)
                self.algorithm.update()
                # time.sleep(1)

                if(self.algorithm.isPaused):
                    self.debuggers[0].isPaused = True
                    while self.debuggers[0].isPaused:
                        pass
                    self.algorithm.isPaused = False
                self.meters_per_second  = round(Converter.convert_meters_per_second(self.algorithm.get_pixels_per_second()),2)
                if(self.meters_per_second>0):
                    logger.info("Current velocity: " +str(self.meters_per_second) + ' m/s')
                    # print (str(self.meters_per_second) + ' m/s')

                self.meters_per_second  = round(Converter.convert_meters_per_second(self.algorithm.get_pixels_per_second()), 2)
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