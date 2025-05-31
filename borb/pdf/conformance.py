#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enum representing various PDF conformance levels.

These levels correspond to different standards of compliance for PDF documents,
ensuring accessibility, long-term preservation, and other requirements.
"""
import enum


class Conformance(enum.Enum):
    """
    Enum representing various PDF conformance levels.

    These levels correspond to different standards of compliance for PDF documents,
    ensuring accessibility, long-term preservation, and other requirements.

    - **PDF/A** (Archival) ensures documents remain readable over time.
        - `PDF_A_1A` and `PDF_A_1B` conform to PDF/A-1.
        - `PDF_A_2A`, `PDF_A_2B`, and `PDF_A_2U` conform to PDF/A-2.
        - `PDF_A_3A`, `PDF_A_3B`, and `PDF_A_3U` conform to PDF/A-3.
        - `PDF_A_4`, `PDF_A_4E`, and `PDF_A_4F` conform to PDF/A-4.

    - **PDF/UA** (Universal Accessibility) ensures accessibility for assistive technologies.
        - `PDF_UA_1` conforms to PDF/UA-1.
        - `PDF_UA_2` conforms to PDF/UA-2.
    """

    PDF_A_1A = 1
    PDF_A_1B = 2

    PDF_A_2A = 3
    PDF_A_2B = 4
    PDF_A_2U = 5

    PDF_A_3A = 6
    PDF_A_3B = 7
    PDF_A_3U = 8

    PDF_A_4 = 9
    PDF_A_4E = 10
    PDF_A_4F = 11

    PDF_UA_1 = 12
    PDF_UA_2 = 13

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_level(self) -> str:
        """
        Retrieve the non-numeric portion of the conformance level.

        This method returns the letter associated with the conformance level:
        - "A" for accessibility-compliant PDF/A levels.
        - "B" for basic compliance without accessibility features.
        - "U" for levels ensuring Unicode text mapping.

        :return: A string representing the conformance level category ("A", "B", or "U").
        """
        if self in [
            Conformance.PDF_A_1A,
            Conformance.PDF_A_2A,
            Conformance.PDF_A_3A,
        ]:
            return "A"
        if self in [
            Conformance.PDF_A_1B,
            Conformance.PDF_A_2B,
            Conformance.PDF_A_3B,
        ]:
            return "B"
        if self in [Conformance.PDF_A_2U, Conformance.PDF_A_3U]:
            return "U"
        assert False

    def get_version(self) -> int:
        """
        Retrieve the numeric portion of the conformance level.

        This method returns the numeric value representing the PDF/A version:
        - 1 for PDF/A-1.
        - 2 for PDF/A-2.
        - 3 for PDF/A-3.
        - 4 for PDF/A-4.

        :return: An integer representing the PDF/A version number.
        """
        if self in [Conformance.PDF_A_1A, Conformance.PDF_A_1B]:
            return 1
        if self in [
            Conformance.PDF_A_2A,
            Conformance.PDF_A_2B,
            Conformance.PDF_A_2U,
        ]:
            return 2
        if self in [
            Conformance.PDF_A_3A,
            Conformance.PDF_A_3B,
            Conformance.PDF_A_3U,
        ]:
            return 1
        if self in [
            Conformance.PDF_A_4,
            Conformance.PDF_A_4E,
            Conformance.PDF_A_4F,
        ]:
            return 4
        assert False

    def requires_icc_color_profile(self) -> bool:
        """
        Determine whether the current conformance level requires an ICC color profile.

        This method checks if the conformance level is one of the PDF/A or PDF/UA
        standards that require an embedded ICC color profile for color management.

        :return: True if an ICC color profile is required, False otherwise.
        """
        return self in {
            Conformance.PDF_A_1A,
            Conformance.PDF_A_1B,
            Conformance.PDF_A_2A,
            Conformance.PDF_A_2B,
            Conformance.PDF_A_2U,
            Conformance.PDF_A_3A,
            Conformance.PDF_A_3B,
            Conformance.PDF_A_3U,
            Conformance.PDF_A_4,
            Conformance.PDF_A_4E,
            Conformance.PDF_A_4F,
            Conformance.PDF_UA_1,
            Conformance.PDF_UA_2,
        }

    def requires_tagged_pdf(self) -> bool:
        """
        Determine whether the current conformance level requires a tagged PDF.

        This method checks if the conformance level is one of the PDF/A or PDF/UA
        standards that require a tagged PDF for accessibility and proper structure.

        :return: True if a tagged PDF is required, False otherwise.
        """
        return self in {
            Conformance.PDF_A_1A,
            Conformance.PDF_A_2A,
            Conformance.PDF_A_3A,
            Conformance.PDF_UA_1,
            Conformance.PDF_UA_2,
        }

    def requires_xmp_metadata(self) -> bool:
        """
        Determine whether the current conformance level requires XMP metadata.

        This method checks if the conformance level is one of the PDF/A or PDF/UA
        standards that require the inclusion of XMP (Extensible Metadata Platform)
        metadata for document compliance.

        :return: True if XMP metadata is required, False otherwise.
        """
        return self in {
            Conformance.PDF_A_1A,
            Conformance.PDF_A_1B,
            Conformance.PDF_A_2A,
            Conformance.PDF_A_2B,
            Conformance.PDF_A_2U,
            Conformance.PDF_A_3A,
            Conformance.PDF_A_3B,
            Conformance.PDF_A_3U,
            Conformance.PDF_A_4,
            Conformance.PDF_A_4E,
            Conformance.PDF_A_4F,
            Conformance.PDF_UA_1,
            Conformance.PDF_UA_2,
        }
