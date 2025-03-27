class EventEmitter:
    def __init__(self):
        self._events = {}

    def on(self, event_name, callback) -> None:
        """
        Register a callback for a specific event.
        """
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def emit(self, event_name, *args, **kwargs) -> None:
        """
        Invoke all callbacks associated with an event.
        """
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback(*args, **kwargs)
