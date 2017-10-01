import threading
import picamera
import time
import Queue
import numpy as np
import cv2
import io


class Camera(threading.Thread):
    def __init__(self, img_buf_size=120):
        self.img_buf_size = img_buf_size
        threading.Thread.__init__(self)
        self.frames = Queue.Queue(maxsize=self.img_buf_size * 4)
        self.latest_frame = None
        self.preview = False

    def run(self):
        with picamera.PiCamera(sensor_mode=7, resolution='VGA') as camera:
            time.sleep(2)
            while True:
                start = time.time()
                camera.capture_sequence(self.receiver(), format='jpeg', use_video_port=True)
                print('Captured 120 images at %.2ffps' % (self.img_buf_size / (time.time() - start)))
                print (self.frames.qsize())

    def get_frame(self):
        if not self.frames.empty():
            return self.frames.get()
        return None

    def peek_frame(self):
        if not self.frames.empty():
            return self.frames.queue[0]
        return None

    def get_latest_frame(self):
        return self.latest_frame

    def receiver(self):
        stream = io.BytesIO()
        for i in range(self.img_buf_size):
            yield stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, 1)
            # cv2.imshow('image', image)
            # cv2.waitKey(1)
            if not self.preview and self.frames.full():
                self.frames.put(image)
            else:
                if not self.frames.full():
                    self.frames.put(image)
            self.latest_frame = image
            stream.seek(0)
            stream.truncate()


camera = Camera()
camera.start()

time.sleep(10)
frame = camera.peek_frame()
cv2.imshow('image', frame)
cv2.waitKey(0)
print('main thread finished')