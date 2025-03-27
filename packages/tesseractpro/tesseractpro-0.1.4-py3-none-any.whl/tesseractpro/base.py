from .utils.event_emitter import EventEmitter
from .utils.socketio_utils import register_socketio_events


class Base (EventEmitter):
    def __init__(self, tesseract_pro):
        super().__init__()

        register_socketio_events(self, tesseract_pro._socket)

        self._tpro = tesseract_pro
