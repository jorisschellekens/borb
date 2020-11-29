from ptext.object.event_listener import Event


class EndPageEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has been processed.
    """

    def __init__(self, page: "Page"):
        self.page = page

    def get_page(self) -> "Page":
        return self.page
