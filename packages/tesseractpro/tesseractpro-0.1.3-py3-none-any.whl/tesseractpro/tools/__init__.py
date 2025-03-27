
from .all_tools import *

from ..base import Base
from ..decorators.on import on
from ..utils import timeframe_align


class Tools (Base):
    @on("tool:add")
    def on_tools_added(self, data) -> None:
        self.emit('add', data)

    @on("tool:update")
    def on_tool_update(self, data) -> None:
        self.emit('update', data)

    @on("tool:remove")
    def on_tool_remove(self, data) -> None:
        self.emit('remove', data)

    def remove_tool(self, space_id, tool):
        self._tpro.rest.delete(f"tools/{space_id}/{tool.get_id()}")

    def add_tool(
        self,
        tool,
        timeframe,
        symbol,
        space_id
    ):
        handles = tool.get_handles()

        data = self._tpro.rest.put("tools", {
            "timeframe": timeframe,
            "market": symbol,
            "space_id": space_id,
            "time": timeframe_align(handles[0].get_time(), timeframe),
            "price": handles[0].get_price(),
            "type": tool.get_type(),
            "options": tool.data.get('options'),
            "handles": [{"price": item.get_price(), "time": timeframe_align(item.get_time(), timeframe)} for item in handles[1:]]
        })

        return data['id']

    def get_tools(
        self,
        from_unix: int,
        to_unix: int,
        timeframe: int,
        market: str,
        space_id: str
    ):
        """
        Return tools for the given parameters
        """
        data = self._tpro.rest.post("tools", {
            "to": to_unix,
            "from": from_unix,
            "timeframe": timeframe * 60,
            "market": market,
            "space_id": space_id
        })

        return {item['id']: get_tool_instance_by_type(item['type'], item) for item in data}
