import numpy as np


class Color:

    def __init__(self, color_rgb, percentage, bgr=False):
        if bgr:
            self.rgb = np.array([color_rgb[2], color_rgb[1], color_rgb[0]])
        else:
            self.rgb = np.array([color_rgb[0], color_rgb[1], color_rgb[2]])
        self.lab = None
        self.percentage = percentage
        self.distance = []
        self.total_distance = 0

    def calculate_weighted_distances(self, all_colors):
        weighted_distances = np.empty((len(all_colors) - 1))

        for k in range(0, len(all_colors)):
            if all_colors[k] != self:
                self.distance.append(
                    [all_colors[k], np.linalg.norm(self.lab - all_colors[k].lab) * all_colors[k].percentage])
        for i in self.distance:
            self.total_distance += i[1]

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
