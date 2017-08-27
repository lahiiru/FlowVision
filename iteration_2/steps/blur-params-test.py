import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

print ("[INFO] Imports done.")

while True:
    for dist in [10,20,50,100,0]:
        gray = cv2.imread('../resources/blur/lenna-'+str(dist)+'.jpg',1)
        h, w = gray.shape[::2]
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        m = 20*np.log(np.abs(fshift))
        y, x = m.shape
        r = int(y * 0.3)
        m = m[r:-r,:]

        # normalising
        ma = np.max(m)
        mi = np.min(m)
        m = (m / ma)

        avg = np.mean(m,axis=0)

        plt.clf()
        plt.plot(avg, linewidth=1)
        
        mins = signal.argrelmin(avg)
        maxs = signal.argrelmax(avg, order=3)
        vals = avg[maxs]
        
        plt.scatter(maxs,vals,10,c='red')
        plt.title(str(dist))
        plt.pause(.1)