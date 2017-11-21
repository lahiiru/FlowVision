import sys
import os
remote_debug = False
# remote debug
if sys.platform == 'linux2' and remote_debug:
    REMOTE_IP = '192.168.137.1'
    sys.path.insert(0, '/home/pi/Desktop/FlowVision/iteration_3/src/pycharm-debug.egg')
    import pydevd
    pydevd.settrace(REMOTE_IP, port=8888, stdoutToServer=True, stderrToServer=True)

import logging
import numpy as np
import math
from logging.config import fileConfig
from cameras import *
import time
from config import DevConfig
from algorithms import *
from debuggers import *
from utilities import *
from communicators import *
from sensors import *
from multiprocessing.connection import Listener
import subprocess

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


class Device:
    __metaclass__ = Singleton
    if sys.platform == 'linux2':
        camera = RPiCamera()
        distance_sensor = DistanceOneFeet()
    else:
        camera = FromVideoCamera(DevConfig.TEST_VIDEO)
        # camera = WebCamera(1)
        distance_sensor = DistanceOneFeet()
        # camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)
        # camera = FromFolderCamera(DevConfig.RB_FRAME_DIR)

    id = "FlowMeter-local"
    logger = None
    debuggers = []
    device = None
    multi_processing = False

    if not multi_processing:
        algorithm = PIVThreeFramesAlgorithm(camera.frame_rate)

    communicator = ThingspeakCommunicator()
    # algorithm = ParticleImageVelocimetryAlgorithm(camera.frame_rate)
    # algorithm = ColorChannelsPIV()

    def __init__(self, id):
        self.id = id
        self.clk = 0
        self.sch_index = 0
        self.meters_per_second = 0
        self.frame_buff = []
        self.lot = 100
        self.x_distance =0
        self.y_distance = 0
        self.frame_nos = ()
        self.pixels_per_second = 0
        self.x_distances = []
        self.y_distances = []
        self.distance = 1

        try:
            self.listener_1 = Listener(('localhost', 7000), authkey=b'secret password')
        except:
            logger.warn("Listener at {0} couldn't started.", 7000)
        try:
            self.listener_2 = Listener(('localhost', 7001), authkey=b'secret password')
        except:
            logger.warn("Listener at {0} couldn't started.", 7001)

    def frames_count_up(self):
        self.sch_index += 1

    def frames_count_reset(self):
        self.sch_index = 0

    def peek_sch_index(self):
        return self.sch_index

    def put_frame_in_buffer(self, frame):
        self.frames_count_up()
        self.frame_buff += [frame]

    def frames_buffer_clear(self):
        del self.frame_buff
        self.frame_buff = []

    def get_frame_buffer(self):
        return self.frame_buff

    def attach_debugger(self, debugger_instance):
        self.debuggers += [debugger_instance]

    def start(self):
        logger.info("Device with id {0} started.".format(self.id))
        # TODO: add your test code

        self.attach_debugger(DisplayDebugger(self))
        # self.attach_debugger(TelnetDebugger(self))

        # self.camera.start()
        time.sleep(5)
        self.algorithm.debug = False
        self.algorithm.visualization_mode = 0

        # for debugger in self.debuggers:
        #     debugger.start()

        # self.communicator.start()

        logger.info("Distance: {0}".format(self.distance_sensor.get_real_time_distance_cm()))
        logger.info(cur_dir)

        logger.info("{0} platform detected.".format(sys.platform))

        if sys.platform == 'win32':
            for script in ["processor_1.py", "processor_2.py"]:
                script_path = cur_dir + os.sep + script
                logger.info("starting sub-processes from : {0}".format(script_path))
                _proc = subprocess.Popen(["python", script_path])
                logger.info("started {0} with PID: {1}".format(script, _proc.pid))

        clk = 0
        good_frames = 0
        good_frames_per_log = 10
        frames_per_log = 100
        cyclic_logging = True

        while True:
            self.frame_buff = self.camera.get_bulk_frames(self.lot)
            if not len(self.frame_buff) == 0:
                self.single_thread_run(self.frame_buff)

            # cyclic logging section -- start  #
                if cyclic_logging:
                    good_frames += 1
                    if good_frames % good_frames_per_log == 0:
                        logger.info("--->{0}th good frame processed.".format(good_frames))
            if cyclic_logging:
                clk += 1
                if clk % frames_per_log == 0:
                    logger.info("---{0}th clock.".format(clk/frames_per_log))
            # cyclic logging section -- end   #

    def single_thread_run(self, frame):
        pixel_distances = self.algorithm.bulk_receive(self.get_frame_buffer())
        print pixel_distances

        # print self.pixel_distances
        self.calculate_velocity(pixel_distances, 'single thread')
        # self.save_data()
        self.frames_buffer_clear()

    def update_distance(self):
        self.conn_1 = self.listener_1.accept()
        logger.debug("placing distance receive request for process {0}".format(1))
        self.distance = self.conn_1.recv()
        logger.debug("distance received {0}".format(self.distance))
        self.conn_1.close()

    def calculate_velocity(self, pixel_distances, process_id):
        self.pixels_per_second = self.get_pixels_per_second(pixel_distances)
        if self.pixels_per_second is not None:
            self.meters_per_second = round(Converter.convert_meters_per_second(self.pixels_per_second), 2)

            message = self.communicator.prepare_message_json(self.meters_per_second, self.distance, dict())
            logger.info('waiting for request from: process {0}'.format(0))
            self.conn_1 = self.listener_1.accept()
            logger.info('connection accepted from: {0}'.format(self.listener_1.last_accepted))
            self.conn_1.send(message)

            logger.info("Current velocity from {0}: {1} m/s".format(process_id, self.meters_per_second))
            # logger.info("Current discharge from {0}: {1} m3/s".format(process_id, self.discharge))

        pixel_distances = []

    def get_pixels_per_second(self, pixel_distances):
        if not len(pixel_distances) == 0:
            self.update_pixel_distances(pixel_distances)
            return self.calculate_pixels_per_second()
        return None

    def calculate_discharge(self):
        self.area = 0.000236
        self.discharge = self.meters_per_second * self.area

    def update_pixel_distances(self, pixel_distances):
        self.x_distances = zip(*pixel_distances)[0]
        self.y_distances = zip(*pixel_distances)[1]
        # self.frame_nos = zip(*pixel_distances)[2]

        x_hist = np.histogram(self.x_distances)
        y_hist = np.histogram(self.y_distances)

        self.x_distance = (x_hist[1][np.argmax(x_hist[0])] + x_hist[1][np.argmax(x_hist[0]) + 1]) / 2
        self.y_distance = (y_hist[1][np.argmax(y_hist[0])] + y_hist[1][np.argmax(y_hist[0]) + 1]) / 2

    def calculate_pixels_per_second(self):
        self.pixels_per_second = math.sqrt(
            math.pow(self.x_distance, 2) + math.pow(self.y_distance, 2)) * self.camera.frame_rate
        return self.pixels_per_second

    def save_data(self):
        data_handler = DataHandler()
        # data_handler.save_pixel_velocity(self.frame_nos, self.pixels_per_second)
        # data_handler.save_pixel_distances(self.frame_nos, self.x_distances, self.y_distances)
        data_handler.save_pixel_distance_validated(self.frame_nos, self.x_distance, self.y_distance)
        self.frame_nos = ()

    def return_one(self):
        return 1

    @staticmethod
    def main():
        try:
            device = Device("FlowMeter-local")
            device.start()
        except KeyboardInterrupt:
            logger.warn("Forcely stopped by user with signal SIGINT")
            exit(0)

if __name__ == '__main__':
    Device.main()