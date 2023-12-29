import cv2
import numpy as np
from datetime import datetime
from Inc.color import Color
from PIL import Image

KEEP_COLORS = 24
COUNT_THREADS = 1
PATH_TO_IMAGE = "img/test2"
IMAGE_EXTENSION = ".jpg"


def get_all_unique_colors_sorted(image):
    colors, count = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
    total_pixels = image.shape[0] * image.shape[1]
    sorted_colors = {}
    for k in range(0, len(colors)):
        sorted_colors[str(colors[k])] = Color(colors[k], count[k] / total_pixels, str(colors[k]), count[k], bgr=True)
    return total_pixels, sorted_colors


def append_common_colors_rest(array_to_append, color_dict, count_colors_to_keep):
    for i in range(1, count_colors_to_keep):
        average_lab = get_average_lab(array_to_append)
        highest_weighted_distance = 0
        append_color_key = None
        for color_value in color_dict.values():
            if color_value not in array_to_append:
                dist = color_value.get_lab_distance_multiplied_with_percentage(average_lab)
                if dist > highest_weighted_distance:
                    highest_weighted_distance = dist
                    append_color_key = color_value.this_color_key
        array_to_append.append(color_dict[append_color_key])


def get_average_lab(array_to_calculate):
    labs = []
    for i in array_to_calculate:
        labs.append(i.lab*i.percentage)
    return np.mean(np.array(labs))


def replace_colors_with_common_colors(image, color_dict):
    last_print_percent = -1
    for i in range(0, len(image)):
        if int(i / len(image) * 100) >= last_print_percent:
            last_print_percent += 1
            print(f"{last_print_percent} %")
        for k in range(0, len(image[i])):
            image[i][k] = np.array(all_colors[color_dict[str(image[i][k])].replacement_key].bgr)
    return image


start_time = datetime.now()
print("Started Program...")
print(str(datetime.now() - start_time) + ": Loading Image...")

pil_img = Image.open(PATH_TO_IMAGE + IMAGE_EXTENSION)
pil_img = pil_img.convert("P", palette=Image.ADAPTIVE, colors=256)
pil_img.save(PATH_TO_IMAGE + ".png")
img_bgr = cv2.imread(PATH_TO_IMAGE + ".png")
print(img_bgr[0][0])
print(str(datetime.now() - start_time) + ": Getting and sorting all Colors...")
count_pixels, all_colors = get_all_unique_colors_sorted(img_bgr)
print("TOTAL COLORS: " + str(len(all_colors)))
print(str(datetime.now() - start_time) + ": Converting Colors to Lab color range...")
for color in all_colors.values():
    color.calculate_lab()
print(str(datetime.now() - start_time) + ": Getting weighted distances between colors...")
last_print = -1
for index, key in enumerate(all_colors):
    if int(index / len(all_colors) * 100) >= last_print:
        last_print += 1
        print(f"{last_print} %")
    all_colors[key].calculate_weighted_distances(all_colors)
print(str(datetime.now() - start_time) + ": Sorting colors by total weighted distance...")
sorted_all_colors = sorted(all_colors.values(), key=lambda this_color: this_color.total_distance)
common_colors = [sorted_all_colors[0]]
append_common_colors_rest(common_colors, all_colors, KEEP_COLORS)
common_colors_keys = []
for index in range(0, len(common_colors)):
    common_colors_keys.append(common_colors[index].this_color_key)
print(str(datetime.now() - start_time) + ": Group nearest Colors to Common Colors...")
common_colors_with_rel_colors = {}
for common_color_key in common_colors_keys:
    common_colors_with_rel_colors[common_color_key] = []
for key in all_colors.keys():
    smallest_distance = all_colors[common_colors_keys[0]].get_distance_to_color(key)
    smallest_distance_common_color_key = common_colors_keys[0]
    for common_color_key in common_colors_keys:
        distance = all_colors[common_color_key].get_distance_to_color(key)
        if smallest_distance > distance:
            smallest_distance = distance
            smallest_distance_common_color_key = common_color_key
    common_colors_with_rel_colors[smallest_distance_common_color_key].append(key)
print(str(datetime.now() - start_time) + ": Calculating replacement colors for common Color groups...")
#TODO: fix this mess
for common_color_key in common_colors_with_rel_colors:
    rgbs = []
    pixels = []
    for color_key in common_colors_with_rel_colors[common_color_key]:
        rgbs.append(all_colors[color_key].lab)
        pixels.append(all_colors[color_key].count_pixel)
    pixels_divided = np.divide(pixels, np.sum(pixels))
    pixels_divided_reshaped = np.reshape(pixels_divided, (len(pixels_divided), 1))
    weighted_labs = np.multiply(rgbs, pixels_divided_reshaped)
    replacement_color_rgb = np.sum(weighted_labs, axis=0)
    replacement_color = Color(replacement_color_rgb, np.sum(pixels)/count_pixels, str(replacement_color_rgb))
    replacement_color_key = replacement_color.this_color_key
    all_colors[replacement_color_key] = replacement_color
    for color in common_colors_with_rel_colors[common_color_key]:
        all_colors[color].replacement_key = replacement_color_key
print(str(datetime.now() - start_time) + ": Replacing Colors with common colors...")
img_bgr = replace_colors_with_common_colors(img_bgr, all_colors)
print("TOTAL COLORS NOW: " + str(len(get_all_unique_colors_sorted(img_bgr)[1])))
print(str(datetime.now() - start_time) + ": Saving image...")
cv2.imwrite('output2.png', img_bgr)
# print(common_colors_with_rel_colors[0])
# print(common_colors_with_rel_colors[1])
# print(common_colors_with_rel_colors[2])
# print(common_colors_with_rel_colors[3])
