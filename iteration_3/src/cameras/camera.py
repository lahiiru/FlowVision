import threading
import Queue
import logging

logger = logging.getLogger()


class AbstractCamera(threading.Thread):
    def __init__(self, img_buf_size=120):
        self.img_buf_size = img_buf_size
        threading.Thread.__init__(self)
        self.frames = Queue.Queue(maxsize=self.img_buf_size * 4)
        self.latest_frame = None
        self.preview = False
        self.resolution = (640, 480)
        self.frame_rate = 7
        self.setName('camera')
        logger.info("Camera initiated.")

    def run(self):
        logger.info("Camera started.")
        self._process()
        self._release()

    def _process(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def _release(self):
        raise NotImplementedError("Subclass must implement abstract method")

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

    def _put_frame(self, frame):
        if not self.preview and self.frames.full():
            self.frames.put(frame)
        else:
            if not self.frames.full():
                self.frames.put(frame)
        self.latest_frame = frame

