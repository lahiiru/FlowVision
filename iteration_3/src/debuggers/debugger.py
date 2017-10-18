import threading


class Debugger(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device
        self.setName('debugger')

    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")

    @staticmethod
    def get_state_object(self):
        state = {}
        state['camera'] = self.device.camera.get_state()
        state['algorithm'] = self.device.algorithm.get_state()
        return state