from .base import Base
from .decorators.on import on


class Alerts (Base):
    @on("alert:trigger")
    def on_alert_trigger(self, data) -> None:
        self.emit('trigger', data)

    @on("alert:add")
    def on_tools_added(self, data) -> None:
        self.emit('add', data)

    @on("alert:update")
    def on_tool_update(self, data) -> None:
        self.emit('update', data)

    @on("alert:remove")
    def on_tool_remove(self, data) -> None:
        self.emit('remove', data)
