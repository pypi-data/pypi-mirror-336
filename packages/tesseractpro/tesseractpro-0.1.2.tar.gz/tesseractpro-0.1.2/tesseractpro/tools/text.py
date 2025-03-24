from .basetool import BaseTool


class Text(BaseTool):
    type = 'text'
    handleCount = 1
    displayName = 'Text'

    def get_adaptive(self):
        return self.get_option('adaptive', 'false')

    def set_adaptive(self, value):
        return self.set_option('adaptive', value)

    def get_color(self):
        return self.get_option('color', 'theme.textColor')

    def set_color(self, value):
        return self.set_option('color', value)

    def get_fontsize(self):
        return self.get_option('fontsize', '24')

    def set_fontsize(self, value):
        return self.set_option('fontsize', value)

    def get_text(self):
        return self.get_option('text', 'Type in Text Properties')

    def set_text(self, value):
        return self.set_option('text', value)
