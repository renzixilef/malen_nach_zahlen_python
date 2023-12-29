import numpy as np


class Color:

    @classmethod
    def create_color_from_lab_and_percentage (cls, lab, percentage):
        color_rgb = np.array ([])


    def __init__(self, color_rgb, percentage, own_color_key, count_pixel, bgr=False):
        if bgr:
            self.rgb = np.array([color_rgb[2], color_rgb[1], color_rgb[0]])
            self.bgr = np.array([color_rgb[0], color_rgb[1], color_rgb[2]])
        else:
            self.rgb = np.array([color_rgb[0], color_rgb[1], color_rgb[2]])
            self.bgr = np.array([color_rgb[2], color_rgb[1], color_rgb[0]])
        self.lab = None
        self.percentage = percentage
        self.count_pixel = count_pixel
        self.distance = {}
        self.total_distance = 0
        self.this_color_key = own_color_key
        self.replacement_key = None

    def calculate_weighted_distances(self, all_colors):

        for key in all_colors.keys():
            if all_colors[key] != self and key not in self.distance:
                distance_value = [np.linalg.norm(self.lab - all_colors[key].lab) / all_colors[key].percentage,
                                  np.linalg.norm(self.lab - all_colors[key].lab)]
                self.distance[key] = distance_value
                all_colors[key].distance[self.this_color_key] = distance_value
        for value in self.distance.values():
            self.total_distance += value[0]

    def calculate_lab(self):
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
        color_xyz = np.array([np.dot(CONVERSION_MATRIX, self.rgb * 1 / 255)[0] / XN,
                              np.dot(CONVERSION_MATRIX, self.rgb * 1 / 255)[1],
                              np.dot(CONVERSION_MATRIX, self.rgb * 1 / 255)[2] / ZN])
        self.lab = np.array([L(color_xyz[1]),
                             500 * (f(color_xyz[0]) - f(color_xyz[1])),
                             200 * (f(color_xyz[1]) - f(color_xyz[2]))])

    def get_distance_to_color(self, color_key):
        if color_key == self.this_color_key:
            return 0
        else:
            return self.distance[color_key][1]

    def get_lab_distance_multiplied_with_percentage(self, lab):
        return np.linalg.norm(self.lab - lab) * self.percentage

