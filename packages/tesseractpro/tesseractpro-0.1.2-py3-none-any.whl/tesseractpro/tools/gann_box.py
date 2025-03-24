from .basetool import BaseTool


class GannBox(BaseTool):
    type = 'gann-box'
    handleCount = 2
    displayName = 'Gann Box'

    def get_color(self):
        return self.get_option('color', 'theme.gannBoxLineColor')

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

    def get_labels(self):
        return self.get_option('labels', 'true')

    def set_labels(self, value):
        return self.set_option('labels', value)

    def get_levels_time(self):
        return self.get_option('levels_time', '[{ "visible": true, "angle": false, "level": 0.125 }, { "visible": true, "angle": false, "level": 0.25 }, { "visible": true, "angle": false, "level": 0.382 }, { "visible": true, "angle": true, "level": 0.5 }, { "visible": true, "angle": false, "level": 0.618 }, { "visible": true, "angle": false, "level": 0.786 }, { "visible": true, "angle": false, "level": 0.886 }]')

    def set_levels_time(self, value):
        return self.set_option('levels_time', value)

    def get_levels_price(self):
        return self.get_option('levels_price', '[{ "visible": true, "angle": false, "level": 0.125 }, { "visible": true, "angle": false, "level": 0.25 }, { "visible": true, "angle": false, "level": 0.382 }, { "visible": true, "angle": true, "level": 0.5 }, { "visible": true, "angle": false, "level": 0.618 }, { "visible": true, "angle": false, "level": 0.786 }, { "visible": true, "angle": false, "level": 0.886 }]')

    def set_levels_price(self, value):
        return self.set_option('levels_price', value)
