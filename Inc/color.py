import numpy as np


class Color:

    @classmethod
    def create_color_from_lab_and_percentage(cls, lab, percentage):
        INVERSE_CONVERSION_MATRIX = np.linalg.inv(np.array(
            [[0.412453, 0.357580, 0.180423],
             [0.212671, 0.715160, 0.072169],
             [0.019334, 0.119193, 0.950227]]))
        XN = 0.950456
        ZN = 1.088754

        def y(L):
            y_k = ((L + 16) / 116) ** 3
            if y_k > 0.008856:
                return y_k
            else:
                return L / 903.3

        def t(y, a=None, b=None):
            f_of_y = y ** (1 / 3) if y > 0.00856 else 7.787 * y + 16 / 116
            ret_value = 0
            if a is not None:
                ret_value = a / 500 + f_of_y
            elif b is not None:
                ret_value = - b / 200 + f_of_y
            ret_value_t = ret_value ** 3
            if ret_value_t > 0.008856:
                return ret_value
            else:
                return (ret_value - 16 / 116) / 7.787

        Y = y(lab[0])
        X_n = t(Y, a=lab[1])
        Z_n = t(Y, b=lab[2])
        Z = Z_n * ZN
        X = X_n * XN

        color_rgb = np.dot(INVERSE_CONVERSION_MATRIX, np.array([X, Y, Z]))*255
        return cls(color_rgb, percentage, str(color_rgb), bgr = True)

    def __init__(self, color_rgb, percentage, own_color_key, count_pixel=0, bgr=False):
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
