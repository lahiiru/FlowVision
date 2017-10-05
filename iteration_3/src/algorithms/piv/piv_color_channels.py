from piv_algorithm import *

logger = logging.getLogger()


class ColorChannelsPIV(ParticleImageVelocimetryAlgorithm):
    def __init__(self):
        ParticleImageVelocimetryAlgorithm.__init__(self, 7)
        self.x_offset = 20
        self.y_offset = 30
        logger.info('ColorChannelsPIV algorithm initiated')

    def receive_frame(self, frame,tag):
        self.separate_channels(frame)
        self.frame_wallet.put_tag(tag)
        self.frame_wallet.put_tag(tag)

    def _process_pre_filters(self):
        pass

    def _calculate_template_bounds(self, frame):
        bounds = []
        feature_points = cv2.goodFeaturesToTrack(frame, 50, 0.1, 5)
        for i in feature_points:
            x, y = i.ravel()
            # placing offsets
            y_max = int(y + self.y_offset)
            x_max = int(x + self.x_offset)
            y_min = int(y - np.min((self.y_offset, y)))
            x_min = int(x - np.min((self.x_offset, x)))
            bounds += [(x_min, x_max, y_min, y_max)]

        return bounds

    def _template_qa_passed(self, template):
        return True

    def separate_channels(self, frame):
        if frame is None:
            logger.warn('No frame received to separate.')
            return
        channels = cv2.split(frame)
        self.frame_wallet.put_masked_frame(channels[0])
        self.frame_wallet.put_masked_frame(channels[2])
        self.frame_wallet.put_original_frame(np.dstack((channels[0], channels[0], channels[0])))
        self.frame_wallet.put_original_frame(np.dstack((channels[1], channels[1], channels[1])))
        # self.frame_wallet.put_original_frame(frame)
        # self.frame_wallet.put_original_frame(frame)

    def get_mode_distance(self, distances):
        x_distances = zip(*distances)[0]
        hist = np.histogram(list(x_distances), np.arange(np.min(x_distances), np.max(x_distances), 1))
        maxBinUpper = np.argmax(hist[0])
        x_mode=(hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0

        y_distances = zip(*distances)[1]
        hist = np.histogram(list(y_distances), np.arange(np.min(y_distances), np.max(y_distances), 1))
        maxBinUpper = np.argmax(hist[0])
        y_mode=(hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0

        self.debug_vis_text = self.frame_wallet.get_tags()[0]+'\nDistance X: '+ str(x_mode)+ '  Distance Y:'+str(y_mode)
        print self.debug_vis_text
        return (x_mode,y_mode)

    def draw_templates(self, **kwargs):
        pass