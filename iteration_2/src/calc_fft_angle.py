from fast_fourier_transform import FastFourierTransform
from spatio import Spatio
import cv2
import time
import numpy as np

frame_rate=30

selected_line=350 # variable for select the line to make the spatio image .Spatio image construct using this line pixels in every frame


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
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC);
    sp = Spatio(frame, selected_line) # initialize the Spatio object
    ft = FastFourierTransform()# initialize the FastFourierTransform object
    cycle_start = 0
    while (1):
        rect, frame = c.read()
        cycle_time = time.time() - cycle_start
        cycle_start = time.time()
        print (1 / cycle_time)
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC);
        if not rect:
            cv2.destroyAllWindows()
            break

        spatio_image = sp.getSpatioImage(frame) # get the spatio image (grayscale) from the  frame

        if (sp.frame_idx > sp.height):
            # if True:
            view = spatio_image.copy()[:, :]
            ft_image = ft.getTransformedImage(spatio_image) # transformed spatio image to fft
            vis = np.hstack((spatio_image, ft_image))
            cv2.imshow('spatio imamge', view)
            print str(ft.globalDirection) # direction calculated in fft method
            # plt.imshow(ft.magnitude_spectrum,cmap="gray")
            # plt.pause(0.01)
            frame[selected_line, :, :] = np.ones_like(frame[selected_line, :, :]) * 255
            cv2.imshow('imamge',frame)

        ch = cv2.waitKey(int(1000.0 / frame_rate))

        if ch == 27:
            break


if __name__ == '__main__':
    main()
