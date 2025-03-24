from .basetool import BaseTool


class Arrow(BaseTool):
    type = 'arrow'
    handleCount = 2
    displayName = 'Arrow'

    def get_color(self):
        return self.get_option('color', 'theme.toolArrowRedBackgroundColor')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_borderColor(self):
        return self.get_option('borderColor', 'theme.toolArrowRedBorderColor')

    def set_borderColor(self, value):
        return self.set_option('borderColor', value)
