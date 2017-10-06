import cv2
import sys
from config import DevConfig
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

print ("[INFO] Imports done.")


try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = DevConfig.VIDEO_DIR+"02.mp4"
c = cv2.VideoCapture(video_src)



#no:of columns the frame should be divided into
grid_columns = 1
#no:of rows the frame should be divided into
grid_rows = 2
frame_rate=30



#this function returns a region of interest
def gridDetails(img, grid_columns, grid_rows, i, j):
    frame_hieght, frame_width = img.shape[:2]
    grid_height = frame_hieght / grid_rows
    grid_width = frame_width / grid_columns
    return img[j * grid_height:(j + 1) * grid_height, i * grid_width:(i + 1) * grid_width]


def drawGrid(frame) :
    frame_hieght, frame_width = frame.shape[:2]
    grid_height = frame_hieght / grid_rows
    grid_width = frame_width / grid_columns
    # draw vertical and horizontal lines in the real_frames showing the grid selection
    for i in range(1, grid_columns):
        frame = cv2.line(frame, (grid_width * i, 0), (grid_width * i, frame_hieght), (255, 255, 0), 1, cv2.LINE_AA)
    for i in range(1, grid_rows):
        frame = cv2.line(frame, (0, grid_height * i), (frame_width, grid_height * i), (255, 255, 0), 1, cv2.LINE_AA)
    return frame


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



while(1) :
    rect, frame = c.read()
    if not rect:
        cv2.destroyAllWindows()
        break
    frame = cv2.imread('../resources/blur/lenna-50.jpg', 1)
    # frame = cv2.resize(frame, (640, 480))
    frame=drawGrid(frame)
    cv2.imshow("frame",frame)
    ch = cv2.waitKey(int(1000.0 / frame_rate))

    for i in range(grid_columns):
        for j in range(grid_rows):
            selected_cell=gridDetails(frame, grid_columns, grid_rows, i, j)
            print getBlurLength(selected_cell, False)



    if ch == 27:
        cv2.destroyAllWindows()
        break
    break