import sys
import time
import socketio
import math

from .tools import Tools
from .markets import Markets
from .alerts import Alerts
from .restclient import RestClient
from .decorators.on import on
from .utils.socketio_utils import register_socketio_events
from .errors import ApiTokenError, AuthenticationTimeoutError
from .indicators.mtops.checklist import Checklist
from .timewindow import TimeWindow
from .chart import Chart

# Make sure we're not running inside an unsupported environment
if sys.version_info < (3, 9):
    raise RuntimeError(
        "The Tesseract Pro Python API requires Python 3.9 or higher.")


class TesseractPro:
    authenticated = False

    def __init__(self, api_token, server_url="https://piper.tesseractpro.io"):
        self.api_token = api_token
        self.server_url = server_url
        self._socket = socketio.Client()

        # Register TesseractPro events
        register_socketio_events(self, self._socket)

        self._socket.connect(
            self.server_url,
            namespaces=['/api'],
            auth={'token': self.api_token}
        )

        timeout = 10
        start_time = time.time()
        while not self.authenticated:
            timed_out = time.time() - start_time > timeout
            if timed_out or not self._socket.connected:
                if self._socket.connected:
                    raise AuthenticationTimeoutError(
                        "Authentication timed out")
                else:
                    raise ApiTokenError("Invalid token provided")

                self._socket.disconnect()
                exit(1)
            time.sleep(0.1)

        self.tool = Tools(self)
        self.market = Markets(self)
        self.rest = RestClient(self)
        self.alert = Alerts(self)

    def get_indicator(self, name: str):
        match name:
            case "mtops":
                return Checklist(self)

    def get_chart(
        self,
        space_id: str,
        timeframe: int,
        symbol: str,
        start_time: int,
        end_time: int,
    ) -> Chart:
        candles = math.ceil((start_time - end_time) / (timeframe * 60))
        time_window = TimeWindow(timeframe, start_time, candles)

        return Chart(
            tesseract_pro=self,
            symbol=symbol,
            space_id=space_id,
            timeframe=timeframe,
            time_window=time_window
        )

    def disconnect(self) -> None:
        self.authenticated = False
        self._socket.disconnect()

    def wait_for_events(self) -> None:
        self._socket.wait()

    @on("invalid_api_token")
    def on_token_error(self) -> None:
        self.disconnect()

    @on("authenticated")
    def on_authenticated(self, data) -> None:
        self.authenticated = True

    @on("disconnect")
    def on_disconnect(self) -> None:
        self.authenticated = False

    @on("error")
    def on_connect_error(self, data) -> None:
        self.authenticated = False

    def close(self) -> None:
        self.authenticated = False
        self._socket.disconnect()
