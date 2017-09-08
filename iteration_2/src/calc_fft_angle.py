from flow_vision import STIAnalyzer
from  flow_vision import STIBuilder
import cv2
import numpy as np
from matplotlib import pyplot as plt
from config import DevConfig

frame_rate=29

selected_line=0 # variable for select the line to make the spatio image .Spatio image construct using this line pixels in every frame
resize_fx=1
resize_fy=1
history_ratio = 0.6
scale_factor = 2
horizontal_start_index=0 # parameter for set starting index of the frame for build the spatio image (spatio image started from this index)
horizontal_end_index=100 # parameter for set ending index of the frame for build the spatio image (spatio image end from this index)
height=200 # enter the desired spatio image height (how many consecutive frames are needed to build the image)

debug = True


# this main function for read the video stream and calculate the angle from FFT method
def main():
    import sys
    try:
        video_src = sys.argv[1]
        if video_src.isdigit():
            video_src = int(video_src)
    except:
        video_src = DevConfig.VIDEO_DIR + "03.mov"

    c = cv2.VideoCapture(video_src)

    rect, frame = c.read()
    frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);
    selected_line = frame.shape[0]/2
    sp = STIBuilder( selected_line, history_ratio, scale_factor,horizontal_start_index,horizontal_end_index,height) # initialize the Spatio object
    ft = STIAnalyzer()
    while (1):
        rect, frame = c.read()
        if not rect:
            cv2.destroyAllWindows()
            break
        frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);
        spatio_image = sp.buildImage(frame)

        # new_frame_count==0 when correct(history and new frame count is correct) image is constructed
        if (sp.new_frame_count == 0):

            ft.process(spatio_image)
            ft_image =ft.getFilteredSpectrum()
            # cv2.imshow('spatio image', spatio_image)
            if debug:
                plt.clf()
                plt.subplot(131), plt.imshow(spatio_image,cmap="gray")
                m = np.tan(np.deg2rad(ft.getDirection()))
                pixel_ditance = frame_rate/(m*resize_fx)
                h, w = ft_image.shape[:2]
                x = np.arange(h/10)
                y = m * x
                plt.subplot(132), plt.plot(x + w/2, y), plt.imshow(ft_image, cmap="gray")
                plt.subplot(133), plt.plot(x, y)
                plt.pause(0.0001)
                print ft.getDirection(), pixel_ditance
                # cv2.imwrite("spatio_04mp4_1.png",spatio_image)
                # plt.imshow(ft.magnitude_spectrum, cmap="gray")
        if debug:
            frame[selected_line, :, :] = np.ones_like(frame[selected_line, :, :]) * 255
            cv2.imshow('imamge', frame)

        ch = cv2.waitKey(int(1000.0 / frame_rate) + 1)

        if ch == 27:
            break


if __name__ == '__main__':
    main()
