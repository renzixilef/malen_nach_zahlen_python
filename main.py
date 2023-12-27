import cv2
import numpy as np
from datetime import datetime
from Inc.color import Color


def get_all_unique_colors_sorted(image):
    colors, count = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
    total_pixels = image.shape[0] * image.shape[1]
    sorted_colors = []
    for i in range(0, len(colors)):
        sorted_colors.append(Color(colors[i], count[i]/total_pixels, bgr=True))
    return sorted_colors








start_time = datetime.now()
print("Started Program...")
print(str(datetime.now()-start_time) + ": Loading Image...")
img = cv2.imread('Malen_Nach_Zahlen_Test.jpg')
print(str(datetime.now()-start_time) + ": Getting and sorting all Colors...")
all_colors = get_all_unique_colors_sorted(img)
print(str(datetime.now()-start_time) + ": Converting Colors to Lab color range...")
for color in all_colors:
    color.calculate_lab()
print(str(datetime.now()-start_time) + ": Getting weighted distances between colors...")
for color in all_colors:
    color.calculate_weighted_distances(all_colors)
for i in all_colors:
    print(i.total_distance)
