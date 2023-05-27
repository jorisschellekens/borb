#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for determining which characters (typing.Set[str])
are used by which Font. This is particularly useful when performing Font subsetting.
"""
import typing

from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.font.font import Font


class CharacterSetListener(EventListener):
    """
    This implementation of WriteBaseTransformer is responsible for determining which characters (typing.Set[str])
    are used by which Font. This is particularly useful when performing Font subsetting.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(CharacterSetListener, self).__init__()
        self._character_set_per_font: typing.Dict[Font, typing.Set[str]] = {}

    #
    # PRIVATE
    #

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            f: Font = event.get_font()
            if f in self._character_set_per_font:
                s: typing.Set[str] = self._character_set_per_font[f]
                for c in event.get_text():
                    s.add(c)
                self._character_set_per_font[f] = s
            else:
                self._character_set_per_font[f] = set([x for x in event.get_text()])

    #
    # PUBLIC
    #

    def get_character_set_per_font(self) -> typing.Dict[Font, typing.Set[str]]:
        """
        This function returns the character set (typing.Set[str]) used by each Font
        :return:    the character set used by each Font
        """
        return self._character_set_per_font
