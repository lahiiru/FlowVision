"""
    2D FFT and histogram based angle calculation algorithm
    Input:  A spatio temporal image
    Output: Approximation for average pattern angle

    python fft-algo.py gradients/60.jpg 10
"""

from __future__ import print_function
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import time

debug = False
gray = None

print ("[INFO] Imports done.")
    
try:
    video_src = sys.argv[1]
except:
    video_src = '../resources/gradients/60.jpg'
    sigma = 0.1

gray = cv2.imread(video_src, 0)

# TODO: should be implemented in less complexity
def getMaximumOccurenceInterval(points):

    hist = np.histogram(points, np.arange(0, 90, 1))
    maxBinUpper = np.argmax(hist[0])
    maximumOccurenceBin = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0
    return maximumOccurenceBin

def getMagnitudeFFT(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    spectrum = 20 * np.log(np.abs(fshift))
    return spectrum

h, w = gray.shape[:2]

if True:
    s = min(h,w)
    gray = gray[:s,:s]
    h, w = s, s

print ("[INFO] Image loaded.")
start_time = time.time()

# Pre-processing image
# gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,2)
# gray = cv2.Laplacian(gray, cv2.CV_32F, ksize=3, delta=0, scale=10)

magnitude_spectrum = getMagnitudeFFT(gray)

print("[INFO] @ "+str(round(time.time() - start_time,2))+" FFT2D compled.")

filtered_spectrum = np.zeros_like(magnitude_spectrum)
filtered_spectrum[np.arange(len(magnitude_spectrum)), magnitude_spectrum.argmax(1)] = 255

# fs contains coordinates of maximum points. e.g. [[x,y],..]
fs = np.argwhere(filtered_spectrum==255)
yy = np.absolute(fs[:,0]-h/2)
xx = np.absolute(fs[:,1]-w/2)
polar = np.arctan2(yy,xx)
polar = np.rad2deg(polar)
globalDirection = getMaximumOccurenceInterval(polar)

print("[INFO] "+str(round(time.time() - start_time,2))+"s elapsed for total algorithm")

print (globalDirection, "Deg.")

if debug:
    plt.xlabel('mode = '+str(globalDirection)+'deg, sigma=')
    plt.vlines([globalDirection], 0, 100, label = str(globalDirection))
    plt.show()
    plt.imshow(filtered_spectrum, cmap='gray')
    plt.show()
