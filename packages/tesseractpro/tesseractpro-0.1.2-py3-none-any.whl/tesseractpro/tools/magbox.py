from .basetool import BaseTool


class MagBox(BaseTool):
    type = 'magbox'
    handleCount = 2
    displayName = 'Rectangle'

    def get_color(self):
        return self.get_option('color', 'rgba(235, 227, 12, 0.1)')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_borderColor(self):
        return self.get_option('borderColor', 'rgb(171,170,41)')

    def set_borderColor(self, value):
        return self.set_option('borderColor', value)

    def get_width(self):
        return self.get_option('width', '2')

    def set_width(self, value):
        return self.set_option('width', value)

    def get_style(self):
        return self.get_option('style', 'solid')

    def set_style(self, value):
        return self.set_option('style', value)
