#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents an easy way to manipulate a PDF document
that looks like a resume.
"""
import typing
from decimal import Decimal
from pathlib import Path

# fmt: off
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
# fmt: on

from borb.pdf.canvas.geometry.rectangle import Rectangle


class A4PortraitResumeTemplate:
    """
    This class represents an easy way to manipulate a PDF document
    that looks like a resume.
    """

    ACCENT_COLOR: Color = HexColor("#0b3954")
    DARK_GRAY_COLOR: Color = HexColor("#595959")
    LIGHT_GRAY_COLOR: Color = HexColor("#fafafa")

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._about_me: typing.Optional[str] = None
        self._document: typing.Optional[Document] = None
        self._email: typing.Optional[str] = None
        self._honors_and_awards: typing.List[str] = []
        self._interests: typing.List[str] = []
        self._languages_and_proficiency: typing.List[typing.Tuple[str, str]] = []
        self._linkedin: typing.Optional[str] = None
        self._location: typing.Optional[str] = None
        self._name: typing.Optional[str] = None
        self._phone_nr: typing.Optional[str] = None
        self._profile_picture: typing.Optional[str] = None
        self._skills: typing.List[str] = []
        self._twitter: typing.Optional[str] = None
        self._work_experience: typing.List[
            typing.Tuple[
                str, typing.Optional[str], str, typing.List[str], typing.Optional[str]
            ]
        ] = []

    #
    # PRIVATE
    #

    def _add_dragon_curve(self, page: Page, rectangle: Rectangle) -> None:
        W: Decimal = page.get_page_info().get_width()
        H: Decimal = page.get_page_info().get_height()
        ConnectedShape(
            LineArtFactory.dragon_curve(
                bounding_box=Rectangle(Decimal(0), Decimal(0), W, H),
                number_of_iterations=10,
            ),
            stroke_color=A4PortraitResumeTemplate.LIGHT_GRAY_COLOR,
        ).paint(page, Rectangle(Decimal(0), Decimal(0), W, H))

    def _add_page_numbers(self) -> None:
        N: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, N):
            s: Page = self._document.get_page(i)
            # add blue square
            ConnectedShape(
                LineArtFactory.rectangle(
                    Rectangle(Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47))
                ),
                stroke_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                fill_color=A4PortraitResumeTemplate.ACCENT_COLOR,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )
            # add Paragraph
            Paragraph(
                f"{i + 1}",
                font_size=Decimal(10),
                font_color=A4PortraitResumeTemplate.LIGHT_GRAY_COLOR,
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )

    def _build(self) -> None:

        # create (empty) Document
        self._document = Document()

        # add Page
        first_page: Page = Page()
        self._document.add_page(first_page)

        # add profile_picture
        layout: MultiColumnLayout = MultiColumnLayout(
            page=first_page,
            header_paint_method=self._add_dragon_curve,
            column_widths=[
                Decimal(0.3 * 595 - 59.5 - 30),
                Decimal(0.7 * 595 - 59.5 - 30),
            ],
            inter_column_margins=[Decimal(59.5)],
        )
        layout.add(
            Image(
                self._profile_picture,
                width=Decimal(75),
                height=Decimal(75),
                border_top=True,
                border_right=True,
                border_bottom=True,
                border_left=True,
                border_width=Decimal(2),
                border_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # add honors_and_awards
        if len(self._honors_and_awards) > 0:
            layout.add(
                Paragraph(
                    "HONORS, AWARDS",
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font_size=Decimal(16),
                    font="Courier-Bold",
                )
            )
            honors_and_awards_list: UnorderedList = UnorderedList()
            for h in self._honors_and_awards:
                honors_and_awards_list.add(
                    Paragraph(
                        h,
                        font_color=A4PortraitResumeTemplate.DARK_GRAY_COLOR,
                        font_size=Decimal(10),
                        font="Helvetica",
                    )
                )
            layout.add(honors_and_awards_list)

        # add interests
        if len(self._interests) > 0:
            layout.add(
                Paragraph(
                    "INTERESTS",
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font_size=Decimal(16),
                    font="Courier-Bold",
                )
            )
            interests_list: UnorderedList = UnorderedList()
            for i in self._interests:
                interests_list.add(
                    Paragraph(
                        i,
                        font_color=A4PortraitResumeTemplate.DARK_GRAY_COLOR,
                        font_size=Decimal(10),
                        font="Helvetica",
                    )
                )
            layout.add(interests_list)

        # add languages_and_proficiency
        if len(self._languages_and_proficiency) > 0:
            layout.add(
                Paragraph(
                    "LANGUAGES",
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font_size=Decimal(16),
                    font="Courier-Bold",
                )
            )
            languages: typing.List[ChunkOfText] = []
            for l, p in self._languages_and_proficiency:
                languages.append(ChunkOfText(l, font_size=Decimal(10)))
                languages.append(
                    ChunkOfText(
                        f" ({p})",
                        font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                        font_size=Decimal(10),
                    )
                )
                languages.append(ChunkOfText(", ", font_size=Decimal(10)))
            languages = languages[0:-1]
            layout.add(HeterogeneousParagraph(languages))

        # add skills
        if len(self._skills) > 0:
            layout.add(
                Paragraph(
                    "SKILLS",
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font_size=Decimal(16),
                    font="Courier-Bold",
                )
            )
            tags: typing.List[ChunkOfText] = []
            for s in self._skills:
                tags.append(
                    ChunkOfText(
                        s,
                        font_size=Decimal(10),
                        font_color=HexColor("ffffff"),
                        background_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                        border_radius_top_left=Decimal(5),
                        border_radius_top_right=Decimal(5),
                        border_radius_bottom_right=Decimal(5),
                        border_radius_bottom_left=Decimal(5),
                        padding_top=Decimal(3),
                        padding_right=Decimal(3),
                        padding_bottom=Decimal(0),
                        padding_left=Decimal(3),
                    )
                )
                tags.append(ChunkOfText(" "))
            layout.add(HeterogeneousParagraph(tags))

        # add name
        if layout._active_column == 0:
            layout.switch_to_next_column()
        layout.add(
            Paragraph(
                self._name,
                font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                font_size=Decimal(20),
                font="Courier-Bold",
            )
        )
        # add about_me
        layout.add(
            Paragraph(
                self._about_me,
                font_color=A4PortraitResumeTemplate.DARK_GRAY_COLOR,
                font_size=Decimal(10),
                text_alignment=Alignment.JUSTIFIED,
                font="Courier",
            )
        )

        # add table containing email, linkedin, location, phone_nr, twitter
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=3)
            # email
            .add(
                Image(
                    "https://img.icons8.com/?size=100&id=12623&format=png",
                    width=Decimal(16),
                    height=Decimal(16),
                )
            )
            .add(Paragraph(self._email or "N.A.", font_size=Decimal(8)))
            # linkedin
            .add(
                Image(
                    "https://img.icons8.com/?size=100&id=8808&format=png",
                    width=Decimal(16),
                    height=Decimal(16),
                )
            )
            .add(Paragraph(self._linkedin or "N.A.", font_size=Decimal(8)))
            # location
            .add(
                Image(
                    "https://img.icons8.com/?size=100&id=7880&format=png",
                    width=Decimal(16),
                    height=Decimal(16),
                )
            )
            .add(Paragraph(self._location or "N.A.", font_size=Decimal(8)))
            # phone_nr
            .add(
                Image(
                    "https://img.icons8.com/?size=100&id=9730&format=png",
                    width=Decimal(16),
                    height=Decimal(16),
                )
            )
            .add(Paragraph(self._phone_nr or "N.A.", font_size=Decimal(8)))
            # twitter
            .add(
                Image(
                    "https://img.icons8.com/?size=100&id=8824&format=png",
                    width=Decimal(16),
                    height=Decimal(16),
                )
            )
            .add(Paragraph(self._twitter or "N.A.", font_size=Decimal(8)))
            .add(Paragraph("", font_size=Decimal(8)))
            .add(Paragraph("", font_size=Decimal(8)))
            .set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            .no_borders()
        )

        # add work_experience
        layout._inter_column_margins = []
        layout._column_widths = [Decimal(0.7 * 595 - 59.5)]
        layout._margin_left = Decimal(0.3 * 595 + 30)
        layout._number_of_columns = 1
        layout._active_column = 0
        for w in self._work_experience:
            layout.add(
                Paragraph(
                    w[0],
                    font_size=Decimal(14),
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font="Courier-Bold",
                )
            )
            layout.add(
                Paragraph(
                    w[2],
                    font_size=Decimal(12),
                    font_color=A4PortraitResumeTemplate.ACCENT_COLOR,
                    font="Courier",
                    padding_left=Decimal(2 * 12),
                )
            )
            if w[4] is not None and w[1] is not None:
                layout.add(
                    Paragraph(
                        f"{w[4]} - {w[1]}",
                        font_size=Decimal(10),
                        font_color=A4PortraitResumeTemplate.DARK_GRAY_COLOR,
                        font="Courier",
                        padding_left=Decimal(2 * 12),
                    )
                )
            responsibilities_list: UnorderedList = UnorderedList(
                padding_left=Decimal(2 * 12)
            )
            for r in w[3]:
                responsibilities_list.add(
                    Paragraph(
                        r,
                        font_size=Decimal(10),
                        font_color=A4PortraitResumeTemplate.DARK_GRAY_COLOR,
                        font="Helvetica",
                    )
                )
            layout.add(responsibilities_list)

    #
    # PUBLIC
    #

    def add_honor_or_award(self, honor_or_award: str) -> "A4PortraitResumeTemplate":
        """
        This function adds an honor/award to the "honors and awards" section of this A4PortraitResumeTemplate
        :param honor_or_award:  the honor/award to be added
        :return:                self
        """
        self._honors_and_awards.append(honor_or_award)
        return self

    def add_interest(self, interest: str) -> "A4PortraitResumeTemplate":
        """
        This function adds an interest to the "interests" section of this A4PortraitResumeTemplate
        :param interest:    the interest to be added
        :return:            self
        """
        self._interests.append(interest)
        return self

    def add_language_and_proficiency(
        self, language: str, proficiency: str
    ) -> "A4PortraitResumeTemplate":
        """
        This function adds a language (and its associated proficiency) in the "languages" section of this A4PortraitResumeTemplate
        :param language:        a language
        :param proficiency:     its associated proficiency
        :return:                self
        """
        self._languages_and_proficiency.append((language, proficiency))
        return self

    def add_skill(self, skill: str) -> "A4PortraitResumeTemplate":
        """
        This function adds a skill to the "skills" section of this A4PortraitResumeTemplate
        :param skill:   the skill to be added
        :return:        self
        """
        self._skills.append(skill)
        return self

    def add_work_experience(
        self,
        company_name: str,
        end_date: typing.Optional[str],
        job_title: str,
        responsibilities: typing.List[str],
        start_date: typing.Optional[str],
    ) -> "A4PortraitResumeTemplate":
        """
        This function adds a work experience to the "work experience" section of this A4PortraitResumeTemplate
        :param company_name:        the name of the company
        :param end_date:            the end date of this work experience
        :param job_title:           the job title of this work experience
        :param responsibilities:    the responsibilities and/or achievements associated with this work experience
        :param start_date:          the start date of this work experience
        :return:                    self
        """
        self._work_experience.append(
            (company_name, end_date, job_title, responsibilities, start_date)
        )
        return self

    def save(self, path_or_str: typing.Union[str, Path]) -> "A4PortraitResumeTemplate":
        """
        This function stores this A4PortraitResumeTemplate at the given path
        :param path_or_str:     the path or str representing the location at which to store this A4PortraitResumeTemplate
        :return:                self
        """
        self._build()
        self._add_page_numbers()
        with open(path_or_str, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self._document)
        return self

    def set_about_me(self, about_me: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the text in the "about me" section of this A4PortraitResumeTemplate
        :param about_me:    the text for the "about me" section
        :return:            self
        """
        self._about_me = about_me
        return self

    def set_email(self, email: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the email (in the contact details section of this A4PortraitResumeTemplate)
        :param email:       the email
        :return:            self
        """
        self._email = email
        return self

    def set_linkedin(self, linkedin: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the LinkedIn URL (in the contact details section of this A4PortraitResumeTemplate)
        :param linkedin:    the LinkedIn URL
        :return:            self
        """
        self._linkedin = linkedin
        return self

    def set_location(self, location: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the location (in the contact details section of this A4PortraitResumeTemplate)
        :param location:    the location
        :return:            self
        """
        self._location = location
        return self

    def set_name(self, name: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the name in the "about me" section of this A4PortraitResumeTemplate
        :param name:    the name in the "about me" section
        :return:        self
        """
        self._name = name
        return self

    def set_phone_nr(self, phone_nr: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the phone nr (in the contact details section of this A4PortraitResumeTemplate)
        :param phone_nr:    the phone nr
        :return:            self
        """
        self._phone_nr = phone_nr
        return self

    def set_profile_picture(
        self, profile_picture: typing.Union[str, Path]
    ) -> "A4PortraitResumeTemplate":
        """
        This function sets the profile picture (URL or Path) in the "about me" section of this A4PortraitResumeTemplate
        :param profile_picture:     the profile picture (URL or Path) in the "about me" section
        :return:                    self
        """
        self._profile_picture = profile_picture
        return self

    def set_twitter(self, twitter: str) -> "A4PortraitResumeTemplate":
        """
        This function sets the X (Twitter) handle (in the contact details section of this A4PortraitResumeTemplate)
        :param twitter:     the X (Twitter) handle
        :return:            self
        """
        self._twitter = twitter
        return self
