#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A generic class for processing and altering PDF page content streams.

The `Source` serves as a base class for various operations
that modify or process the content of a PDF page's content stream. It is a more
general-purpose class than filters, and is designed to support a wide range of use
cases, such as Optical Character Recognition (OCR), rendering PDF pages to images,
extracting images or text, and other content manipulations.

The class can be extended to implement specific processing behaviors, enabling the
ability to perform complex transformations on the page's content.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name, stream, hexstr
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.visitor.read.compression.decode_stream import decode_stream

PointType: typing.TypeAlias = typing.Tuple[float, float]  # x, y
LineType: typing.TypeAlias = typing.Tuple[PointType, PointType]  # from_point, to_point
ShapeType: typing.TypeAlias = typing.List[LineType]  # lines making up the shape
GlyphType: typing.TypeAlias = typing.Tuple[bytes, str, float]  # bytes, text, width


class Source(Pipe):
    """
    A generic class for processing and altering PDF page content streams.

    The `Source` serves as a base class for various operations
    that modify or process the content of a PDF page's content stream. It is a more
    general-purpose class than filters, and is designed to support a wide range of use
    cases, such as Optical Character Recognition (OCR), rendering PDF pages to images,
    extracting images or text, and other content manipulations.

    The class can be extended to implement specific processing behaviors, enabling the
    ability to perform complex transformations on the page's content.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a `Source` instance.

        The constructor takes a `Page` object that represents the PDF page whose content
        stream will be processed. This forms the basis for any content manipulation or
        transformation operations that will be applied to the page.

        :param p:  The `Page` object that represents the PDF page to be processed.
                   It contains the page content that will be the target of the processing.

        The `Source` class can be extended to implement specific
        processing behaviors, and the page passed to the constructor will be the subject
        of those transformations or manipulations.
        """
        super().__init__()
        from borb.pdf.toolkit.source.operator.operator import Operator
        from borb.pdf.toolkit.source.operator.operator_BDC import OperatorBDC
        from borb.pdf.toolkit.source.operator.operator_BI import OperatorBI
        from borb.pdf.toolkit.source.operator.operator_B import OperatorB
        from borb.pdf.toolkit.source.operator.operator_b import Operatorb
        from borb.pdf.toolkit.source.operator.operator_BMC import OperatorBMC
        from borb.pdf.toolkit.source.operator.operator_BT import OperatorBT
        from borb.pdf.toolkit.source.operator.operator_BX import OperatorBX
        from borb.pdf.toolkit.source.operator.operator_B_star import OperatorBStar
        from borb.pdf.toolkit.source.operator.operator_b_star import OperatorbStar
        from borb.pdf.toolkit.source.operator.operator_c import Operatorc
        from borb.pdf.toolkit.source.operator.operator_cm import Operatorcm
        from borb.pdf.toolkit.source.operator.operator_CS import OperatorCS
        from borb.pdf.toolkit.source.operator.operator_cs import Operatorcs
        from borb.pdf.toolkit.source.operator.operator_d0 import Operatord0
        from borb.pdf.toolkit.source.operator.operator_d1 import Operatord1
        from borb.pdf.toolkit.source.operator.operator_d import Operatord
        from borb.pdf.toolkit.source.operator.operator_Do import OperatorDo
        from borb.pdf.toolkit.source.operator.operator_DP import OperatorDP
        from borb.pdf.toolkit.source.operator.operator_EI import OperatorEI
        from borb.pdf.toolkit.source.operator.operator_EMC import OperatorEMC
        from borb.pdf.toolkit.source.operator.operator_ET import OperatorET
        from borb.pdf.toolkit.source.operator.operator_EX import OperatorEX
        from borb.pdf.toolkit.source.operator.operator_f import Operatorf
        from borb.pdf.toolkit.source.operator.operator_F import OperatorF
        from borb.pdf.toolkit.source.operator.operator_f_star import OperatorfStar
        from borb.pdf.toolkit.source.operator.operator_G import OperatorG
        from borb.pdf.toolkit.source.operator.operator_g import Operatorg
        from borb.pdf.toolkit.source.operator.operator_gs import Operatorgs
        from borb.pdf.toolkit.source.operator.operator_h import Operatorh
        from borb.pdf.toolkit.source.operator.operator_ID import OperatorID
        from borb.pdf.toolkit.source.operator.operator_i import Operatori
        from borb.pdf.toolkit.source.operator.operator_J import OperatorJ
        from borb.pdf.toolkit.source.operator.operator_j import Operatorj
        from borb.pdf.toolkit.source.operator.operator_K import OperatorK
        from borb.pdf.toolkit.source.operator.operator_k import Operatork
        from borb.pdf.toolkit.source.operator.operator_l import Operatorl
        from borb.pdf.toolkit.source.operator.operator_m import Operatorm
        from borb.pdf.toolkit.source.operator.operator_M import OperatorM
        from borb.pdf.toolkit.source.operator.operator_MP import OperatorMP
        from borb.pdf.toolkit.source.operator.operator_n import Operatorn
        from borb.pdf.toolkit.source.operator.operator_Q import OperatorQ
        from borb.pdf.toolkit.source.operator.operator_q import Operatorq
        from borb.pdf.toolkit.source.operator.operator_re import Operatorre
        from borb.pdf.toolkit.source.operator.operator_rg import Operatorrg
        from borb.pdf.toolkit.source.operator.operator_RG import OperatorRG
        from borb.pdf.toolkit.source.operator.operator_ri import Operatorri
        from borb.pdf.toolkit.source.operator.operator_SC import OperatorSC
        from borb.pdf.toolkit.source.operator.operator_sc import Operatorsc
        from borb.pdf.toolkit.source.operator.operator_SCN import OperatorSCN
        from borb.pdf.toolkit.source.operator.operator_scn import Operatorscn
        from borb.pdf.toolkit.source.operator.operator_sh import Operatorsh
        from borb.pdf.toolkit.source.operator.operator_S import OperatorS
        from borb.pdf.toolkit.source.operator.operator_Tc import OperatorTc
        from borb.pdf.toolkit.source.operator.operator_Td import OperatorTd
        from borb.pdf.toolkit.source.operator.operator_TD import OperatorTD
        from borb.pdf.toolkit.source.operator.operator_Tf import OperatorTf
        from borb.pdf.toolkit.source.operator.operator_TJ import OperatorTJ
        from borb.pdf.toolkit.source.operator.operator_Tj import OperatorTj
        from borb.pdf.toolkit.source.operator.operator_TL import OperatorTL
        from borb.pdf.toolkit.source.operator.operator_Tm import OperatorTm
        from borb.pdf.toolkit.source.operator.operator_Tr import OperatorTr
        from borb.pdf.toolkit.source.operator.operator_Ts import OperatorTs
        from borb.pdf.toolkit.source.operator.operator_Tw import OperatorTw
        from borb.pdf.toolkit.source.operator.operator_Tz import OperatorTz
        from borb.pdf.toolkit.source.operator.operator_T_star import OperatorTStar
        from borb.pdf.toolkit.source.operator.operator_v import Operatorv
        from borb.pdf.toolkit.source.operator.operator_w import Operatorw
        from borb.pdf.toolkit.source.operator.operator_W import OperatorW
        from borb.pdf.toolkit.source.operator.operator_W_star import OperatorWStar
        from borb.pdf.toolkit.source.operator.operator_y import Operatory
        from borb.pdf.toolkit.source.operator.operator_double_quote import (
            OperatorDoubleQuote,
        )
        from borb.pdf.toolkit.source.operator.operator_single_quote import (
            OperatorSingleQuote,
        )

        self.operators: typing.List[Operator] = [  # type: ignore[annotation-unchecked]
            OperatorB(),
            Operatorb(),
            OperatorBStar(),
            OperatorbStar(),
            OperatorBDC(),
            OperatorBI(),
            OperatorBMC(),
            OperatorBT(),
            OperatorBX(),
            Operatorc(),
            Operatorcm(),
            OperatorCS(),
            Operatorcs(),
            Operatord(),
            Operatord0(),
            Operatord1(),
            OperatorDo(),
            OperatorDP(),
            OperatorEI(),
            OperatorEMC(),
            OperatorET(),
            OperatorEX(),
            OperatorF(),
            Operatorf(),
            OperatorfStar(),
            OperatorG(),
            Operatorg(),
            Operatorgs(),
            Operatorh(),
            Operatori(),
            OperatorID(),
            OperatorJ(),
            Operatorj(),
            OperatorK(),
            Operatork(),
            Operatorl(),
            OperatorM(),
            Operatorm(),
            OperatorMP(),
            Operatorn(),
            OperatorQ(),
            Operatorq(),
            Operatorre(),
            OperatorRG(),
            Operatorrg(),
            Operatorri(),
            OperatorS(),
            OperatorSC(),
            Operatorsc(),
            OperatorSCN(),
            Operatorscn(),
            Operatorsh(),
            OperatorTStar(),
            OperatorTc(),
            OperatorTD(),
            OperatorTd(),
            OperatorTf(),
            OperatorTJ(),
            OperatorTj(),
            OperatorTL(),
            OperatorTm(),
            OperatorTr(),
            OperatorTs(),
            OperatorTw(),
            OperatorTz(),
            Operatorv(),
            OperatorW(),
            Operatorw(),
            OperatorWStar(),
            Operatory(),
            OperatorSingleQuote(),
            OperatorDoubleQuote(),
        ]
        self.color_rendering_intent: name = name("DeviceRGB")  # type: ignore[annotation-unchecked]
        self.dash_array: typing.List[int] = []  # type: ignore[annotation-unchecked]
        self.dash_phase: int = 0  # type: ignore[annotation-unchecked]
        self.font_size: float = 0  # type: ignore[annotation-unchecked]
        self.line_width: float = 0  # type: ignore[annotation-unchecked]
        self.horizontal_scaling: float = 100  # type: ignore[annotation-unchecked]
        self.word_spacing: float = 0  # type: ignore[annotation-unchecked]
        self.character_spacing: float = 0  # type: ignore[annotation-unchecked]
        self.flatness_tolerance: float = 0  # type: ignore[annotation-unchecked]
        self.graphics_state_stack: typing.List[dict] = []  # type: ignore[annotation-unchecked]
        self.is_in_compatibility_section: bool = False  # type: ignore[annotation-unchecked]
        self.leading: float = 0  # type: ignore[annotation-unchecked]
        self.line_cap_style: int = 0  # type: ignore[annotation-unchecked]
        self.line_join_style: int = 0  # type: ignore[annotation-unchecked]
        self.miter_limit: float = 0  # type: ignore[annotation-unchecked]
        self.non_stroke_color: Color = X11Color.BLACK  # type: ignore[annotation-unchecked]
        self.non_stroke_color_space: name = name("DeviceRGB")  # type: ignore[annotation-unchecked]
        self.path: typing.List[ShapeType] = []  # type: ignore[annotation-unchecked]
        self.stroke_color: Color = X11Color.BLACK  # type: ignore[annotation-unchecked]
        self.stroke_color_space: name = name("DeviceRGB")  # type: ignore[annotation-unchecked]
        self.font: Font = Standard14Fonts.get("Helvetica")  # type: ignore[annotation-unchecked]
        self.text_line_matrix: typing.List[typing.List[float]] = [  # type: ignore[annotation-unchecked]
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.text_matrix: typing.List[typing.List[float]] = [  # type: ignore[annotation-unchecked]
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.text_rendering_mode: int = 0  # type: ignore[annotation-unchecked]
        self.text_rise: float = 0  # type: ignore[annotation-unchecked]
        self.transformation_matrix: typing.List[typing.List[float]] = [  # type: ignore[annotation-unchecked]
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.__page: typing.Optional[Page] = None  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def fill(
        self,
        fill_color: Color,
        shape: ShapeType,
        use_even_odd_rule: bool,
    ):
        """
        Initiate the process of pushing a filling event down the pipe.

        This method starts the flow of a filling-related event down the pipeline by creating
        and passing a filling event. The event is triggered by the invocation of this method,
        which processes the given parameters to define the characteristics of the fill operation
        to be applied to the current path or shape.

        :param fill_color:       The color to be used for filling the shape or path. This determines the interior color of the defined region.
        :param shape:            The shape type of the fill operation. This defines the structure or outline of the area to be filled.
        :param use_even_odd_rule: A boolean value indicating whether to use the even-odd rule for determining the fill region.
                                  If True, the even-odd rule is used; otherwise, the nonzero winding number rule is applied.
        :return: None
        """
        next: typing.Optional[Pipe] = self.get_next()
        if next is None:
            return
        from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent

        assert self.__page is not None
        next.process(
            ShapeFillEvent(
                fill_color=fill_color,
                shape=shape,
                use_even_odd_rule=use_even_odd_rule,
                page=self.__page,
            )
        )

    def image(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        image: PDFType,
        xobject_resource: name,
    ) -> None:
        """
        Initiate the process of pushing an image event down the pipe.

        This method starts the flow of an image-related event down the pipeline by creating
        and passing an image event. The event is triggered by the invocation of this method,
        which processes the given parameters to define the characteristics of the image to
        be rendered on a page.

        :param x:                   The x-coordinate in user space where the image will be placed. This specifies the horizontal starting point of the image.
        :param y:                   The y-coordinate in user space where the image will be placed. This specifies the vertical starting point of the image.
        :param width:               The width of the image to be rendered. This controls the scaling of the image along the horizontal axis.
        :param height:              The height of the image to be rendered. This controls the scaling of the image along the vertical axis.
        :param image:               The image data in the form of a `PDFType`. This contains the image content to be displayed on the page.
        :param xobject_resource:    The name of the XObject resource associated with the image. This resource links the image content to the document.
        :return: None
        """
        next: typing.Optional[Pipe] = self.get_next()
        if next is None:
            return
        from borb.pdf.toolkit.source.event.image_event import ImageEvent

        assert self.__page is not None
        next.process(
            ImageEvent(
                x=x,
                y=y,
                width=width,
                height=height,
                image=image,
                xobject_resource=xobject_resource,
                page=self.__page,
            )
        )

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        next: typing.Optional[Pipe] = self.get_next()
        if next is not None:
            next.process(event)

    def process_page(self, page: Page) -> None:
        """
        Process the content stream of a PDF page, executing operations based on the PDF operators encountered.

        This method serves as the main entry point for processing a PDF page's content stream.
        It iterates over the stream's operators and operands, invoking corresponding methods for
        each operator. Subclasses can override these operator-specific methods to implement custom
        behavior for specific operations (e.g., rendering, text extraction, or modification).

        The `process_content_stream` method provides a flexible framework for handling content
        streams, enabling extensions to define custom processing logic while leveraging this base
        implementation.

        :param page: The Page
        """
        # fmt: off
        from borb.pdf.toolkit.source.operator.operator import Operator
        self.operators = sorted(self.operators, key=lambda x: x.get_name())
        self.operators = sorted(self.operators, key=lambda x: len(x.get_name()), reverse=True)
        # fmt: on

        # set __page
        self.__page = page

        # decompress /Contents /Bytes

        content_stream_bytes: bytes = b""
        if isinstance(page["Contents"], list):
            content_stream_bytes = b"".join(
                [decode_stream(cs).get("DecodedBytes", b"") for cs in page["Contents"]]
            )
        if isinstance(page["Contents"], stream):
            content_stream_bytes = decode_stream(page["Contents"]).get(
                "DecodedBytes", b""
            )

        operands: typing.List[
            typing.Union[PDFType, typing.Literal[b"<<"], typing.Literal[b"["]]
        ] = []
        i: int = 0
        while i < len(content_stream_bytes):

            # float
            if content_stream_bytes[i] in b"0123456789.-":
                j: int = i
                has_leading_digits: bool = False
                has_trailing_digits: bool = False
                has_dot: bool = False
                if content_stream_bytes[j] in b"-":
                    j += 1
                while content_stream_bytes[j] in b"0123456789":
                    has_leading_digits = True
                    j += 1
                if content_stream_bytes[j] in b".":
                    has_dot = True
                    j += 1
                while content_stream_bytes[j] in b"0123456789":
                    has_trailing_digits = True
                    j += 1
                if has_dot and (has_leading_digits or has_trailing_digits):
                    operands += [float(content_stream_bytes[i:j].decode())]
                    i = j
                    continue

            # integer
            if content_stream_bytes[i] in b"0123456789-":
                j = i
                if content_stream_bytes[j] in b"-":
                    j += 1
                while content_stream_bytes[j] in b"0123456789":
                    j += 1
                operands += [int(content_stream_bytes[i:j].decode())]
                i = j
                continue

            # name
            if content_stream_bytes[i] in b"/":
                j = i + 1
                while (
                    (content_stream_bytes[j : j + 1] != b" ")
                    and (content_stream_bytes[j : j + 2] != b"\n\r")
                    and (content_stream_bytes[j : j + 2] != b"\r\n")
                    and (content_stream_bytes[j : j + 1] != b"\n")
                    and (content_stream_bytes[j : j + 1] != b"\r")
                    and (content_stream_bytes[j : j + 1] != b"[")
                    and (content_stream_bytes[j : j + 1] != b"]")
                    and (content_stream_bytes[j : j + 1] != b"<")
                    and (content_stream_bytes[j : j + 1] != b">")
                    and (content_stream_bytes[j : j + 1] != b"/")
                ):
                    j += 1
                operands += [name(content_stream_bytes[i:j].decode())]
                i = j
                continue

            # string
            if content_stream_bytes[i] in b"(":
                j = i
                while content_stream_bytes[j : j + 1] != b")":
                    if content_stream_bytes[j:].startswith(b"\\n"):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\r"):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\t"):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\b"):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\f"):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\("):
                        j += 2
                        continue
                    if content_stream_bytes[j:].startswith(b"\\)"):
                        j += 2
                        continue
                    j += 1
                j += 1
                operands += [content_stream_bytes[i + 1 : j - 1].decode("latin1")]
                i = j
                continue

            # hex string
            if (content_stream_bytes[i:].startswith(b"<")) and (
                not content_stream_bytes[i:].startswith(b"<<")
            ):
                j = i + 1
                while content_stream_bytes[j] in b"0123456789ABCDEFabcdef":
                    j += 1

                j += 1
                operands += [hexstr(content_stream_bytes[i + 1 : j - 1].decode())]
                i = j
                continue

            # open array [
            if content_stream_bytes[i] in b"[":
                operands += [b"["]
                i += 1
                continue
            # close array ]
            if content_stream_bytes[i] in b"]":
                array_open_bracket_pos: int = operands.index(b"[")
                arr = operands[array_open_bracket_pos + 1 :]
                operands = operands[:array_open_bracket_pos] + [arr]  # type: ignore[assignment]
                i += 1
                continue

            # open dictionary
            if content_stream_bytes[i:].startswith(b"<<"):
                operands += [b"<<"]
                i += 2
                continue
            if content_stream_bytes[i:].startswith(b">>"):
                dict_open_brackets_pos: int = operands.index(b"<<")
                arr = operands[dict_open_brackets_pos + 1 :]  # type: ignore[assignment]
                arr_as_dict = {arr[k]: arr[k + 1] for k in range(0, len(arr), 2)}
                operands = operands[:dict_open_brackets_pos] + [arr_as_dict]  # type: ignore[assignment]
                i += 2
                continue

            # space
            if content_stream_bytes[i : i + 1] == b" ":
                i += 1
                continue

            # newline
            if content_stream_bytes[i : i + 2] == b"\n\r":
                i += 2
                continue
            if content_stream_bytes[i : i + 2] == b"\r\n":
                i += 2
                continue
            if content_stream_bytes[i : i + 1] == b"\n":
                i += 1
                continue
            if content_stream_bytes[i : i + 1] == b"\r":
                i += 1
                continue

            # operators
            j = i + 1
            while any(
                [
                    x.get_name().startswith(content_stream_bytes[i:j].decode())
                    for x in self.operators
                ]
            ):
                j += 1
            j -= 1
            operator_code: str = content_stream_bytes[i:j].decode()
            operator: typing.Optional[Operator] = next(
                iter([x for x in self.operators if x.get_name() == operator_code]), None
            )
            if operator is not None:
                args: typing.List[PDFType] = []
                for _ in range(0, operator.get_number_of_operands()):
                    args += [operands.pop(-1)]  # type: ignore[list-item]
                args.reverse()
                operator.apply(
                    operands=args,  # type: ignore[arg-type]
                    page=page,
                    source=self,
                )
                i = j
                continue

            # move ahead 1 byte
            i += 1

    def stroke(self, line_width: float, shape: ShapeType, stroke_color: Color):
        """
        Initiate the process of pushing a stroking event down the pipe.

        This method starts the flow of a stroking-related event down the pipeline by creating
        and passing a stroking event. The event is triggered by the invocation of this method,
        which processes the given parameters to define the characteristics of the stroke to be
        applied to the current path.

        :param line_width:   The width of the stroke line. This parameter controls the thickness of the stroke applied to the path.
        :param shape:        The shape type of the stroke. This defines how the stroke's path corners and ends are rendered (e.g., round, square).
        :param stroke_color: The color of the stroke. This parameter defines the stroke's color, which will be applied based on the current graphics state.
        :return: None
        """
        next: typing.Optional[Pipe] = self.get_next()
        if next is None:
            return
        from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent

        assert self.__page is not None
        next.process(
            ShapeStrokeEvent(
                line_width=line_width,
                shape=shape,
                stroke_color=stroke_color,
                page=self.__page,
            )
        )

    def text(
        self,
        s: str,
        x: float,
        y: float,
        width: float,
        height: float,
        font: Font,
        font_color: Color,
        font_size: float,
    ):
        """
        Initiate the process of pushing a text event down the pipe.

        This method starts the flow of an event down the pipeline by creating and passing a
        text-related event. The event is triggered by the invocation of this method, which
        processes the given parameters to define the characteristics of the text to be
        rendered on a page.

        :param s:           The text string to be displayed. This is the content that will be shown at the specified coordinates.
        :param x:           The x-coordinate in user space where the text will be placed. This specifies the horizontal starting point of the text.
        :param y:           The y-coordinate in user space where the text will be placed. This specifies the vertical starting point of the text.
        :param width:       The width of the text string to be rendered. It may influence the positioning of subsequent elements.
        :param height:      The height of the text string to be rendered, used for vertical alignment and positioning relative to other elements.
        :param font:        The font to be used for rendering the text. This defines the style and design of the characters.
        :param font_color:  The color to be used for the text. This parameter defines the text’s color, which will be applied based on the current graphics state.
        :param font_size:   The size of the font to be applied to the text. This parameter determines the scale of the characters.
        :return: None
        """
        next: typing.Optional[Pipe] = self.get_next()
        if next is None:
            return
        from borb.pdf.toolkit.source.event.text_event import TextEvent

        assert self.__page is not None
        next.process(
            TextEvent(
                s=s,
                x=x,
                y=y,
                width=width,
                height=height,
                font=font,
                font_color=font_color,
                font_size=font_size,
                page=self.__page,
            )
        )
