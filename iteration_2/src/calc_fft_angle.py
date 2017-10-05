from flow_vision import sti_analyzer
from  flow_vision import sti_builder
import cv2
import numpy as np
from matplotlib import pyplot as plt
from config import DevConfig

frame_rate=29

resize_width=640
history_ratio = 0.6
ref_line_ratio=0.5
hor_start_ratio=0
hor_end_ratio=1
scale_factor = 2
height=200

debug = False

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
    org_frame_width=frame.shape[1]
    org_frame_height=frame.shape[0]
    resize_height=(resize_width*org_frame_height)/org_frame_width
    resize_fx=resize_width/float(org_frame_width)
    resize_fy=resize_height/float(org_frame_height)
    # print  org_frame_width,org_frame_height,resize_width,resize_height,resize_fx,resize_fy
    frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);

    hor_end_index=int((frame.shape[1]-1)*hor_end_ratio)
    hor_start_index=int((frame.shape[1]-1)*hor_start_ratio)
    sp = sti_builder( ref_line_ratio, history_ratio, scale_factor,hor_start_index,hor_end_index,height)
    ft = sti_analyzer()
    while (1):
        rect, frame = c.read()
        if not rect:
            cv2.destroyAllWindows()
            break
        frame = cv2.resize(frame, None, fx=resize_fx, fy=resize_fy, interpolation=cv2.INTER_CUBIC);
        spatio_image = sp.build_image(frame)


        if (sp.can_analyze):
            ft.process(spatio_image)
            ft_image =ft.get_filtered_spectrum()
            cv2.imshow('imamge', ft_image)
            ch = cv2.waitKey(1)
            if debug:
                plt.clf()
                plt.subplot(131), plt.imshow(spatio_image,cmap="gray")
                m = np.tan(np.deg2rad(ft.get_direction()))
                pixel_ditance = frame_rate/(m*resize_fx)
                h, w = ft_image.shape[:2]
                x = np.arange(h/10)
                y = m * x
                plt.subplot(132), plt.plot(x + w/2, y), plt.imshow(ft_image, cmap="gray")
                plt.subplot(133), plt.plot(x, y)
                # plt.pause(0.0001)
                print ft.get_direction(), pixel_ditance
                print "calculated pixel Distancce",ft.get_pixel_distance()
        if debug:
            selected_line_index=sp.ref_point
            frame[selected_line_index, hor_start_index:hor_end_index, :] = np.ones_like(frame[selected_line_index, hor_start_index:hor_end_index, :]) * 255
            cv2.imshow('imamge', frame)

        ch = cv2.waitKey(1)

        if ch == 27:
            break


if __name__ == '__main__':
    main()
