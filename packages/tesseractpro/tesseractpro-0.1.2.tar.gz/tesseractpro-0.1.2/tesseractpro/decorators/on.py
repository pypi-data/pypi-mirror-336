from typing import Callable


def on(
    event_name,
    namespace="/api"
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Decorator to mark a method as a Socket.IO event handler.
    """
    def decorator(func):
        setattr(func, "_socketio_event", (event_name, namespace))
        return func
    return decorator
