from .utils.event_emitter import EventEmitter
from .timewindow import TimeWindow
from .errors import ToolHandleCountError, ToolExistsError
from .tools.all_tools import get_tool_instance_by_type

class Chart(EventEmitter):
    ON_TOOL_UPDATE = "tool:update"
    ON_TOOL_ADD = "tool:add"
    ON_TOOL_REMOVE = "tool:remove"
    ON_ALERT_TRIGGER = "alert:trigger"
    ON_ALERT_ADD = "alert:add"
    ON_ALERT_UPDATE = "alert:update"
    ON_ALERT_REMOVE = "alert:remove"
    ON_PRICE = "price"

    def __init__(self,
                 tesseract_pro,
                 space_id: str,
                 timeframe: int,
                 symbol: str,
                 time_window: TimeWindow
                 ):
        super().__init__()

        self.space_id = space_id
        self.timeframe = timeframe
        self.time = time_window
        self.symbol = symbol
        self.tpro = tesseract_pro

        self.tpro.market.subscribe(symbol)

        # create event listeners
        def create_handler(context, event):
            return lambda data: self.handle_event(context, event, data)

        self.tpro.tool.on("update", create_handler("tool", "update"))
        self.tpro.tool.on("add", create_handler("tool", "add"))
        self.tpro.tool.on("remove", create_handler("tool", "remove"))

        self.tpro.alert.on("trigger", create_handler("alert", "trigger"))
        self.tpro.alert.on("add", create_handler("alert", "add"))
        self.tpro.alert.on("update", create_handler("alert", "update"))
        self.tpro.alert.on("remove", create_handler("alert", "remove"))

        self.tpro.market.on(
            "pricechange", lambda data: self.handle_price_change(data))

    def handle_price_change(self, data):
        if data[0] == self.symbol:
            self.emit('price', data[1])

    def handle_event(self, context, event, data):
        if context == 'alert' and data['symbol'] == self.symbol:
            self.emit(f'{context}:{event}', data)
            return

        # Event may not be bound to timeframe
        if "timeframe" not in data:
            self.emit(f'tool:{event}', get_tool_instance_by_type(data['type'], data))
            return

        # Not for us
        if data['timeframe'] != self.timeframe:
            return

        # Lets go!
        if (context == 'tool'):
            self.emit(f'tool:{event}', get_tool_instance_by_type(data['type'], data))
        else:
            self.emit(f'{context}:{event}', data)

    def get_candles(self):
        # TODO: We should cache the candles until the timeWindow is changed

        data = self.tpro.rest.post('ohlc', {
            "from": self.time.get_start_time(),
            "count": self.time.candles,
            "timeframe": self.timeframe,
            "market": self.symbol
        })

        return data

    def get_tools(self):
        data = self.tpro.tool.get_tools(
            from_unix=self.time.get_start_time(),
            to_unix=self.time.get_end_time(),
            timeframe=self.timeframe,
            market=self.symbol,
            space_id=self.space_id
        )

        # Attach to chart
        for id in data:
            data[id].chart = self

        return data

    def add_tool(self, tool):
        if len(tool.get_handles()) != tool.handleCount:
            raise ToolHandleCountError(
                f"Not enought handles ({len(tool.get_handles())} of {tool.handleCount}) to add {tool.get_type()} tool")

        if tool.get_id() is not None:
            raise ToolExistsError(
                f"Tool already exists with id {tool.get_id()}")

        id = self.tpro.tool.add_tool(
            tool,
            timeframe=self.timeframe * 60,
            symbol=self.symbol,
            space_id=self.space_id
        )

        tool.set_id(id)
        tool.chart = self

        print(f"added tool id {id}")

    def remove_tool(self, tool):
        self.tpro.tool.remove_tool(self.space_id, tool)

    def wait_for_events(self):
        self.tpro.wait_for_events()
