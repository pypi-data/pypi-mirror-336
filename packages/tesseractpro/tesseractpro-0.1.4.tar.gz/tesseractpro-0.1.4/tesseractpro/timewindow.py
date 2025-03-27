
class TimeWindow:
    def __init__(self, timeframe: int, start_time: int, candles: int):
        self.timeframe = timeframe
        self.time = start_time
        self.candles = candles

    def get_start_time(self) -> int:
        return self.time

    def get_end_time(self) -> int:
        return self.time - (self.candles * self.timeframe * 60)
