import numpy as np
import cv2
import time
from matplotlib import pyplot as plt

frame_rate = 30
selected_line = 350
history_ratio = 0.6
scale_factor = 2

# spatio image testing with black error

class Spatio:
    height = 0
    width = 0
    ref_point = 0
    spatio_array = []

    history_ratio = 0.6
    index = -1
    scale_factor = 2
    array_size =0
    first_round = True
    next_index = 0
    initial_spatio=False


    def __init__(self, frame, ref_point,history_ratio,scale_factor):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.height, self.width = frame.shape
        self.array_size = self.height * scale_factor
        self.spatio_array = np.zeros((self.array_size, self.width), dtype=np.int)
        self.ref_point = ref_point
        self.history_ratio= history_ratio
        self.scale_factor= scale_factor
        self.next_index=self.height-1
        self.history_count = int(self.history_ratio * self.height)
        self.partition_count = self.height - self.history_count

    def getSpatioImage(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self.index = (self.index + 1) % self.array_size
        self.spatio_array[self.index, :] = frame[self.ref_point,:]



        if self.first_round:

            if (self.index == self.array_size - 1):
                self.first_round = False

            if (self.index == self.height - 1):
                self.next_index = self.index + self.partition_count
                self.initial_spatio= True
                return self.spatio_array[:self.index + 1, ]

            if (self.index > self.height and self.index == self.next_index):
                self.next_index = (self.index + self.partition_count) % self.array_size
                print str(self.index) + " next index" + str(self.next_index)
                return self.spatio_array[self.index - (self.height - 1):self.index + 1, ]
            return None

        else:
            if self.next_index == self.index:
                self.next_index = (self.index + self.partition_count) % self.array_size
                print str(self.index) + " next index" + str(self.next_index)
                if self.index < self.height - 1:
                    return np.concatenate((self.spatio_array[-(self.height - self.index - 1):, ], self.spatio_array[:self.index + 1, ]),
                                         axis=0)

                else:
                    return self.spatio_array[self.index - (self.height - 1):self.index + 1, ]
            return None

class FourierTransform:
    globalDirection = 0

    def getTransformedImage(self, frame):
        height, width = frame.shape[:2]

        s = min(height, width)
        frame = frame[:s, :s]
        height, width = s, s
        # frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,2)
        img_float32 = np.float32(frame)
        dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        self.magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

        print("[INFO] @ FFT2D completed.")

        filtered_spectrum = self.magnitude_spectrum.copy()[:, :]
        filtered_spectrum = np.zeros_like(filtered_spectrum)
        filtered_spectrum[np.arange(len(self.magnitude_spectrum)), self.magnitude_spectrum.argmax(1)] = 255
        fs = np.argwhere(filtered_spectrum == 255)
        yy = np.absolute(fs[:, 0] - height / 2)
        xx = np.absolute(fs[:, 1] - width / 2)
        polar = np.arctan2(yy, xx)
        polar = polar * 180 / np.pi

        # hist = plt.hist(polar, np.arange(0,90,1));
        hist = np.histogram(polar, np.arange(0, 90, 1))
        maxBinUpper = np.argmax(hist[0])
        self.globalDirection = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0

        # plt.xlabel('mode = '+str(globalDirection)+'deg')
        # plt.vlines([globalDirection], 0, 100, label = str(globalDirection))
        # plt.pause(0.001)
        # plt.imshow(filtered_spectrum, cmap='gray')
        # plt.title(str)
        # plt.pause(0.001)
        return filtered_spectrum


def main():
    import sys
    try:
        video_src = sys.argv[1]
        if video_src.isdigit():
            video_src = int(video_src)
    except:
        video_src = "../03.MOV"

    c = cv2.VideoCapture(video_src)

    rect, frame = c.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC);
    sp = Spatio(frame, selected_line,history_ratio, scale_factor)
    ft = FourierTransform()
    cycle_start = 0
    while (1):
        rect, frame = c.read()
        # cycle_time=time.time()-cycle_start
        # cycle_start=time.time()
        # print (1/cycle_time)

        if not rect:
            cv2.destroyAllWindows()
            break
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC);
        spatio_image = sp.getSpatioImage(frame)

        if sp.initial_spatio:
            # if True:
            if type(spatio_image)==type(None):
                ch = cv2.waitKey(int(1000.0 / frame_rate)+1)
                continue

            view = spatio_image.copy()[:, :]
            #ft_image = ft.getTransformedImage(spatio_image)
            # vis = np.hstack((spatio_image, ft_image))
            #spatio_image = np.ones_like(spatio_image) * 255

            print spatio_image
            cv2.imshow('spatio image', spatio_image*2)
            print str(ft.globalDirection)
            # plt.imshow(ft.magnitude_spectrum, cmap="gray")
            # plt.pause(0.0001)
            frame[selected_line, :, :] = np.ones_like(frame[selected_line, :, :]) * 255
            cv2.imshow('imamge',frame)

        ch = cv2.waitKey(int(1000.0 / frame_rate)+1)

        if ch == 27:
            break


if __name__ == '__main__':
    main()
