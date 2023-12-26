import cv2
import numpy as np
from datetime import datetime


def get_all_unique_colors_sorted(image):
    colors, count = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
    total_pixels = image.shape[0] * image.shape[1]
    sorted_colors = []
    number_of_colors = []
    for i in range(0, len(colors)):
        if count[i] >= 0.1 * total_pixels:
            sorted_colors.append(colors[i])
            number_of_colors.append(count[i])
    return np.stack(sorted_colors), number_of_colors


def convert_array_to_LAB(rgb_colors):
    def f(t):
        if t > 0.008856:
            return t ** (1 / 3)
        else:
            return 7.787 * t + 16 / 116

    def L(y):
        if y > 0.008856:
            return 116 * (y ** (1 / 3)) - 16
        else:
            return 903.3 * y

    CONVERSION_MATRIX = np.array(
        [[0.412453, 0.357580, 0.180423],
         [0.212671, 0.715160, 0.072169],
         [0.019334, 0.119193, 0.950227]])
    XN = 0.950456
    ZN = 1.088754
    all_colors_xyz = np.empty_like(rgb_colors, dtype=float)
    all_colors_lab = np.empty_like(rgb_colors, dtype=float)
    for i in range(0, len(rgb_colors)):
        all_colors_xyz[i] = np.array([np.dot(CONVERSION_MATRIX, rgb_colors[i] * 1 / 255)[0] / XN,
                                      np.dot(CONVERSION_MATRIX, rgb_colors[i] * 1 / 255)[1],
                                      np.dot(CONVERSION_MATRIX, rgb_colors[i] * 1 / 255)[2] / ZN])
    for i in range(0, len(all_colors_lab)):
        all_colors_lab[i] = np.array([L(all_colors_xyz[i][1]),
                                      500 * (f(all_colors_xyz[i][0]) - f(all_colors_xyz[i][1])),
                                      200 * (f(all_colors_xyz[i][1]) - f(all_colors_xyz[i][2]))])
    return all_colors_lab


def calculate_weighted_distances(lab_colors, count):
    weighted_distances = np.empty((len(lab_colors)))
    total = sum(count)
    for i in range(0, len(lab_colors)):
        weighted_distance = 0
        for k in range(0, len(lab_colors)):
            weighted_distance += np.linalg.norm(lab_colors[i]-lab_colors[k]) * count[k]/total
        weighted_distances[i] = weighted_distance
    return weighted_distances


start_time = datetime.now()
print("Started Program...")
print(str(datetime.now()-start_time) + ": Loading Image...")
img = cv2.imread('Malen_Nach_Zahlen_Test.jpg')
print(str(datetime.now()-start_time) + ": Getting and sorting all Colors...")
all_colors_BGR, colors_count = get_all_unique_colors_sorted(img)
all_colors_RGB = np.stack([np.flip(i) for i in all_colors_BGR])
print(str(datetime.now()-start_time) + ": Converting Colors to Lab color range...")
all_colors_LAB = convert_array_to_LAB(all_colors_RGB)
print(str(datetime.now()-start_time) + ": Getting weighted distances between colors...")
all_colors_LAB_distance = calculate_weighted_distances(all_colors_LAB, colors_count)
print(all_colors_LAB_distance)
