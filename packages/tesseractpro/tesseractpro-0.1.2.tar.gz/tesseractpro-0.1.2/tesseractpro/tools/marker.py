from .basetool import BaseTool


class Marker(BaseTool):
    type = 'marker'
    handleCount = 1
    displayName = 'Target'

    def get_show_label(self):
        return self.get_option('show_label', 'true')

    def set_show_label(self, value):
        return self.set_option('show_label', value)
