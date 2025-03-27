from .basetool import BaseTool


class GannSquare(BaseTool):
    type = 'gann-square'
    handleCount = 2
    displayName = 'Gann Square'

    def get_color(self):
        return self.get_option('color', 'theme.gannSquareLineColor')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_gannbox(self):
        return self.get_option('gannbox', '0')

    def set_gannbox(self, value):
        return self.set_option('gannbox', value)

    def get_doublearcs(self):
        return self.get_option('doublearcs', '0')

    def set_doublearcs(self, value):
        return self.set_option('doublearcs', value)
