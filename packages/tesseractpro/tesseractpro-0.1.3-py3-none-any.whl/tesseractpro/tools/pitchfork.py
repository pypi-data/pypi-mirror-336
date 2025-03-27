from .basetool import BaseTool


class PitchFork(BaseTool):
    type = 'pitchfork'
    handleCount = 3
    displayName = 'Pitch Fork'

    def get_color(self):
        return self.get_option('color', 'theme.PitchForkLineColor')

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
        return self.get_option('levels', '[{"visible":false,"level":0.25},{"visible":false,"level":0.382},{"visible":true,"level":0.5},{"visible":false,"level":0.618},{"visible":false,"level":0.75},{"visible":true,"level":1},{"visible":false,"level":1.5},{"visible":false,"level":1.75},{"visible":false,"level":2}]')

    def set_levels(self, value):
        return self.set_option('levels', value)
