import cv2
import numpy as np

from skcvideo.colors import RED, WHITE
from skcvideo.utils import put_text


class Plot:
    def __init__(
        self,
        box=None,
        margin=100,
        ticks=None,
        unit="m/s",
        values=None,
        min_value=0.0,
        max_value=10.0,
    ):
        """
        Widget for displaying a curve.
        Arguments:
            box: (list) [x1, y1, x2, y2] coordinates of the delimitation of
                 the widget
            margin: (int) size in pixels of the space left before the curve to
                    write the ticks
            ticks: (list) list of values to be used as a scale on the y axis
            unit: (str) unit used for the values e.g. "m/s"
            values: (list) list of float of shape [n_frames] containing values
                    to be plotted
            min_value: (float) value mapped at the bottom of the plot
            max_value: (float) value mapped at the top of the plot
        """
        if box is None:
            box = [960, 930, 1920, 1065]
        self.box = box
        self.m = margin
        self.ticks = ticks
        self.unit = unit
        self.values = values
        self.min_value = min_value
        self.max_value = max_value

    @property
    def x0(self):
        x1, y1, x2, y2 = self.box
        return x1 + self.m

    def get_y(self, value):
        x1, y1, x2, y2 = self.box
        y = (value - self.min_value) / (self.max_value - self.min_value) * (y2 - y1)
        y = int(np.round(y))
        return y2 - y

    def build(self, image):
        x1, y1, x2, y2 = self.box

        # Draw box
        cv2.rectangle(
            image,
            (self.x0, y1),
            (x2, y2),
            color=WHITE,
            thickness=1,
        )

        # Draw ticks
        if self.ticks is not None:
            for tick in self.ticks:
                y = self.get_y(tick)
                cv2.line(
                    image,
                    (self.x0 - 3, y),
                    (self.x0 + 3, y),
                    color=WHITE,
                    thickness=1,
                )
                put_text(
                    img=image,
                    text=f"{tick:.1f} {self.unit}",
                    org=(self.x0 - 10, y),
                    fontScale=0.5,
                    align_x="right",
                    align_y="center",
                )

        # Draw curve
        for frame in range(x2 - self.x0):
            if frame < len(self.values):
                value = self.values[frame]
                if value is not None:
                    y = self.get_y(value)

                    if not (y1 <= y <= y2):
                        continue

                    image[y, self.x0 + frame] = WHITE

    def refresh(self, image, frame):
        x1, y1, x2, y2 = self.box

        # Draw timer
        cv2.rectangle(
            image,
            (self.x0 + frame, y1),
            (self.x0 + frame, y2),
            color=RED,
            thickness=1,
        )

        # Draw current value
        if frame < len(self.values):
            value = self.values[frame]
            if value is not None:
                y = self.get_y(value)
                put_text(
                    img=image,
                    text=f"{value:.2f} {self.unit}",
                    org=(self.x0 + frame + 5, y - 5),
                    fontScale=0.4,
                    align_x="left",
                    align_y="bottom",
                )
