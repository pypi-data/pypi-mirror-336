from .basetool import BaseTool


class GannGrid(BaseTool):
    type = 'gann-grid'
    handleCount = 2
    displayName = 'Gann Grid'

    def get_show_grid(self):
        return self.get_option('show_grid', 'true')

    def set_show_grid(self, value):
        return self.set_option('show_grid', value)
