from fast_fourier_transform import FastFourierTransform
from spatio import STIBuilder
import cv2
import time
import numpy as np
from matplotlib import pyplot as plt

frame_rate=30

selected_line=260 # variable for select the line to make the spatio image .Spatio image construct using this line pixels in every frame
resize_fx=0.5
resize_fy=0.5
history_ratio = 0.6
scale_factor = 2


# this main function for read the video stream and calculate the angle from FFT method
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
    frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);
    sp = STIBuilder( selected_line, history_ratio, scale_factor) # initialize the Spatio object
    ft = FastFourierTransform()# initialize the FastFourierTransform object
    cycle_start = 0
    while (1):
        rect, frame = c.read()
        # cycle_time=time.time()-cycle_start
        # cycle_start=time.time()
        # print (1/cycle_time)

        if not rect:
            cv2.destroyAllWindows()
            break
        frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);
        spatio_image = sp.buildImage(frame)

        # new_frame_count==0 when correct(history and new frame count is correct) image is constructed
        if (sp.new_frame_count == 0):
            # if True:
            if type(spatio_image) == type(None):
                ch = cv2.waitKey(int(1000.0 / frame_rate) + 1)
                continue

            view = spatio_image.copy()[:, :]
            ft_image = ft.getTransformedImage(spatio_image)
            # spatio_image = np.ones_like(spatio_image) * 255

            print spatio_image.shape
            # cv2.imshow('spatio image', spatio_image)
            plt.imshow(spatio_image,cmap="gray")
            # print np.argwhere(spatio_image > 255)
            # cv2.imwrite("spatio_03MOV_1.png",spatio_image)
            plt.pause(0.0001)
            print str(ft.globalDirection)
            # plt.imshow(ft.magnitude_spectrum, cmap="gray")
            # plt.pause(0.0001)
            frame[selected_line, :, :] = np.ones_like(frame[selected_line, :, :]) * 255
            # cv2.imshow('imamge', frame)

        ch = cv2.waitKey(int(1000.0 / frame_rate) + 1)

        if ch == 27:
            break


if __name__ == '__main__':
    main()
