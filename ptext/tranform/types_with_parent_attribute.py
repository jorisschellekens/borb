from decimal import Decimal


def add_base_methods(cls):
    """
    This decorator adds a variety of methods to an object to ensure
    it can be used by a BaseTransformer. These methods include:
    setting/getting a parent, getting the root in hierarchy,
    adding an EventListener,
    and notifying an object that an event has occurred.
    """

    def get_parent(self):
        """
        Get the parent object of this object
        """
        return getattr(self, "_parent")

    def set_parent(self, parent):
        """
        Set the parent object of this object
        """
        setattr(self, "_parent", parent)
        return self

    def get_root(self):
        """
        Get the root object of this object
        """
        tmp = getattr(self, "_parent")
        while (
            tmp is not None
            and hasattr(tmp, "_parent")
            and getattr(tmp, "_parent") is not None
        ):
            tmp = getattr(tmp, "_parent")
        return tmp

    def add_event_listener(self, event_listener):
        """
        Add an EventListener to this object
        """
        if not hasattr(self, "_event_listeners"):
            setattr(self, "_event_listeners", [])
        getattr(self, "_event_listeners").append(event_listener)
        return self

    def event_occurred(self, event):
        """
        Notify the EventListeners registered
        to this object that an Event has occurred
        """
        if not hasattr(self, "_event_listeners"):
            setattr(self, "_event_listeners", [])
        for l in getattr(self, "_event_listeners"):
            l.event_occurred(event)
        return self

    def to_json_serializable(self, to_convert=None):
        """
        Convert this object to a representation that
        can be serialized as JSON
        """
        if isinstance(to_convert, dict):
            return {
                self.to_json_serializable(k): self.to_json_serializable(v)
                for k, v in to_convert.items()
            }
        if isinstance(to_convert, list):
            return [self.to_json_serializable(x) for x in to_convert]
        if isinstance(to_convert, Decimal):
            return float(to_convert)
        if isinstance(to_convert, hexstr) or isinstance(to_convert, str):
            return to_convert
        return None

    # linkage methods
    setattr(cls, "get_parent", get_parent)
    setattr(cls, "set_parent", set_parent)
    setattr(cls, "get_root", get_root)
    # event listener methods
    setattr(cls, "add_event_listener", add_event_listener)
    setattr(cls, "event_occurred", event_occurred)
    # serialization methods
    setattr(cls, "to_json_serializable", to_json_serializable)
    # initialize fields
    setattr(cls, "_parent", None)
    setattr(cls, "_event_listeners", [])
    return cls


@add_base_methods
class DecimalWithParentAttribute(Decimal):
    pass


@add_base_methods
class StringWithParentAttribute(str):
    pass


class hexstr(str):
    def __new__(cls, value):
        if len(value) % 2 == 1:
            return str.__new__(cls, value + "0")
        else:
            return str.__new__(cls, value)


@add_base_methods
class HexStringWithParentAttribute(hexstr):
    pass


@add_base_methods
class ListWithParentAttribute(list):
    pass


@add_base_methods
class DictionaryWithParentAttribute(dict):
    pass
