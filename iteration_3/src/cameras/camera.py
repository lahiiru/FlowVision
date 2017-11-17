import threading
import Queue
import logging
# from iteration_3.src.debuggers import Debuggable
from debuggers.debuggable import Debuggable

logger = logging.getLogger()


class AbstractCamera(threading.Thread, Debuggable):
    def __init__(self, img_buf_size=12):
        self.img_buf_size = img_buf_size
        threading.Thread.__init__(self)
        self.frames = Queue.Queue(maxsize=self.img_buf_size * 4)
        self.latest_frame = None
        self.preview = False
        self.resolution = (640, 480)
        self.frame_rate = 7
        self.setName('camera')
        self.sem = threading.Semaphore()

    def run(self):
        logger.debug("Camera started.")
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

    def get_visualization(self):
        return self.peek_frame()

    def get_name(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_state(self):
        state = {}
        state["type"] = self.get_name()
        state["frame rate"] = self.frame_rate
        state["resolution"] = self.resolution
        return state
