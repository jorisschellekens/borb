import io
from typing import Union, List, Any

from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject, PDFIndirectObject


class Event:
    pass


class EventListener:
    def event_occurred(self, event: Event) -> None:
        pass


class PDFHighLevelObject(PDFObject):
    """
    This object represents a single value/property in a PDF document.
    Objects of this type can be nested (by applying set_property) and
    can be used to mimic both dictionaries and arrays.
    """

    def __init__(self):
        self.properties = {}
        self.parent = None
        self.listeners = []

    def add_event_listener(self, listener: EventListener) -> "PDFHighLevelObject":
        """
        Add an EventListener to this PDFHighLevelObject
        :param listener:    the EventListener to add
        :type listener:     EventListener
        """
        self.listeners.append(listener)
        return self

    def event_occurred(self, event: Event) -> "PDFHighLevelObject":
        """
        Notify all EventListener(s) that the Event has occurred.
        Then notifies the EventListener(s) of the parent PDFHighLevelObject
        :param event:   the Event that occurred
        :type event:    Event
        """
        for l in self.listeners:
            l.event_occurred(event)
        # propagate event up
        if self.parent is not None:
            self.parent.event_occurred(event)
        # return
        return self

    def get_parent(self) -> "PDFHighLevelObject":
        """
        Get the parent PDFHighLevelObject of this PDFHighLevelObject
        """
        return self.parent

    def get_root(self) -> "PDFHighLevelObject":
        """
        Get the root of this PDFHighLevelObject tree
        """
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    def set(self, key: Union[str, int], value: PDFObject) -> "PDFHighLevelObject":
        """
        Add a key/value pair to this PDFHighLevelObject
        :param key:     the key to be used
        :type key:      Union[str, int]
        :param value:   the value to be used
        :type value:    PDFObject
        """
        self.properties[key] = value
        if isinstance(value, PDFHighLevelObject):
            value.parent = self
        return self

    def pop(self, key: Union[str, int, List[Union[str, int]]]) -> "PDFHighLevelObject":
        """
        Pop a key/value pair to this PDFHighLevelObject
        :param key:     the key of the key/value pair
        :type key:      Union[str, int]
        """
        if isinstance(key, str) or isinstance(key, int):
            if key in self.properties:
                self.properties.pop(key)
        if isinstance(key, List):
            if len(key) == 1:
                self.pop(key[0])
                return self
            if key[0] in self.properties and isinstance(
                self.properties[key[0]], PDFHighLevelObject
            ):
                self.properties[key[0]].pop(key[1:])
        return self

    def get(self, key: Union[str, int, List[Union[str, int]]]) -> Union[PDFObject]:
        """
        Get a key/value pair from this PDFHighLevelObject.
        If a List is passed the first property will be matched and the subsequent
        value(s) in the List will be used to get a key/value pair from that first value.
        :param key:     the key to be used
        :type key:      Union[str, int, List[Union[str, int]]]
        """
        if isinstance(key, str) or isinstance(key, int):
            return self.properties[key] if key in self.properties else PDFNull()
        if isinstance(key, List):
            obj = self
            for k in key:
                if isinstance(obj, PDFHighLevelObject) and obj.has_key(k):
                    obj = obj.get(k)
                else:
                    return PDFNull()
            return obj

    def has_key(self, key: Union[str, int]) -> bool:
        """
        Return True if this PDFHighLevelObject has a given key
        :param key: the key
        :type key:  Union[str, int]
        """
        return key in self.properties

    def has_value(self, value: Any) -> bool:
        """
        Return True if this PDFHighLevelObject has a given value
        :param value: the value
        :type value:  Any
        """
        return value in [v for k, v in self.properties.items()]

    def as_dict(self):
        out = {}
        for k, v in self.properties.items():
            if k in ["DecodedBytes", "RawBytes"]:
                continue
            if isinstance(v, PDFHighLevelObject):
                out[k] = v.as_dict()
            else:
                out[k] = str(v)
        return out

    def __len__(self):
        return len(self.properties)
