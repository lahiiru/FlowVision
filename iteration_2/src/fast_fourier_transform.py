import numpy as np
import cv2

# this class for make the fourier transform from a spatio image and calculate the angle
class FastFourierTransform:
    globalDirection = 0

    # this function get a grayscale spatio image as a input and return the fourier transformed image of it.
    # Angle also calculated and store in the variable called globalDirection
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

        # print("[INFO] @ FFT2D completed.")

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

        # plt.xlabel('mode = '+str(self.globalDirection)+'deg')
        # plt.vlines([self.globalDirection], 0, 100, label = str(self.globalDirection))
        # plt.pause(0.001)
        # plt.imshow(filtered_spectrum, cmap='gray')
        # plt.title(str)
        # plt.pause(0.001)
        return filtered_spectrum