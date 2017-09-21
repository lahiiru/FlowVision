import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from config import DevConfig

print ("[INFO] Imports done.")

def getBlurLength(image, debug=False):
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    m = 20 * np.log(np.abs(fshift))

    y, x = m.shape
    r = int(y * 0.3)
    m = m[r:-r, :]

    avg = np.mean(m, axis=0)

    mins = signal.argrelmin(avg, order=3)[0]

    g_max_loc = np.argmax(avg)
    min_lower = mins[mins < g_max_loc][::-1]
    min_upper = mins[mins > g_max_loc]
    d = 1
    if len(min_upper) > 4 and len(min_lower) > 4:
        d = (((min_upper[0] - min_lower[0]) / 2) + abs(min_upper[1] - min_upper[0]) + abs(
            min_upper[2] - min_upper[1]) + abs(min_upper[3] - min_upper[2]) \
             + abs(min_lower[0] - min_lower[1]) + abs(min_lower[1] - min_lower[2]) + abs(
            min_lower[2] - min_lower[3])) / 7

    blength = w * 1.0 / d

    if debug:
        plt.clf()
        plt.plot(avg, linewidth=1)
        plt.scatter(mins, avg[mins], 20, c='red')
        plt.show()

    return blength

cap = cv2.VideoCapture(DevConfig.VIDEO_DIR + "01.mp4")

vals = []
while True:
    r, image = cap.read()
    vals += [getBlurLength(image)]
    plt.plot(np.arange(len(vals)),vals)
    plt.pause(0.01)
    cv2.imshow('a',image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
        cv2.destroyAllWindows()

cap.release()

# for dist in [20,50,100]:
#     image = cv2.imread('../resources/blur/lenna-'+str(dist)+'.jpg',1)
#     print getBlurLength(image)
#     print("INFO taken", t - time.time())