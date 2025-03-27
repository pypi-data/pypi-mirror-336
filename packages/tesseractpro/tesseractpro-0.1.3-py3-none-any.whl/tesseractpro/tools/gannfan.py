from .basetool import BaseTool


class GannFan(BaseTool):
    type = 'gannfan'
    handleCount = 2
    displayName = 'Gann Fan'

    def get_color(self):
        return self.get_option('color', 'color.primary')

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

    def get_levels(self):
        return self.get_option('levels', '[{"visible": true,"level":8},{"visible": true,"level":4},{"visible": true,"level":3},{"visible": true,"level":2},{"visible": true,"level":1}]')

    def set_levels(self, value):
        return self.set_option('levels', value)
