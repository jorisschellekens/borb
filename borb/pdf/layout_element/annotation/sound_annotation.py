#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a sound annotation that embeds an audio file in the PDF document.

Sound annotations (PDF 1.3) associate an audio file with a specific point on the page. When activated,
they allow the user to play the embedded audio content. The annotation can be triggered either by
clicking the annotation icon or through other user interactions. The annotation's location and
appearance on the page are determined by the Rect entry in the annotation dictionary.

The audio is stored as a stream in a format suitable for embedding, such as raw PCM or other supported
audio formats. The annotation's appearance can be customized, and the audio content can be played using
PDF viewers that support this feature.
"""
import pathlib
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name, stream


class SoundAnnotation(Annotation):
    """
    Represents a sound annotation that embeds an audio file in the PDF document.

    Sound annotations (PDF 1.3) associate an audio file with a specific point on the page. When activated,
    they allow the user to play the embedded audio content. The annotation can be triggered either by
    clicking the annotation icon or through other user interactions. The annotation's location and
    appearance on the page are determined by the Rect entry in the annotation dictionary.

    The audio is stored as a stream in a format suitable for embedding, such as raw PCM or other supported
    audio formats. The annotation's appearance can be customized, and the audio content can be played using
    PDF viewers that support this feature.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        path_to_audio_file: pathlib.Path,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        contents: typing.Optional[str] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 100),
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a sound annotation that embeds an audio file and links to a destination.

        This constructor sets up a sound annotation, allowing users to attach an audio file to a specific
        location in the document. The sound can be triggered by user interaction with the annotation, such
        as clicking the annotation icon. The annotation’s appearance, including dimensions and visual properties
        (e.g., background and border colors), can be customized.

        The embedded audio is stored in a suitable format for PDF, such as raw PCM or other compatible audio types.

        :param path_to_audio_file:      the pathlib.Path pointing to the audio file
        :param background_color:        Optional background color for the annotation.
        :param border_color:            Optional border color for the annotation.
        :param border_dash_pattern:     Dash pattern used for the annotation's border lines.
        :param border_dash_phase:       Phase offset for the dash pattern in the borders.
        :param border_width_bottom:     Width of the bottom border of the annotation.
        :param border_width_left:       Width of the left border of the annotation.
        :param border_width_right:      Width of the right border of the annotation.
        :param border_width_top:        Width of the top border of the annotation.
        :param horizontal_alignment:     Horizontal alignment of the annotation (default is LEFT).
        :param margin_bottom:           Space between the annotation and the element below it.
        :param margin_left:             Space between the annotation and the left page margin.
        :param margin_right:            Space between the annotation and the right page margin.
        :param margin_top:              Space between the annotation and the element above it.
        :param padding_bottom:          Padding inside the annotation at the bottom.
        :param padding_left:            Padding inside the annotation on the left side.
        :param padding_right:           Padding inside the annotation on the right side.
        :param padding_top:             Padding inside the annotation at the top.
        :param vertical_alignment:       Vertical alignment of the annotation (default is TOP).
        """
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            contents=contents,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size,
            vertical_alignment=vertical_alignment,
        )
        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        self[name("Subtype")] = name("Sound")

        # (Required) A sound object defining the sound that shall be played when
        # the annotation is activated (see 13.3, “Sounds”).
        self[name("Sound")] = stream(
            {
                name("B"): 8,
                name("Bytes"): self.__convert_audio_to_raw(path_to_audio_file),
                name("C"): 1,
                name("E"): name("Raw"),
                name("Filter"): None,
                name("R"): 44100,
                name("Type"): name("Sound"),
            }
        )

        # (Optional) The name of an icon that shall be used in displaying the
        # annotation. Conforming readers shall provide predefined icon
        # appearances for at least the standard names Speaker and Mic. Additional
        # names may be supported as well. Default value: Speaker.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[name("Name")] = name("Speaker")  # Annotation icon

    #
    # PRIVATE
    #

    @staticmethod
    def __convert_audio_to_raw(path_to_audio_file: pathlib.Path) -> bytes:
        """Convert an audio file to 8-bit unsigned PCM, mono, 44.1kHz, suitable for embedding as a PDF /Sound stream."""
        try:
            import ffmpeg  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'ffmpeg' library to use the SoundAnnotation class. "
                "You can install it with 'pip install ffmpeg-python'."
            )
        process = (
            ffmpeg.input(str(path_to_audio_file))
            .output("pipe:", format="u8", acodec="pcm_u8", ac=1, ar="44100")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return process[0]

    #
    # PUBLIC
    #
