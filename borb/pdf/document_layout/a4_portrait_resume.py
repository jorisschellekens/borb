#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represent a resume in A4 portrait format.

The `A4PortraitResume` class enables users to create and customize a professional resume in A4 portrait layout.
It provides methods for adding personal information, work experience, education, skills, and other relevant sections
to the resume.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.document_layout.document_layout import DocumentLayout
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.smart_art.tags import Tags
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class A4PortraitResume(DocumentLayout):
    """
    Represent a resume in A4 portrait format.

    The `A4PortraitResume` class enables users to create and customize a professional resume in A4 portrait layout.
    It provides methods for adding personal information, work experience, education, skills, and other relevant sections
    to the resume.
    """

    __DARK_GRAY: Color = X11Color.DARK_GRAY
    __WHITE: Color = X11Color.WHITE
    __YELLOW_MUNSELL: Color = X11Color.YELLOW_MUNSELL

    #
    # CONSTRUCTOR
    #
    def __init__(self):
        """
        Initialize an A4PortraitResume object, a specialized subclass of A4Portrait for creating resumes.

        This constructor sets up a default A4 portrait-oriented document with pre-defined formatting
        and layout styles suited for creating professional resumes. No parameters are required.
        """
        self.__about_me: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__document: typing.Optional[Document] = None  # type: ignore[annotation-unchecked]
        self.__email: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__honors_and_awards: typing.List[str] = []  # type: ignore[annotation-unchecked]
        self.__interests: typing.List[str] = []  # type: ignore[annotation-unchecked]
        self.__languages_and_proficiency: typing.List[typing.Tuple[str, int]] = []  # type: ignore[annotation-unchecked]
        self.__linkedin: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__location: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__name: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__phone_nr: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__profile_picture: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__skills: typing.List[str] = []  # type: ignore[annotation-unchecked]
        self.__twitter: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        # fmt: off
        self.__work_experience: typing.List[                                        # type: ignore[annotation-unchecked]
            typing.Tuple[
                str,                    # name
                typing.Optional[str],   # from
                typing.Optional[str],   # to
                str,                    # description
                typing.List[str],       # tags
            ]
        ] = []
        # fmt: on

    #
    # PRIVATE
    #

    def __build(self) -> None:

        # start building the PDF
        self.__document = Document()

        # add empty Page
        page: Page = Page()
        self.__document.append_page(page)

        # short info
        # fmt: off
        short_info_table: Table = FlexibleColumnWidthTable(number_of_columns=1, number_of_rows=7)
        short_info_table.append_layout_element(Image(self.__profile_picture, size=(120, 120)))
        short_info_table.append_layout_element(self.__left_side_header("HONORS & AWARDS"))
        short_info_table.append_layout_element(self.__left_side_list(self.__honors_and_awards))
        short_info_table.append_layout_element(self.__left_side_header("LANGUAGES"))
        short_info_table.append_layout_element(self.__left_side_list([x for x,_ in self.__languages_and_proficiency]))
        short_info_table.append_layout_element(self.__left_side_header("SKILLS"))
        short_info_table.append_layout_element(self.__left_side_list(self.__skills))
        short_info_table.set_padding_on_all_cells(padding_bottom=5, padding_left=5, padding_right=5, padding_top=5)
        short_info_table.no_borders()
        short_info_table.paint(
            available_space=(
                page.get_size()[0] // 10,
                page.get_size()[1] // 10,
                110,
                page.get_size()[1] - 2 * page.get_size()[1] // 10,
            ),
            page=page,
        )
        previous_paint_box = short_info_table.get_previous_paint_box()
        assert previous_paint_box is not None
        _,_,w,_ = previous_paint_box
        # fmt: on

        # PageLayout to make it easier to append work information
        # fmt: off
        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout._MultiColumnLayout__page_margin_left = page.get_size()[0] // 10 + w + 10                            # type: ignore[attr-defined]
        page_layout._MultiColumnLayout__column_widths[0] = page.get_size()[0] -  2*(page.get_size()[0]//10) - w - 10    # type: ignore[attr-defined]

        # fmt: on

        # name
        page_layout.append_layout_element(
            Paragraph(
                self.__name or "John Doe",
                font=Standard14Fonts.get("Helvetica-Bold"),
                font_size=20,
                font_color=A4PortraitResume.__YELLOW_MUNSELL,
            )
        )

        # about
        from borb.pdf.lipsum.lipsum import Lipsum

        page_layout.append_layout_element(
            Paragraph(
                self.__about_me or Lipsum.generate_lorem_ipsum(512),
                font=Standard14Fonts.get("Helvetica-Italic"),
                font_color=A4PortraitResume.__DARK_GRAY,
            )
        )

        # contact information
        # fmt: off
        page_layout.append_layout_element(
            FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=3)
            .append_layout_element(Image("https://img.icons8.com/?size=100&id=8808&format=png", size=(16, 16)))
            .append_layout_element(Paragraph(self.__linkedin or "n.a."))
            .append_layout_element(Image("https://img.icons8.com/?size=100&id=phOKFKYpe00C&format=png", size=(16, 16)))
            .append_layout_element(Paragraph(self.__twitter or "n.a."))
            .append_layout_element(Image("https://img.icons8.com/?size=128&id=tiHbAqWU3ZCQ&format=png", size=(16, 16)))
            .append_layout_element(Paragraph(self.__email or "n.a."))
            .append_layout_element(Image("https://img.icons8.com/?size=60&id=78224&format=png", size=(16, 16)))
            .append_layout_element(Paragraph(self.__phone_nr or "n.a."))
            .append_layout_element(Image("https://img.icons8.com/?size=160&id=qPoyvo26Eh8c&format=png", size=(16, 16)))
            .append_layout_element(Paragraph(self.__location or "n.a."))
            .set_padding_on_all_cells(3, 0, 0, 3)
            .no_borders()
        )
        # fmt: on

        for work_experience in self.__work_experience:
            company, from_date, to_date, description, tags = work_experience
            work_experience_table: Table = FlexibleColumnWidthTable(
                number_of_columns=1, number_of_rows=4
            )
            work_experience_table.append_layout_element(
                Paragraph(
                    company,
                    font_color=A4PortraitResume.__YELLOW_MUNSELL,
                    font_size=16,
                    font=Standard14Fonts.get("Helvetica-Bold"),
                )
            )
            work_experience_table.append_layout_element(
                Paragraph(
                    f"{from_date} - {to_date}",
                    font_color=A4PortraitResume.__DARK_GRAY,
                    font=Standard14Fonts.get("Helvetica-Italic"),
                )
            )
            work_experience_table.append_layout_element(Paragraph(description))
            work_experience_table.append_layout_element(
                Tags.build(
                    tags,
                    background_color=A4PortraitResume.__YELLOW_MUNSELL,
                    level_1_font_color=A4PortraitResume.__WHITE,
                    level_1_font_size=12,
                )
            )
            work_experience_table.set_padding_on_all_cells(3, 0, 0, 3)
            work_experience_table.no_borders()
            page_layout.append_layout_element(work_experience_table)

    def __left_side_header(self, s: str) -> Paragraph:
        return Paragraph(
            s,
            font=Standard14Fonts.get("Helvetica-Bold"),
            background_color=A4PortraitResume.__YELLOW_MUNSELL,
            font_size=14,
            padding_bottom=5,
            padding_left=5,
            padding_right=5,
            font_color=A4PortraitResume.__WHITE,
        )

    def __left_side_list(self, s: typing.List[str]) -> UnorderedList:
        tmp: UnorderedList = UnorderedList()
        for x in s:
            tmp.append_layout_element(Paragraph(x))
        return tmp

    #
    # PUBLIC
    #

    def append_honors_or_award(self, honor_or_award: str) -> "A4PortraitResume":
        """
        Add an honor or award to the resume.

        This method appends a given honor or award to the honors and awards
        section of the resume.

        :param honor_or_award: A string describing the honor or award to add.
        :return: The updated A4PortraitResume instance.
        """
        self.__honors_and_awards += [honor_or_award]
        return self

    def append_language_and_proficiency(
        self, language: str, proficiency_on_a_scale_of_1_to_5: int
    ) -> "A4PortraitResume":
        """
        Add a language and its proficiency level to the resume.

        This method appends a language and the user's proficiency level
        (on a scale of 1 to 5) to the languages and proficiency section
        of the resume.

        :param language: The language to add.
        :param proficiency_on_a_scale_of_1_to_5: The proficiency level of the language on a scale from 1 (basic) to 5 (fluent).
        :return: The updated A4PortraitResume instance.
        """
        assert 1 <= proficiency_on_a_scale_of_1_to_5 <= 5
        self.__languages_and_proficiency += [
            (language, proficiency_on_a_scale_of_1_to_5)
        ]
        return self

    def append_skill(self, skill: str) -> "A4PortraitResume":
        """
        Add a skill to the resume.

        This method appends a skill to the skills section of the resume.

        :param skill: A string describing the skill to add.
        :return: The updated A4PortraitResume instance.
        """
        self.__skills += [skill]
        return self

    def append_work_experience(
        self,
        company: str,
        description: str,
        from_date: str,
        tags: typing.List[str],
        to_date: str,
    ) -> "A4PortraitResume":
        """
        Add a work experience entry to the resume.

        This method appends a work experience entry to the work experience
        section of the resume. Each entry includes the company name, duration,
        description, and associated tags.

        :param company: The name of the company where the experience was gained.
        :param description: A brief description of the role or responsibilities.
        :param from_date: The starting date of the experience (e.g., "Jan 2020").
        :param tags: A list of tags summarizing key skills or technologies used.
        :param to_date: The ending date of the experience (e.g., "Dec 2022").
        :return: The updated A4PortraitResume instance.
        """
        self.__work_experience += [(company, from_date, to_date, description, tags)]
        return self

    def save(self, path: str) -> "A4PortraitResume":
        """
        Save the resume to a specified file path.

        This method writes the current resume document to the given file path.
        The document will be saved in the PDF format. If the file already exists,
        it may be overwritten.

        :param path:    The file path where the resume will be saved.
        :return:        Self, allowing for method chaining.
        """
        self.__build()
        assert self.__document is not None
        PDF.write(what=self.__document, where_to=path)
        return self

    def set_about_me(self, about_me: str) -> "A4PortraitResume":
        """
        Set the candidate's 'About Me' section on the CV.

        Adds a brief personal summary to introduce the candidate's background, skills, and interests.

        :param about_me: Personal summary text describing the candidate.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__about_me = about_me
        return self

    def set_email(self, email: str) -> "A4PortraitResume":
        """
        Set the candidate's email address on the CV.

        Adds the specified email address to the resume's contact details section.

        :param email: Email address of the candidate.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__email = email
        return self

    def set_linkedin(self, linkedin_url: str) -> "A4PortraitResume":
        """
        Set the candidate's LinkedIn profile URL on the CV.

        Adds the specified LinkedIn URL to the resume, displaying it within the
        candidate's contact details section for easy access.

        :param linkedin_url: URL to the candidate’s LinkedIn profile.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__linkedin = linkedin_url
        return self

    def set_location(self, location: str) -> "A4PortraitResume":
        """
        Set the candidate's location on the CV.

        Adds the specified location (e.g., city, state, or country) to the resume,
        displaying it as part of the candidate’s contact information.

        :param location: Candidate’s location information.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__location = location
        return self

    def set_name(self, name: str) -> "A4PortraitResume":
        """
        Set the candidate's name on the CV.

        Adds the specified name to the resume, displaying it prominently at the top
        as part of the candidate's main information.

        :param name: Full name of the candidate.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__name = name
        return self

    def set_phone_nr(self, phone_nr: str) -> "A4PortraitResume":
        """
        Set the phone number on the CV.

        Adds the specified phone number to the resume, displaying it as part of the contact
        information in the document.

        :param phone_nr: Phone number to include in the resume.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__phone_nr = phone_nr
        return self

    def set_picture(self, picture_url: str) -> "A4PortraitResume":
        """
        Set the profile picture for the resume.

        This method sets the URL of the profile picture to be included in the resume.

        :param picture_url: The URL of the profile picture.
        :return: The updated A4PortraitResume instance.
        """
        self.__profile_picture = picture_url
        return self

    def set_twitter(self, twitter: str) -> "A4PortraitResume":
        """
        Set the Twitter handle on the CV.

        Adds the provided Twitter handle to the resume, allowing it to display alongside other
        contact information in the document. The Twitter handle is typically formatted as `@handle`.

        :param twitter: Twitter handle to include in the resume.
        :return: Returns the A4PortraitResume instance for method chaining.
        """
        self.__twitter = twitter
        return self
