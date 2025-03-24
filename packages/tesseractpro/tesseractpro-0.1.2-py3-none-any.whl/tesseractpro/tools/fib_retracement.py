from .basetool import BaseTool


class FibRetracement(BaseTool):
    type = 'fib-retracement'
    handleCount = 2
    displayName = 'Fibonacci Retracement'

    def get_extendLeft(self):
        return self.get_option('extendLeft', '0')

    def set_extendLeft(self, value):
        return self.set_option('extendLeft', value)

    def get_extendRight(self):
        return self.get_option('extendRight', '0')

    def set_extendRight(self, value):
        return self.set_option('extendRight', value)

    def get_trendline(self):
        return self.get_option('trendline', '0')

    def set_trendline(self, value):
        return self.set_option('trendline', value)

    def get_levels(self):
        return self.get_option('levels', '[{ "visible": true, "level": 0 }, { "visible": true, "level": 0.236 }, { "visible": true, "level": 0.382 }, { "visible": true, "level": 0.5 }, { "visible": true, "level": 0.618 }, { "visible": true, "level": 0.786 }, { "visible": true, "level": 1 }, { "visible": true, "level": 1.618 }, { "visible": true, "level": 2.618 } ]')

    def set_levels(self, value):
        return self.set_option('levels', value)

    def get_color(self):
        return self.get_option('color', 'theme.FibRetracementLineColor')

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
