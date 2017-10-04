class FrameWallet:
    def __init__(self, wallet_size):
        self.wallet_size = wallet_size
        self._original_frames=[]
        self._masked_frames = []

    def put_original_frame(self,frame):
        if len(self._original_frames) > self.wallet_size:
            self._original_frames.pop(0)
        self._original_frames.append(frame)

    def put_masked_frame(self,frame):
        if len(self._masked_frames) > self.wallet_size:
            self._masked_frames.pop(0)
        self._masked_frames.append(frame)

    def get_original_frames(self):
        return self._original_frames

    def get_masked_frames(self):
        return self._masked_frames



