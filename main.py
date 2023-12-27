import cv2
import numpy as np
from datetime import datetime
from Inc.color import Color

KEEP_COLORS = 4


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
print(str(datetime.now() - start_time) + ": Sorting colors by total weighted distance...")
sorted_all_colors = sorted(all_colors, key=lambda color: color.total_distance)
common_colors = sorted_all_colors[:KEEP_COLORS]
common_colors_with_rel_colors = []
print(str(datetime.now()-start_time) + ": Group nearest Colors to Common Colors...")
for color in common_colors:
    common_colors_with_rel_colors.append([color, []])
for color in sorted_all_colors:
    smallest_distance = common_colors[0].get_distance_to_color(color)
    smallest_distance_common_color = common_colors[0]
    for common_color in common_colors:
        if smallest_distance > common_color.get_distance_to_color(color):
            smallest_distance = common_color.get_distance_to_color(color)
            smallest_distance_common_color = common_color
    for common_color_rel_array in common_colors_with_rel_colors:
        if common_color_rel_array[0] == smallest_distance_common_color:
            common_color_rel_array[1].append([color, smallest_distance])
print(common_colors_with_rel_colors[0])
print(common_colors_with_rel_colors[1])
print(common_colors_with_rel_colors[2])
print(common_colors_with_rel_colors[3])