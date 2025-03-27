from typing import Union
from .decorators.on import on
from .base import Base


class Markets (Base):
    def subscribe(self, symbol: Union[tuple[str, ...], str]) -> None:
        """
        Subscribe to one or more markets events
        """

        if isinstance(symbol, str):
            symbol = [symbol]

        self._tpro._socket.emit(
            'market:subscribe',
            {'symbols': symbol},
            namespace="/api"
        )

    @on("market:pricechange")
    def on_price_change(self, data: tuple[str, int]) -> None:
        self.emit('pricechange', (data[0], data[1]))
