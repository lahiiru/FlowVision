class Algorithm:

    def __init__(self):
        self.debug = True
        self.pixels_per_second=0

    def get_pixels_per_second(self):
        return self.pixels_per_second

    def receive_frames(self, frame):
        raise NotImplementedError("Subclass must implement abstract method")

    def update(self,**kwargs):
        raise NotImplementedError("Subclass must implement abstract method")