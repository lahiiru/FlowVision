import numpy as np
import cv2
from matplotlib import pyplot as plt
from iteration_2.src.LSPIV.core import PointAroundComparator

debug = False

path = '../resources/double_exposed_webcam/'
for no in [12, 14, 16, 20, 22]:
    img = cv2.imread(path + str(no) + '.jpg')
    b, g, r = cv2.split(img)

    cr = cv2.goodFeaturesToTrack(r, 50, 0.01, 5)
    cr = np.int0(cr)

    cb = cv2.goodFeaturesToTrack(b, 50, 0.01, 5)
    cb = np.int0(cb)

    corners = np.concatenate((cb, cr), 0)
    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, 255, -1)

    plt.imshow(img), plt.show()
    comparator = PointAroundComparator()

    if debug:
        vis = comparator.compare(r, b, center=(x, y), template_radius=20, matching_radius=60)
        cv2.imshow('vis', vis)
        cv2.waitKey(0)

    comparator.debug = False
    distances = []
    for i in corners:
        x, y = i.ravel()
        d = comparator.compare(r, b, center=(x, y), template_radius=20, matching_radius=60)[0]
        if abs(d) > 1:
            distances += [d]
    hist = plt.hist(distances, 60)
    maxBinUpper = np.argmax(hist[0])
    dist = (hist[1][maxBinUpper + 1] + hist[1][maxBinUpper]) / 2.0
    print (no, dist)
    plt.show()


    # offset = 50
    # w_min, h_min = tuple(np.min(corners, 0)[0])
    # w_max, h_max = tuple(np.max(corners, 0)[0])
    # if h_min > offset:
    #     h_min -= offset
    # else:
    #     h_min = 0
    # if w_min > offset:
    #     w_min -= offset
    # else:
    #     w_min = 0
    # h_max += offset
    # w_max += offset
    # img = img[h_min:h_max,w_min:w_max]
    # plt.imshow(img),plt.show()