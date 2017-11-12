import numpy as np
import cv2
from matplotlib import pyplot as plt


# class for build the spatio temporal image
class sti_builder:
    height = 0
    width=0
    horizontal_start_index=0
    horizontal_end_index=0
    ref_point = 0
    spatio_image = []
    history_ratio = 0.6
    index = -1
    scale_factor = 2
    array_size =0
    first_round = True
    next_pointer = 0
    is_configured=False
    new_frame_count=0
    ref_point_ratio=0
    can_analyze=False

    count=0



    def __init__(self,ref_point_ratio,history_ratio,scale_factor,horizontal_start_index,horizontal_end_index,height):
        self.ref_point_ratio=ref_point_ratio
        self.history_ratio= history_ratio
        self.scale_factor= scale_factor
        self.horizontal_start_index=horizontal_start_index
        self.horizontal_end_index=horizontal_end_index
        self.width =horizontal_end_index-horizontal_start_index+1
        self.height=height

    def init_configuration(self, frame):
        # self.height = frame.shape[0]
        self.ref_point = int(self.ref_point_ratio * (frame.shape[0] - 1))
        self.array_size = self.height * self.scale_factor
        self.spatio_image = np.zeros((self.array_size, self.width), dtype=np.int)
        self.next_pointer = self.height - 1
        self.new_frame_count = self.height - int(self.history_ratio * self.height)
        self.is_configured = True

    def build_image(self, frame):
        if(not self.is_configured) :
            self.init_configuration(frame)

        self.count+=1

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self.index = (self.index + 1) % self.array_size
        self.spatio_image[self.index, :] = frame[self.ref_point,self.horizontal_start_index: self.horizontal_end_index+1]
        self.can_analyze=False
        if self.first_round:
            if (self.index == self.array_size - 1):
                self.first_round = False

            if (self.index == self.height - 1):
                self.next_pointer = self.index + self.new_frame_count
                self.can_analyze=True
                return self.spatio_image[:self.index + 1, ]

            elif self.index < self.height - 1 :
                return self.spatio_image[:self.index + 1, ]

            elif (self.index > self.height and self.index == self.next_pointer):
                self.next_pointer = (self.index + self.new_frame_count) % self.array_size
                self.can_analyze=True
            return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]
        else:
            if self.next_pointer == self.index:
                self.can_analyze=True
                self.next_pointer = (self.index + self.new_frame_count) % self.array_size
            if self.index < self.height - 1:
                return np.concatenate(
                    (self.spatio_image[-(self.height - self.index - 1):, ], self.spatio_image[:self.index + 1, ]),
                    axis=0)
            else:
                return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]






class sti_analyzer:
    _global_direction = 0
    _pixel_distance=0

    def process(self, frame):
        height, width = frame.shape[:2]

        s = min(height, width)
        frame = frame[:s, :s]
        height, width = s, s
        # frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,2)
        img_float32 = np.float32(frame)
        dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        self._magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))




        self._filtered_spectrum = self._magnitude_spectrum.copy()[:, :]
        self._filtered_spectrum = np.zeros_like(self._filtered_spectrum)
        self._filtered_spectrum[np.arange(len(self._magnitude_spectrum)), self._magnitude_spectrum.argmax(1)] = 255
        fs = np.argwhere(self._filtered_spectrum == 255)
        yy = np.absolute(fs[:, 0] - height / 2)
        xx = np.absolute(fs[:, 1] - width / 2)
        polar = np.arctan2(yy, xx)
        polar = polar * 180 / np.pi
        hist = np.histogram(polar, np.arange(0, 90, 1))
        maxBinUpper = np.argmax(hist[0])
        self._global_direction = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0



        tan_value=yy/xx
        tan_value=tan_value[np.where(tan_value>0)]
        tan_hist = plt.hist(tan_value, np.arange(0,50,1));
        maxBinUpper = np.argmax(tan_hist[0])
        self._pixel_distance = (tan_hist[1][maxBinUpper + 1] + tan_hist[1][maxBinUpper]) / 2.0

        print self._global_direction,self._pixel_distance

        # plt.pause(0.001)


    def get_fft_image(self):
        return self._magnitude_spectrum


    def get_filtered_spectrum(self):
        return self._filtered_spectrum

    def get_direction(self):
        return self._global_direction

    def get_pixel_distance(self):
        return self._pixel_distance

