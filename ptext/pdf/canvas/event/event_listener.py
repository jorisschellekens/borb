class Event:
    pass


class EventListener:
    """
    This class represents a generic event listener
    This listener is notified whenever the canvas processes an event/command.
    """

    def event_occurred(self, event: Event) -> None:
        pass
