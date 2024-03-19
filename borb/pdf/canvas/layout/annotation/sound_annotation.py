#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A sound annotation (PDF 1.2) shall analogous to a text annotation except that instead of a text note, it contains
sound recorded from the computer’s microphone or imported from a file. When the annotation is activated, the
sound shall be played. The annotation shall behave like a text annotation in most ways, with a different icon (by
default, a speaker) to indicate that it represents a sound. Table 185 shows the annotation dictionary entries
specific to this type of annotation. Sound objects are discussed in 13.3, “Sounds.”
"""
import pathlib

from borb.io.read.types import Boolean
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class SoundAnnotation(Annotation):
    """
    A sound annotation (PDF 1.2) shall analogous to a text annotation except that instead of a text note, it contains
    sound recorded from the computer’s microphone or imported from a file. When the annotation is activated, the
    sound shall be played. The annotation shall behave like a text annotation in most ways, with a different icon (by
    default, a speaker) to indicate that it represents a sound. Table 185 shows the annotation dictionary entries
    specific to this type of annotation. Sound objects are discussed in 13.3, “Sounds.”
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        url_to_mp3_file: str,
    ):
        super(SoundAnnotation, self).__init__(bounding_box=bounding_box)
        self._url_to_mp3_file: str = url_to_mp3_file

        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        self[Name("Subtype")] = Name("Screen")

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        self[Name("A")] = Dictionary()
        self["A"][Name("Type")] = Name("Action")
        self["A"][Name("S")] = Name("Rendition")
        self["A"][Name("OP")] = bDecimal(0)

        # A/R
        self["A"][Name("R")] = Dictionary()
        self[Name("A")][Name("R")][Name("Type")] = Name("Rendition")
        self[Name("A")][Name("R")][Name("S")] = Name("MR")

        # A/R/C
        self[Name("A")][Name("R")][Name("C")] = Dictionary()
        self[Name("A")][Name("R")][Name("C")][Name("Type")] = Name("MediaClip")
        self[Name("A")][Name("R")][Name("C")][Name("S")] = Name("MCD")
        self[Name("A")][Name("R")][Name("C")][Name("CT")] = String("video/mp4")

        # A/R/C/D
        # fmt: off
        self[Name("A")][Name("R")][Name("C")][Name("D")] = Dictionary()
        self[Name("A")][Name("R")][Name("C")][Name("D")][Name("Type")] = Name("Filespec")
        self[Name("A")][Name("R")][Name("C")][Name("D")][Name("FS")] = Name("URL")
        self[Name("A")][Name("R")][Name("C")][Name("D")][Name("F")] = String(SoundAnnotation._make_canonical_file_path(self._url_to_mp3_file))
        # fmt: on

        # A/R/C/P
        # fmt: off
        self[Name("A")][Name("R")][Name("C")][Name("P")] = Dictionary()
        self[Name("A")][Name("R")][Name("C")][Name("P")][Name("TF")] = String("TEMPACCESS")
        # fmt: on

        # A/R
        self[Name("A")][Name("R")][Name("P")] = Dictionary()
        self[Name("A")][Name("R")][Name("P")][Name("BE")] = Dictionary()
        self[Name("A")][Name("R")][Name("P")][Name("BE")][Name("C")] = Boolean(True)

    #
    # PRIVATE
    #

    @staticmethod
    def _make_canonical_file_path(p: str) -> str:
        try:
            return pathlib.Path(p).as_uri()
        except:
            return p

    #
    # PUBLIC
    #
