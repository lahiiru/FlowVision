from camera import AbstractCamera
import picamera
import time
import numpy as np
import cv2
import io


class RPiCamera(AbstractCamera):

    def __init__(self, path):
        AbstractCamera.__init__(self)
        self.frame_rate = 30

    def get_name(self):
        return 'RPi Camera'

    def _process(self):
        with picamera.PiCamera(sensor_mode=7, resolution='VGA') as camera:
            time.sleep(2)
            while True:
                start = time.time()
                camera.capture_sequence(self.__receiver(), format='jpeg', use_video_port=True)
                self.frame_rate = (self.img_buf_size / (time.time() - start))

    def __receiver(self):
        stream = io.BytesIO()
        for i in range(self.img_buf_size):
            yield stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, 1)
            # cv2.imshow('image', image)
            # cv2.waitKey(1)
            self._put_frame(image)
            stream.seek(0)
            stream.truncate()

    def _release(self):
        pass