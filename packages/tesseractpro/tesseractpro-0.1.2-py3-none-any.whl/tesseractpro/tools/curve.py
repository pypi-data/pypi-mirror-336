from .basetool import BaseTool


class Curve(BaseTool):
    type = 'curve'
    handleCount = 3
    displayName = 'Curve'

    def get_color(self):
        return self.get_option('color', 'color.primary')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_width(self):
        return self.get_option('width', '2')

    def set_width(self, value):
        return self.set_option('width', value)

    def get_style(self):
        return self.get_option('style', 'solid')

    def set_style(self, value):
        return self.set_option('style', value)
