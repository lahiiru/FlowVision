class FrameWallet:
    def __init__(self, wallet_size):
        self.wallet_size = wallet_size
        self._original_frames = []
        self._masked_frames = []
        self._tags = []

    def put_original_frame(self, frame):
        if len(self._original_frames) >= self.wallet_size:
            self._original_frames.pop(0)
        self._original_frames.append(frame)

    def put_masked_frame(self,frame):
        if len(self._masked_frames) >= self.wallet_size:
            self._masked_frames.pop(0)
        self._masked_frames.append(frame)

    def put_tag(self,tag):
        if len(self._tags) >= self.wallet_size:
            self._tags.pop(0)
        self._tags.append(tag)

    def get_original_frames(self):
        return self._original_frames

    def get_masked_frames(self):
        return self._masked_frames

    def get_tags(self):
        return self._tags



