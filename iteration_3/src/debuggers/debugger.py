import threading


class Debugger(threading.Thread):

    def __init__(self, device, type):
        threading.Thread.__init__(self)
        self.type = type
        self.device = device
        self.setName('debugger')

    def routine(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def run(self):
        self.routine()

    @staticmethod
    def get_state_object(self):
        state = {}
        state['camera'] = self.device.camera.get_state()
        state['algorithm'] = self.device.algorithm.get_state()
        return state