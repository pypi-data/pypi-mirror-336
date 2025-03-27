from .basetool import BaseTool


class TurningPoint(BaseTool):
    type = 'turningpoint'
    handleCount = 1
    displayName = 'Turning Point'

    def get_rays(self):
        return self.get_option('rays', '0')

    def set_rays(self, value):
        return self.set_option('rays', value)

    def get_fixedscale(self):
        return self.get_option('fixedscale', '0')

    def set_fixedscale(self, value):
        return self.set_option('fixedscale', value)

    def get_gannbox(self):
        return self.get_option('gannbox', '0')

    def set_gannbox(self, value):
        return self.set_option('gannbox', value)

    def get_doublearcs(self):
        return self.get_option('doublearcs', '0')

    def set_doublearcs(self, value):
        return self.set_option('doublearcs', value)

    def get_show_fib(self):
        return self.get_option('show_fib', '1')

    def set_show_fib(self, value):
        return self.set_option('show_fib', value)

    def get_grid(self):
        return self.get_option('grid', '0')

    def set_grid(self, value):
        return self.set_option('grid', value)

    def get_non_probability(self):
        return self.get_option('non_probability', '0')

    def set_non_probability(self, value):
        return self.set_option('non_probability', value)

    def get_extend_arcs(self):
        return self.get_option('extend_arcs', '0')

    def set_extend_arcs(self, value):
        return self.set_option('extend_arcs', value)

    def get_level(self):
        return self.get_option('level', '1')

    def set_level(self, value):
        return self.set_option('level', value)

    def get_number(self):
        return self.get_option('number', '0')

    def set_number(self, value):
        return self.set_option('number', value)
