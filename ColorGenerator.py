import random


class ColorGenerator:
    """This is a module to generate colors """

    def __init__(self):
        self.selected_colors = []

    def get_colors(self, transparency=0.5):
        """Generator which list colors infinitely"""
        count = 0
        while True:
            count += 1
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if color not in self.selected_colors or count > 50:
                r, g, b = color
                self.selected_colors.append(color)
                yield f'rgba({r}, {g}, {b}, {transparency})',
            else:
                continue

    def get_solid_selected_colors(self, transparency=1):
        colors = []
        for color in self.selected_colors:
            r, g, b = color
            colors.append(f'rgba({r}, {g}, {b}, {transparency})')
        return colors