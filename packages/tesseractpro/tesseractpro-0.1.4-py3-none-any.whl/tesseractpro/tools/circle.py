from .basetool import BaseTool


class Circle(BaseTool):
    type = 'circle'
    handleCount = 2
    displayName = 'Circle'

    def get_color(self):
        return self.get_option('color', 'theme.circleLineBackgroundColor')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_borderColor(self):
        return self.get_option('borderColor', 'theme.circleLineColor')

    def set_borderColor(self, value):
        return self.set_option('borderColor', value)

    def get_drawBackground(self):
        return self.get_option('drawBackground', 'false')

    def set_drawBackground(self, value):
        return self.set_option('drawBackground', value)

    def get_width(self):
        return self.get_option('width', '1')

    def set_width(self, value):
        return self.set_option('width', value)

    def get_style(self):
        return self.get_option('style', 'solid')

    def set_style(self, value):
        return self.set_option('style', value)
