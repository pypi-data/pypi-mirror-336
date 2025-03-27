from .basetool import BaseTool


class Protractor(BaseTool):
    type = 'protractor'
    handleCount = 1
    displayName = 'Protractor'

    def get_type(self):
        return self.get_option('type', '2')

    def set_type(self, value):
        return self.set_option('type', value)

    def get_doublearcs(self):
        return self.get_option('doublearcs', '0')

    def set_doublearcs(self, value):
        return self.set_option('doublearcs', value)
