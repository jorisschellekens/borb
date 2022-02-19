#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A sound annotation (PDF 1.2) shall analogous to a text annotation except that instead of a text note, it contains
sound recorded from the computer’s microphone or imported from a file. When the annotation is activated, the
sound shall be played. The annotation shall behave like a text annotation in most ways, with a different icon (by
default, a speaker) to indicate that it represents a sound. Table 185 shows the annotation dictionary entries
specific to this type of annotation. Sound objects are discussed in 13.3, “Sounds.”
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class SoundAnnotation(Annotation):
    """
    A sound annotation (PDF 1.2) shall analogous to a text annotation except that instead of a text note, it contains
    sound recorded from the computer’s microphone or imported from a file. When the annotation is activated, the
    sound shall be played. The annotation shall behave like a text annotation in most ways, with a different icon (by
    default, a speaker) to indicate that it represents a sound. Table 185 shows the annotation dictionary entries
    specific to this type of annotation. Sound objects are discussed in 13.3, “Sounds.”
    """

    def __init__(self):
        super(SoundAnnotation, self).__init__()
        # TODO
