import threading


class AbstractDebugger(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")
