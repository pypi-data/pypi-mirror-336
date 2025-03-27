import matplotlib.cm as cm
import numpy as np


class Colormap:
    def __init__(self, value_green=0.0, value_red=1.0):
        """
        A colormap utility that maps scalar values to RGB colors using a
        modified 'jet' colormap.
        Methods:
            get(value): Returns the RGB color corresponding to the input value,
                        scaled between value_green and value_red.
        """

        self.value_green = value_green
        self.value_red = value_red

        self.colormap = cm.jet(np.linspace(0, 1, 200))
        self.colormap = self.colormap[100:][:, [2, 1, 0]]
        self.colormap = np.round(self.colormap * 255).tolist()

    def get(self, value):
        color_i = int((value - self.value_green) / (self.value_red - self.value_green) * 100.0)
        if color_i < 0:
            color_i = 0
        if color_i >= 100:
            color_i = 99
        color = self.colormap[color_i]
        return color
