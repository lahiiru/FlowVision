import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import datetime
import os
import time

def quit_figure(event):
    if event.key == 'v':
        plt.close('all')
        videoMode = True
    if event.key == 'q':
        plt.close('all')
        cv2.destroyAllWindows()


def speedCalc(avg_d, angle, drain_d, frame_rate, frame_width):
    speed = (avg_d * 2 * drain_d * math.tan(math.radians(angle / 2)) * frame_rate) / frame_width
    return speed


try:
    video_src = sys.argv[1]
    if video_src.isdigit():
        video_src = int(video_src)
except:
    video_src = "..\\01.mp4"

c = cv2.VideoCapture(video_src)

cam_angle = 28
frame_rate = 7
drain_d = 30

rect, prev = c.read()

frame_hieght, frame_width = prev.shape[:2]

prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10, detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
values = []
means = []
mean_size = 10
white_threshold = 5
i = 0
videoMode = True
record = False
speed = 0

execution_times_outer = np.zeros((20, 8))
performance_graph_titles = ['Reading\n_Frames','GrayScale\n_Image','Removing\n_Background','MorphologyEx\nfunction','Selecting\n_template','Counting\n_white_pixels','Template\n_matching','MinMax\n_locate']
average_time_values = []
outer_loop = 0

if record:
    try:
        os.mkdir('records')
    except:
        print("folder exist")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('records\\' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.avi', fourcc,
                          frame_rate, (frame_width, frame_hieght))


while (outer_loop<20):                                               #changed

    print outer_loop
    inner_loop=0

    start = time.clock()
    rect, frame = c.read()                                          #reading the frames
    span = round((time.clock() - start),2)
    execution_times_outer[outer_loop,inner_loop] = span

    inner_loop+=1

    if not rect:
        break

    raw_frame = frame
    start = time.clock()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                  #gray the image
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop+=1

    start = time.clock()
    fgmask = fgbg.apply(frame)                                       #apply the background remover
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop += 1
    #print span

    start = time.clock()
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)       #morphologyEx function
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop += 1

    current = fgmask

    start = time.clock()
    template = prev[20:-20, -300:-100]                                #selecting the template
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop += 1

    a = (template > 250)

    start = time.clock()
    white = cv2.countNonZero(template[a])                             #Counting White pixels
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop += 1

    tot = template.shape[:2][0] * template.shape[:2][1]
    perc = white * 1000.0 / tot

    start = time.clock()
    diff = cv2.matchTemplate(current, template, method=cv2.TM_CCOEFF_NORMED)        #template matching algorithm
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span
    inner_loop += 1

    start = time.clock()
    loc = cv2.minMaxLoc(diff)                                           #minMax locate algo
    span = round((time.clock() - start), 2)
    execution_times_outer[outer_loop, inner_loop] = span

    inner_loop += 1
    outer_loop += 1

    minVal, maxVal, minLoc, maxLoc = loc

    ref_point = prev.shape[:2][1] - 300
    distance = ref_point - maxLoc[0]

    if perc > white_threshold:


        inst_speed = speedCalc(distance, cam_angle, drain_d, frame_rate, frame_width)       #instant speed calculating function


        values += [inst_speed]
        i += 1
        x = range(0, i)

        vals_for_mean = values[-1 * mean_size:]                           #re-arrange the array


        m = np.mean(vals_for_mean)
        means += [m]

        speed = m

    if len(values) < 1:
        prev = current
        continue

    if videoMode:
        backtorgb = cv2.cvtColor(current, cv2.COLOR_GRAY2RGB)
        vis = np.hstack((raw_frame, backtorgb))

        font = cv2.FONT_HERSHEY_SIMPLEX
        text = 'Speed: %d cm/s\nWhite count: %d' % (speed, round(perc, 2))
        for row, txt in enumerate(text.split('\n')):
            vis = cv2.putText(vis, txt, (10, 50 + 25 * row), font, 0.8, (255, 255, 128), 2)

        if perc > white_threshold:
            vis = cv2.putText(vis, 'Detected: %d cm/s' % inst_speed, (10, 50 + 25 * (row + 1)), font, 0.8,
                              (100, 255, 128), 2)

        cv2.imshow('preview window', vis)
        ch = cv2.waitKey(int(1000.0 / frame_rate))
        if ch == 118:
            cv2.destroyAllWindows()
            videoMode = False
        if ch == 27:
            break
    else:
        plt.clf()
        plt.subplot(321), plt.axis('off'), plt.text(0.25, 0.25,
                                                    'mean sample size: ' + str(mean_size) + '\nmean: ' + str(
                                                        int(m)) + '\nwhite fraction: ' + str(round(perc, 2)),
                                                    horizontalalignment='left', verticalalignment='center', fontsize=10,
                                                    color='red')
        plt.subplot(322), plt.imshow(current, 'gray'), plt.axvline(x=maxLoc[0]), plt.axvline(x=ref_point, color='red')
        plt.subplot(323), plt.plot(x, values), plt.ylabel('speed'), plt.xlabel('frames')
        plt.subplot(324), plt.plot(x, means, label='Mean'), plt.ylabel('avg speed'), plt.xlabel('frames')
        plt.subplot(325), plt.imshow(template)
        plt.subplot(326), plt.imshow(
            current[maxLoc[1]:maxLoc[1] + template.shape[:2][0], maxLoc[0]:maxLoc[0] + template.shape[:2][1]])
        cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)
        plt.pause(0.1)

    if record:
        out.write(raw_frame)

    prev = current

plt.close('all')
cv2.destroyAllWindows()
c.release()
if record:
    out.release()

                  # plot the graph execution_time vs case

average_time_values = execution_times_outer.mean(axis=0)

x_numbers = [0,1,2,3,4,5,6,7]
plt.xticks(x_numbers, performance_graph_titles, rotation='vertical',fontsize='7')

plt.plot(x_numbers,average_time_values)
plt.ylabel('Time taken(s)')
plt.margins(0.2)
plt.subplots_adjust(bottom=0.15)
plt.show()