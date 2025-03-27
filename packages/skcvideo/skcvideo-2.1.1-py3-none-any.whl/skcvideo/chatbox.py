import cv2

from skcvideo.colors import WHITE
from skcvideo.utils import put_text


class ChatBox:
    def __init__(
        self,
        box=None,
        data=None,
        row_height=20,
    ):
        """
        A widget to display text appearing gradually along with the video.
        box: list of coordinates defining the widget delimitation
        data: list of dict
            {
                "frame": (int) frame from which to display the text
                "text": (str) text to be displayed
                "color": (list) or (tuple) of length 3, containing RGB values
                        defines color of the text
            }
        """
        if box is None:
            box = [0, 0, 1920, 1080]
        if data is None:
            data = []
        self.box = box
        self.data = data
        self.row_height = row_height

        x1, y1, x2, y2 = self.box
        self.number_of_rows = int((y2 - y1) / self.row_height)

    def build(self, image):
        x1, y1, x2, y2 = self.box
        image[y1:y2, x1:x2] = 0

        # Draw box
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color=WHITE,
            thickness=2,
        )

    def refresh(self, image, frame):
        x1, y1, x2, y2 = self.box

        # Prepare texts to be displayed
        lines = []
        for d in self.data:
            if d["frame"] <= frame:
                lines.append(d)

        lines = lines[-self.number_of_rows :]
        offset = self.number_of_rows - len(lines)

        # Draw texts
        for i, d in enumerate(lines):
            y = int(round(y1 + (offset + i + 0.5) * self.row_height))
            put_text(
                image,
                d["text"],
                (x1 + 5, y),
                fontScale=0.5,
                align_x="left",
                align_y="center",
                color=d["color"],
            )
