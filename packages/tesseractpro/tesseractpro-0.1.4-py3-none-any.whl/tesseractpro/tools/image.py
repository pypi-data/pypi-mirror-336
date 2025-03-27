from .basetool import BaseTool


class Image(BaseTool):
    type = 'image'
    handleCount = 2
    displayName = 'Image'

    def get_imageSrc(self):
        return self.get_option('imageSrc', '')

    def set_imageSrc(self, value):
        return self.set_option('imageSrc', value)

    def get_opacity(self):
        return self.get_option('opacity', '100')

    def set_opacity(self, value):
        return self.set_option('opacity', value)
