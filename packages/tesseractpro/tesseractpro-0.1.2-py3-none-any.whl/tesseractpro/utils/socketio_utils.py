
def register_socketio_events(instance, socket) -> None:
    """
    Register all @on event handlers for a class instance
    with a Socket.IO client.
    """
    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)
        if callable(attr) and hasattr(attr, "_socketio_event"):
            event_name, namespace = getattr(attr, "_socketio_event")
            socket.on(event_name, attr, namespace=namespace)
