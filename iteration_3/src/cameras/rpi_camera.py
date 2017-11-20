from cameras.camera import AbstractCamera
import picamera
import time
import numpy as np
import cv2
import io
import logging

logger = logging.getLogger()


class RPiCamera(AbstractCamera):

    def __init__(self):
        AbstractCamera.__init__(self)
        self.frame_rate = 50
        logger.debug("Raspberry Pi camera initiated.")
        self.bulk_size = 50

    def get_name(self):
        return 'RPi Camera'

    def _process(self):
        with picamera.PiCamera(sensor_mode=7, resolution='VGA') as camera:
            camera.shutter_speed = 2000
            camera.framerate = 50
            time.sleep(4)
            while True:
                start = time.time()
                camera.capture_sequence(self.__receiver(self.bulk_size), format='jpeg', use_video_port=True)
                #self.frame_rate = int(self.img_buf_size / (time.time() - start))

    def __receiver(self, bulk_size):
        stream = io.BytesIO()
        for i in range(bulk_size):
            yield stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, 1)
            # cv2.imshow('image', image)
            # cv2.waitKey(1)
            # self._put_frame(image)
            self.frame_array.append(image)
            logger.debug("Put frame. Queue size :" + str(self.frames.qsize()))
            stream.seek(0)
            stream.truncate()

    def get_bulk_frames(self, bulk_size):
        with picamera.PiCamera(sensor_mode=7, resolution='VGA') as camera:
            camera.shutter_speed = 2000
            camera.framerate = 50
            time.sleep(4)
            camera.capture_sequence(self.__receiver(bulk_size), format='jpeg', use_video_port=True)
        array = self.frame_array[:bulk_size]
        self.frame_array = []
        return array

    def _release(self):
        pass