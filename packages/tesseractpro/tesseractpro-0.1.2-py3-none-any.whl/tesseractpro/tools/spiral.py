from .basetool import BaseTool


class Spiral(BaseTool):
    type = 'spiral'
    handleCount = 2
    displayName = 'Spiral'

    def get_show_rectangles(self):
        return self.get_option('show_rectangles', 'false')

    def set_show_rectangles(self, value):
        return self.set_option('show_rectangles', value)

    def get_width(self):
        return self.get_option('width', '1')

    def set_width(self, value):
        return self.set_option('width', value)

    def get_rectangle_color(self):
        return self.get_option('rectangle_color', 'theme.SpiralRectangleColor')

    def set_rectangle_color(self, value):
        return self.set_option('rectangle_color', value)

    def get_color(self):
        return self.get_option('color', 'color.primary')

    def set_color(self, value):
        return self.set_option('color', value)
