from .basetool import BaseTool


class VerticalRay(BaseTool):
    type = 'vertical-ray'
    handleCount = 1
    displayName = 'Vertical Line'

    def get_color(self):
        return self.get_option('color', 'theme.rayVerticalColor')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_width(self):
        return self.get_option('width', '1')

    def set_width(self, value):
        return self.set_option('width', value)

    def get_style(self):
        return self.get_option('style', 'solid')

    def set_style(self, value):
        return self.set_option('style', value)
