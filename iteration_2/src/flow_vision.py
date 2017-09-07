import numpy as np
import cv2


# class for build the spatio temporal image
class STIBuilder:
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
    next_index = 0
    initial_spatio=False
    is_configured=False
    partition_count=0
    new_frame_count=0 # new_frame_count is 0 only if  correct spatio image constructed with correct history and new frame count. new_frame_count >0 for other return values


    def __init__(self,ref_point,history_ratio,scale_factor,horizontal_start_index,horizontal_end_index,height):
        self.ref_point = ref_point
        self.history_ratio= history_ratio
        self.scale_factor= scale_factor
        self.horizontal_start_index=horizontal_start_index
        self.horizontal_end_index=horizontal_end_index
        self.width =horizontal_end_index-horizontal_start_index+1
        self.height=height

    def initConfiguration(self, frame):
        # self.height = frame.shape[0]
        self.array_size = self.height * self.scale_factor
        self.spatio_image = np.zeros((self.array_size, self.width), dtype=np.int)
        self.next_index = self.height - 1
        self.history_count = int(self.history_ratio * self.height)
        self.partition_count = self.height - self.history_count
        self.is_configured = True

    def buildImage(self, frame):
        if(not self.is_configured) :
            self.initConfiguration(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.new_frame_count +=1

        self.index = (self.index + 1) % self.array_size
        self.spatio_image[self.index, :] = frame[self.ref_point,self.horizontal_start_index: self.horizontal_end_index+1]
        if self.first_round:

            if (self.index == self.array_size - 1):
                self.first_round = False

            if (self.index == self.height - 1):
                self.next_index = self.index + self.partition_count
                self.initial_spatio= True
                self.new_frame_count=0
                return self.spatio_image[:self.index + 1, ]

            elif self.index < self.height - 1 :
                # do not build the full image (no enough frames) returns what have in tha spatio_image array
                return self.spatio_image[:self.index + 1, ]

            elif (self.index > self.height and self.index == self.next_index):
                self.next_index = (self.index + self.partition_count) % self.array_size
                # print str(self.index) + " next index" + str(self.next_index)
                self.new_frame_count = 0
                return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]
            else:
                # returns the full image but not contains the correct amount of new frames (no enough new frames yet)
                # self.index < self.next_index
                return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]


        else:
            if self.next_index == self.index:
                self.new_frame_count=0
                self.next_index = (self.index + self.partition_count) % self.array_size
                # print str(self.index) + " next index" + str(self.next_index)
                if self.index < self.height - 1:
                    return np.concatenate((self.spatio_image[-(self.height - self.index - 1):, ], self.spatio_image[:self.index + 1, ]),
                                         axis=0)

                else:
                    return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]
            else :
                # returns the full image but not contains the correct amount of new frames (no enough new frames yet)
                # self.index < self.next_index
                if self.index < self.height - 1:
                    return np.concatenate(
                        (self.spatio_image[-(self.height - self.index - 1):, ], self.spatio_image[:self.index + 1, ]),
                        axis=0)

                else:
                    return self.spatio_image[self.index - (self.height - 1):self.index + 1, ]





# this class for make the fourier transform from a spatio image and calculate the angle
class Analyzer:
    _globalDirection = 0
    # this function get a grayscale spatio image as a input and process the fourier transformed image of it.
    # Angle also calculated and store in the variable called globalDirection
    # Filtered spectrem also stored in filtered_spectrum
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

        # hist = plt.hist(polar, np.arange(0,90,1));
        hist = np.histogram(polar, np.arange(0, 90, 1))
        maxBinUpper = np.argmax(hist[0])
        self._globalDirection = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0



    def getFFTImage(self):
        return self._magnitude_spectrum


    def getFilteredSpectrum(self):
        return self._filtered_spectrum

    def getDirection(self):
        return self._globalDirection

