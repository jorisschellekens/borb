#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener allows you to search for regular expressions in a PDF Document
"""
import io
import re
import typing
from decimal import Decimal
import functools

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import LeftToRightComparator
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class PDFMatch:
    """
    This class represents a match of a regular expression in a PDF.
    It has convenience methods to allow the user to extract information about the text that was matched,
    as well as the location (on the page) of the match.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        re_match: re.Match,
        glyph_bounding_boxes: typing.List["Rectangle"],
        font_color: Color,
        font_name: str,
        font_size: Decimal,
        page_nr: int,
    ):
        super(PDFMatch, self).__init__()
        assert page_nr >= 0
        self._page_nr: int = page_nr
        self._font_color: Color = font_color
        self._font_name: str = font_name
        self._font_size: Decimal = font_size
        self._glyph_bounding_boxes: typing.List["Rectangle"] = glyph_bounding_boxes
        self._re_match: re.Match = re_match
        # these fields are kept public to align with the existing python re.Match object
        self.pos = self._re_match.pos
        self.endpos = self._re_match.endpos
        self.lastindex = self._re_match.lastindex
        self.lastgroup = self._re_match.lastgroup
        self.string = self._re_match.string

    #
    # PRIVATE
    #

    def __getitem__(self, item):
        """
        This is identical to m.group(g). This allows easier access to an individual group from a match:
        """
        return self._re_match.__getitem__(item)

    #
    # PUBLIC
    #

    def end(self, __group: typing.Union[int, str] = 0) -> int:
        """
        Return the indices of the end of the substring matched by group;
        group defaults to zero (meaning the whole matched substring).
        Return -1 if group exists but did not contribute to the match.
        For a match object m, and a group g that did contribute to the match,
        the substring matched by group g (equivalent to m.group(g)) is m.string[m.start(g):m.end(g)]
        """
        return self._re_match.end(__group)

    def expand(self, template: typing.AnyStr) -> typing.AnyStr:
        """
        Returns one or more subgroups of the match. If there is a single argument, the result is a single string;
        if there are multiple arguments, the result is a tuple with one item per argument.
        Without arguments, group1 defaults to zero (the whole match is returned).
        If a groupN argument is zero, the corresponding return value is the entire matching string; if it is in the inclusive range [1..99],
        it is the string matching the corresponding parenthesized group.
        If a group number is negative or larger than the number of groups defined in the pattern,
        an IndexError exception is raised. If a group is contained in a part of the pattern that did not match,
        the corresponding result is None. If a group is contained in a part of the pattern that matched multiple times,
        the last match is returned.
        """
        return self._re_match.expand(template)

    def get_bounding_boxes(self) -> typing.List["Rectangle"]:
        """
        This function returns the bounding box(es) that constitute the locations of the glyph(s) that matched the regular expression.
        """
        out: typing.List[Rectangle] = []
        prev_group_of_rectangles: typing.List[Rectangle] = [
            self._glyph_bounding_boxes[0]
        ]
        for i in range(1, len(self._glyph_bounding_boxes)):
            bb: Rectangle = self._glyph_bounding_boxes[i]
            y_delta: Decimal = abs(bb.get_y() - prev_group_of_rectangles[-1].get_y())
            if y_delta > 12:
                max_x = max(
                    [(x.get_x() + x.get_width()) for x in prev_group_of_rectangles]
                )
                min_x = min([x.get_x() for x in prev_group_of_rectangles])
                max_y = max(
                    [(x.get_y() + x.get_height()) for x in prev_group_of_rectangles]
                )
                min_y = min([x.get_y() for x in prev_group_of_rectangles])
                out.append(Rectangle(min_x, min_y, max_x - min_x, max_y - min_y))
                prev_group_of_rectangles.clear()
                prev_group_of_rectangles.append(bb)
                continue
            else:
                prev_group_of_rectangles.append(bb)

        if len(prev_group_of_rectangles) > 0:
            max_x = max([(x.get_x() + x.get_width()) for x in prev_group_of_rectangles])
            min_x = min([x.get_x() for x in prev_group_of_rectangles])
            max_y = max(
                [(x.get_y() + x.get_height()) for x in prev_group_of_rectangles]
            )
            min_y = min([x.get_y() for x in prev_group_of_rectangles])
            out.append(Rectangle(min_x, min_y, max_x - min_x, max_y - min_y))
        return out

    def get_font_color(self) -> Color:
        """
        This function returns the Color in which the text was written that matched the regular expression
        :return:    the font_color in which the text was written
        """
        return self._font_color

    def get_font_name(self) -> str:
        """
        This function returns the name of the Font in which the text was written that matched the regular expression
        :return:    the font_name in which the text was written
        """
        return self._font_name

    def get_font_size(self) -> Decimal:
        """
        This function returns the font_size in which the text was written that matched the regular expression
        :return:    the font_size in which the text was written
        """
        return self._font_size

    def group(self, __group: typing.Union[str, int] = 0) -> typing.AnyStr:
        """
        Return the string obtained by doing backslash substitution on the template string template, as done by the sub() method.
        Escapes such as \n are converted to the appropriate characters, and numeric backreferences (\1, \2)
        and named backreferences (\g<1>, \g<name>) are replaced by the contents of the corresponding group.
        Changed in version 3.5: Unmatched groups are replaced with an empty string.
        """
        return self._re_match.group(__group)

    def groupdict(
        self, default: typing.AnyStr = None
    ) -> typing.Dict[str, typing.AnyStr]:
        """
        Return a dictionary containing all the named subgroups of the match, keyed by the subgroup name.
        The default argument is used for groups that did not participate in the match; it defaults to None.
        """
        return self._re_match.groupdict(default)  # type: ignore[arg-type]

    def groups(self, default: typing.AnyStr = None) -> typing.Sequence[typing.AnyStr]:
        """
        Return a tuple containing all the subgroups of the match, from 1 up to however many groups are in the pattern.
        The default argument is used for groups that did not participate in the match; it defaults to None.
        """
        return self._re_match.groups(default)  # type: ignore[arg-type]

    def span(self, __group: typing.Union[int, str] = 0) -> typing.Tuple[int, int]:
        """
        For a match m, return the 2-tuple (m.start(group), m.end(group)).
        Note that if group did not contribute to the match, this is (-1, -1). group defaults to zero, the entire match.
        """
        return self._re_match.span(__group)

    def start(self, __group: typing.Union[int, str] = 0) -> int:
        """
        Return the indices of the start of the substring matched by group;
        group defaults to zero (meaning the whole matched substring).
        Return -1 if group exists but did not contribute to the match.
        For a match object m, and a group g that did contribute to the match,
        the substring matched by group g (equivalent to m.group(g)) is m.string[m.start(g):m.end(g)]
        """
        return self._re_match.start(__group)


class RegularExpressionTextExtraction(EventListener):
    """
    This implementation of EventListener allows you to search for regular expressions in a PDF Document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, regular_expression):
        self._regular_expression = regular_expression
        self._text_render_info_events_per_page: typing.Dict[
            int, typing.List[ChunkOfTextRenderEvent]
        ] = {}
        self._matches_per_page: typing.Dict[int, typing.List[PDFMatch]] = {}
        self._text_per_page: typing.Dict[int, str] = {}
        self._current_page: int = -1

    #
    # PRIVATE
    #

    def _begin_page(self, page: Page):
        self._current_page += 1

    def _end_page(self, page: Page):
        # get ChunkOfTextRenderEvent objects on page
        tris: typing.List[ChunkOfTextRenderEvent] = (
            self._text_render_info_events_per_page[self._current_page]
            if self._current_page in self._text_render_info_events_per_page
            else []
        )

        # remove no-op
        tris = [x for x in tris if len(x.get_text().replace(" ", "")) != 0]

        # skip empty
        if len(tris) == 0:
            return

        # sort according to comparator
        tris = sorted(tris, key=functools.cmp_to_key(LeftToRightComparator.cmp))

        poss = []

        # iterate over the ChunkOfTextRenderEvent objects to get the text
        last_baseline_bottom = tris[0].get_baseline().y
        last_baseline_right = tris[0].get_baseline().x
        text = ""
        for t in tris:
            chunk_of_text_bounding_box: typing.Optional[
                Rectangle
            ] = t.get_previous_layout_box()
            assert chunk_of_text_bounding_box is not None

            # add newline if needed
            if abs(t.get_baseline().y - last_baseline_bottom) > 10 and len(text) > 0:
                if text.endswith(" "):
                    text = text[0:-1]
                text += "\n"
                text += t.get_text()
                last_baseline_right = (
                    chunk_of_text_bounding_box.get_x()
                    + chunk_of_text_bounding_box.get_width()
                )
                last_baseline_bottom = t.get_baseline().y
                poss.append(len(text))
                continue

            # check text
            if t.get_text().startswith(" ") or text.endswith(" "):
                text += t.get_text()
                last_baseline_right = (
                    chunk_of_text_bounding_box.get_x()
                    + chunk_of_text_bounding_box.get_width()
                )
                poss.append(len(text))
                continue

            # add space if needed
            delta = abs(last_baseline_right - chunk_of_text_bounding_box.get_x())
            space_width = round(t.get_space_character_width_estimate_in_user_space(), 1)
            text += " " if (space_width * Decimal(0.90) < delta) else ""

            # normal append
            text += t.get_text()
            last_baseline_right = (
                chunk_of_text_bounding_box.get_x()
                + chunk_of_text_bounding_box.get_width()
            )
            poss.append(len(text))
            continue

        # attempt to match
        for m in re.finditer(self._regular_expression, text):
            tri_start_index = len(
                [x for x in poss if x <= m.start()]
            )  # here we use '<=' because poss contains the number of characters we have seen at position x, with x included
            tri_stop_index = len([x for x in poss if x < m.end()])

            # set up list if we don't have information yet for this Page
            if self._current_page not in self._matches_per_page:
                self._matches_per_page[self._current_page] = []

            # extend collection
            self._matches_per_page[self._current_page].append(
                PDFMatch(
                    re_match=m,
                    glyph_bounding_boxes=[
                        y
                        for y in [
                            x.get_previous_layout_box()
                            for x in tris[tri_start_index : (tri_stop_index + 1)]
                        ]
                        if y is not None
                    ],
                    font_color=tris[tri_start_index].get_font_color(),
                    font_name=tris[tri_start_index].get_font().get_font_name() or "",
                    font_size=tris[tri_start_index].get_font_size(),
                    page_nr=self._current_page,
                )
            )

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            self._render_text(event)
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())

    def _render_text(self, text_render_info: ChunkOfTextRenderEvent):
        # init if needed
        if self._current_page not in self._text_render_info_events_per_page:
            self._text_render_info_events_per_page[self._current_page] = []

        # append TextRenderInfo
        for e in text_render_info.split_on_glyphs():
            self._text_render_info_events_per_page[self._current_page].append(e)

    #
    # PUBLIC
    #

    def get_matches(self) -> typing.Dict[int, typing.List[PDFMatch]]:
        """
        This function returns a typing.List[PDFMatch] matching the regular expression
        """
        return self._matches_per_page

    @staticmethod
    def get_matches_for_pdf(
        pattern: str, pdf: Document
    ) -> typing.Dict[int, typing.List[PDFMatch]]:
        """
        This function returns a typing.Dict[int, typing.List[PDFMatch]] matching the regular expression, on a given PDF
        :param pattern: the regular expression to match
        :param pdf:     the PDF on which to perform matching
        :return:        all matches (represented as typing.Dict[int, typing.List[PDFMatch]])
        """
        out: typing.Dict[int, typing.List[PDFMatch]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])

            # register EventListener
            cse: "RegularExpressionTextExtraction" = RegularExpressionTextExtraction(
                pattern
            )

            # process Page
            cse._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [cse])
            cse._event_occurred(EndPageEvent(page))

            # store output
            out[page_nr] = cse.get_matches().get(0, [])
        # return
        return out
