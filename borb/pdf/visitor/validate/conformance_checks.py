#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Container class for accessing predefined conformance checks.

This class provides a convenience method to retrieve all known
`ConformanceCheck` instances used in PDF validation. It is designed
to serve as a centralized registry of specification checks, organized
for use in conformance-level validation workflows.

Portions of this conformance checking code are based on the veraPDF project,
developed by the veraPDF Consortium (https://verapdf.org/).

The veraPDF Validation project is dual-licensed, see:
- GPLv3+
- MPLv2+

Source: https://github.com/veraPDF
"""
import datetime
import re
import typing

from borb.pdf import Document
from borb.pdf.conformance import Conformance
from borb.pdf.primitives import name, hexstr, stream, datestr
from borb.pdf.visitor.validate.conformance_check import ConformanceCheck


class ConformanceChecks:
    """
    Container class for accessing predefined conformance checks.

    This class provides a convenience method to retrieve all known
    `ConformanceCheck` instances used in PDF validation. It is designed
    to serve as a centralized registry of specification checks, organized
    for use in conformance-level validation workflows.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __get_author_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            # Find the <dc:creator> sequence
            for desc in root.findall(".//rdf:Description", ns):
                creator_seq = desc.find("dc:creator/rdf:Seq", ns)
                if creator_seq is not None:
                    authors = [
                        li.text for li in creator_seq.findall("rdf:li", ns) if li.text
                    ]
                    if authors:
                        return ", ".join(authors)

            return None
        except Exception:
            return None

    @staticmethod
    def __get_channel_count_from_jpg2000_image(obj: typing.Any) -> typing.Optional[int]:
        try:
            from PIL import Image  # type: ignore[import-not-found]
            from io import BytesIO

            with Image.open(BytesIO(obj)) as img:
                return len(img.getbands())
        except Exception:
            return None

    @staticmethod
    def __get_creation_date_from_xmp(obj: str) -> typing.Optional[datetime.date]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "xmp": "http://ns.adobe.com/xap/1.0/",
            }

            # Look for CreateDate attribute
            for desc in root.findall(".//rdf:Description", ns):
                creation_date: typing.Optional[str] = desc.attrib.get(
                    f"{{{ns['xmp']}}}CreateDate"
                )
                if creation_date:
                    return datetime.datetime.fromisoformat(creation_date)

            return None
        except Exception:
            return None

    @staticmethod
    def __get_creator_tool_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "xmp": "http://ns.adobe.com/xap/1.0/",
            }

            # Look for CreatorTool attribute
            for desc in root.findall(".//rdf:Description", ns):
                creator_tool: typing.Optional[str] = desc.attrib.get(
                    f"{{{ns['xmp']}}}CreatorTool"
                )
                if creator_tool:
                    return creator_tool

            return None
        except Exception:
            return None

    @staticmethod
    def __get_keywords_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "xmp": "http://ns.adobe.com/xap/1.0/",
            }

            # Look for Keywords attribute
            for desc in root.findall(".//rdf:Description", ns):
                keywords: typing.Optional[str] = desc.attrib.get(
                    f"{{{ns['xmp']}}}Keywords"
                )
                if keywords:
                    return keywords

            return None
        except Exception:
            return None

    @staticmethod
    def __get_modification_date_from_xmp(obj: str) -> typing.Optional[datetime.date]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "xmp": "http://ns.adobe.com/xap/1.0/",
            }

            # Look for ModifyDate attribute
            for desc in root.findall(".//rdf:Description", ns):
                mod_date: typing.Optional[str] = desc.attrib.get(
                    f"{{{ns['xmp']}}}ModifyDate"
                )
                if mod_date:
                    return datetime.datetime.fromisoformat(mod_date)

            return None
        except Exception:
            return None

    @staticmethod
    def __get_pdfaid_conformance_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "pdfaid": "http://www.aiim.org/pdfa/ns/id/",
            }

            for desc in root.findall(".//rdf:Description", ns):
                conf = desc.find("pdfaid:conformance", ns)
                if conf is not None and conf.text:
                    return conf.text

            return None
        except Exception:
            return None

    @staticmethod
    def __get_pdfaid_part_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "pdfaid": "http://www.aiim.org/pdfa/ns/id/",
            }

            for desc in root.findall(".//rdf:Description", ns):
                part = desc.find("pdfaid:part", ns)
                if part is not None and part.text:
                    return part.text

            return None
        except Exception:
            return None

    @staticmethod
    def __get_pdfaid_revision_year(obj: str) -> typing.Optional[int]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "pdfaid": "http://www.aiim.org/pdfa/ns/id/",
            }

            for desc in root.findall(".//rdf:Description", ns):
                rev = desc.find("pdfaid:rev", ns)
                if rev is not None and rev.text:
                    text = rev.text.strip()
                    if text.isdigit() and len(text) == 4:
                        return int(text)  # Valid 4-digit year
                    else:
                        return None  # Present but invalid

            return None  # Not present
        except Exception:
            return None

    @staticmethod
    def __get_producer_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip <?xml ... ?> and <?xpacket ... ?>
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "pdf": "http://ns.adobe.com/pdf/1.3/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            }

            # Find rdf:Description elements and extract pdf:Producer attribute
            for desc in root.findall(".//rdf:Description", ns):
                producer = desc.attrib.get(f"{{{ns['pdf']}}}Producer")
                if producer:
                    return producer

            return None
        except Exception:
            return None

    @staticmethod
    def __get_subject_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            # Find <dc:subject> and extract <rdf:li> entries
            for desc in root.findall(".//rdf:Description", ns):
                bag = desc.find("dc:subject/rdf:Bag", ns)
                if bag is not None:
                    subjects = [li.text for li in bag.findall("rdf:li", ns) if li.text]
                    if subjects:
                        return ", ".join(subjects)

            return None
        except Exception:
            return None

    @staticmethod
    def __get_title_from_xmp(obj: str) -> typing.Optional[str]:
        try:
            # Strip xpacket wrapper
            obj = obj.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(obj)
            ns = {
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            # Find the <dc:title> element
            for desc in root.findall(".//rdf:Description", ns):
                title_elem = desc.find("dc:title/rdf:Alt/rdf:li", ns)
                if title_elem is not None and title_elem.text:
                    return title_elem.text

            return None
        except Exception:
            return None

    @staticmethod
    def __is_standard_14_font(obj: typing.Any) -> bool:
        if not isinstance(obj, dict):
            return False
        if not obj.get("Type") == "Font":
            return False
        if not obj.get("Subtype") == "Type1":
            return False
        if obj.get("BaseFont") not in [
            "Courier",
            "Courier-Bold",
            "Courier-Oblique",
            "Courier-BoldOblique",
            "Helvetica",
            "Helvetica-Bold",
            "Helvetica-Oblique",
            "Helvetica-BoldOblique",
            "Times-Roman",
            "Times-Bold",
            "Times-Italic",
            "Times-BoldItalic",
            "Symbol",
            "ZapfDingbats",
        ]:
            return False
        return True

    @staticmethod
    def __is_valid_xml(obj: typing.Any) -> bool:
        try:
            # decode
            xml_str: str = obj.decode("utf-8")

            # Strip xpacket wrapper
            xml_str = xml_str.split("?>", 1)[1].rsplit("<?xpacket", 1)[0]

            # Parse XML
            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml_str)

            # return
            return root is not None
        except:
            return False

    @staticmethod
    def __xmp_has_forbidden_bytes_attribute(obj: str) -> bool:
        # Extract xpacket header (first line starting with <?xpacket)
        match = re.search(r"<\?xpacket\s+([^>]+)\?>", obj)
        if match:
            header = match.group(1)
            # Look for bytes=... in the header
            return "bytes=" in header
        return False

    @staticmethod
    def __xmp_has_forbidden_encoding_attribute(obj: str) -> bool:
        match = re.search(r"<\?xpacket\s+([^>]+)\?>", obj)
        if match:
            header = match.group(1)
            return "encoding=" in header
        return False

    #
    # PUBLIC
    #

    @staticmethod
    def get() -> typing.List[ConformanceCheck]:
        """
        Retrieve all predefined conformance checks.

        This method returns a list of `ConformanceCheck` instances that represent
        validation rules for various PDF conformance levels (e.g., PDF/A, PDF/UA, PDF/X).
        These checks are typically statically defined and used to enforce compliance
        with the associated specifications.

        :return: A list of all known `ConformanceCheck` instances.
        """
        return [
            # [1/400] 6.1.10 (1) : The LZWDecode filter shall not be permitted
            ConformanceCheck(
                clause="6.1.10",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The LZWDecode filter shall not be permitted",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Filter") == "LZWDecode",
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [2/400] 6.1.10 (1) : The value of the F key in the Inline Image dictionary shall not be LZW, LZWDecode, Crypt, a value not listed in ISO 32000-1:2008, Table 6, or an array containing any such value
            ConformanceCheck(
                clause="6.1.10",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The value of the F key in the Inline Image dictionary shall not be LZW, LZWDecode, Crypt, a value not listed in ISO 32000-1:2008, Table 6, or an array containing any such value",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and (
                    (x.get("F") in ["LZW", "LZWDecode", "Crypt"])
                    or (
                        isinstance(x.get("F"), list)
                        and (
                            "LZW" in x.get("F")  # type: ignore[operator]
                            or "LZWDecode" in x.get("F")  # type: ignore[operator]
                            or "Crypt" in x.get("F")  # type: ignore[operator]
                        )
                    )
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [3/400] 6.1.10 (2) : The LZWDecode filter shall not be permitted
            ConformanceCheck(
                clause="6.1.10",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The LZWDecode filter shall not be permitted",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Filter") == "LZWDecode",
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [4/400] 6.1.11 (1) : A file specification dictionary, as defined in PDF 3.10.2, shall not contain the EF key
            ConformanceCheck(
                clause="6.1.11",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A file specification dictionary, as defined in PDF 3.10.2, shall not contain the EF key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Filespec"
                and "EF" in x,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [5/400] 6.1.11 (1) : No keys other than UR3 and DocMDP shall be present in a permissions dictionary (ISO 32000-2:2020, 12.8.6, Table 263)
            ConformanceCheck(
                clause="6.1.11",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="No keys other than UR3 and DocMDP shall be present in a permissions dictionary (ISO 32000-2:2020, 12.8.6, Table 263)",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and "Perms" in x
                and isinstance(x.get("Perms"), dict)
                and any([y not in ["UR3", "DocMDP"] for y in x.get("Perms").keys()]),  # type: ignore[union-attr]
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [6/400] 6.1.11 (2) : A file's name dictionary, as defined in PDF Reference 3.6.3, shall not contain the EmbeddedFiles key
            ConformanceCheck(
                clause="6.1.11",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A file's name dictionary, as defined in PDF Reference 3.6.3, shall not contain the EmbeddedFiles key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and "Names" in x
                    and isinstance(x.get("Names"), dict)
                    and "EmbeddedFiles" in x.get("Names")  # type: ignore[operator]
                ),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [7/400] 6.1.12 (1) : Largest Integer value is 2,147,483,647. Smallest integer value is -2,147,483,648
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Largest Integer value is 2,147,483,647. Smallest integer value is -2,147,483,648",
                lambda_function_to_check_object=lambda x: isinstance(x, int)
                and (x > 2147483647 or x < -2147483648),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [8/400] 6.1.12 (1) : No keys other than UR3 and DocMDP shall be present in a permissions dictionary (ISO 32000-1:2008, 12.8.4, Table 258)
            ConformanceCheck(
                clause="6.1.12",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="No keys other than UR3 and DocMDP shall be present in a permissions dictionary (ISO 32000-1:2008, 12.8.4, Table 258)",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and "Perms" in x
                and isinstance(x.get("Perms"), dict)
                and any([y not in ["UR3", "DocMDP"] for y in x.get("Perms").keys()]),  # type: ignore[union-attr]
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [9/400] 6.1.12 (1) : If the Version key is present in the document catalog dictionary, the first character in its value shall be a 2 (32h) and the second character of its value shall be a PERIOD (2Eh) (decimal point). The third character shall be a decimal digit. The number of characters of the value of the Version key shall be exactly 3
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If the Version key is present in the document catalog dictionary, the first character in its value shall be a 2 (32h) and the second character of its value shall be a PERIOD (2Eh) (decimal point). The third character shall be a decimal digit. The number of characters of the value of the Version key shall be exactly 3",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and isinstance(x.get("Version"), str)
                and (
                    len(x.get("Version")) != 3  # type: ignore[arg-type]
                    or x.get("Version")[0] != "2"  # type: ignore[index]
                    or x.get("Version")[1] != "."  # type: ignore[index]
                    or x.get("Version")[2] not in "0123456789"  # type: ignore[index]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [11/400] 6.1.12 (2) : Absolute real value must be less than or equal to 32767.0
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Absolute real value must be less than or equal to 32767.0",
                lambda_function_to_check_object=lambda x: isinstance(x, float)
                and (x > 32767 or x < -32767),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [13/400] 6.1.12 (3) : Maximum length of a string (in bytes) is 65535
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Maximum length of a string (in bytes) is 65535",
                lambda_function_to_check_object=lambda x: isinstance(x, str)
                and len(x) > 65535,
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [14/400] 6.1.12 (4) : Maximum length of a name (in bytes) is 127
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Maximum length of a name (in bytes) is 127",
                lambda_function_to_check_object=lambda x: isinstance(x, name)
                and len(str(x)) > 127,
                specification="ISO_19005_1",
                test_number=4,
            ),
            # [15/400] 6.1.12 (5) : Maximum capacity of an array (in elements) is 8191
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Maximum capacity of an array (in elements) is 8191",
                lambda_function_to_check_object=lambda x: isinstance(x, list)
                and len(x) > 8191,
                specification="ISO_19005_1",
                test_number=5,
            ),
            # [16/400] 6.1.12 (6) : Maximum capacity of a dictionary (in entries) is 4095
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Maximum capacity of a dictionary (in entries) is 4095",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and len(x) > 4095,
                specification="ISO_19005_1",
                test_number=6,
            ),
            # [17/400] 6.1.12 (7) : Maximum number of indirect objects in a PDF file is 8,388,607
            ConformanceCheck(
                clause="6.1.12",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Maximum number of indirect objects in a PDF file is 8,388,607",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "XRef" in x
                and isinstance(x.get("XRef"), list)
                and len(x.get("XRef")) > 8388607,  # type: ignore[arg-type]
                specification="ISO_19005_1",
                test_number=7,
            ),
            # [20/400] 6.1.13 (1) : The document catalog dictionary shall not contain a key with the name OCProperties
            ConformanceCheck(
                clause="6.1.13",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The document catalog dictionary shall not contain a key with the name OCProperties",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "OCProperties" in x,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [21/400] 6.1.13 (1) : A conforming file shall not contain any integer greater than 2147483647. A conforming file shall not contain any integer less than -2147483648
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any integer greater than 2147483647. A conforming file shall not contain any integer less than -2147483648",
                lambda_function_to_check_object=lambda x: isinstance(x, int)
                and x > 2147483647
                or x < -2147483648,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [23/400] 6.1.13 (11) : The size of any of the page boundaries described in ISO 32000-1:2008, 14.11.2 shall not be less than 3 units in either direction, nor shall it be greater than 14 400 units in either direction
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The size of any of the page boundaries described in ISO 32000-1:2008, 14.11.2 shall not be less than 3 units in either direction, nor shall it be greater than 14 400 units in either direction",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Page"
                and (
                    (
                        "CropBox" in x
                        and isinstance(x.get("CropBox"), list)
                        and len(x.get("CropBox")) == 4  # type: ignore[arg-type]
                        and (
                            isinstance(x.get("CropBox")[0], int)  # type: ignore[index]
                            or isinstance(x.get("CropBox")[0], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("CropBox")[1], int)  # type: ignore[index]
                            or isinstance(x.get("CropBox")[1], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("CropBox")[2], int)  # type: ignore[index]
                            or isinstance(x.get("CropBox")[2], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("CropBox")[3], int)  # type: ignore[index]
                            or isinstance(x.get("CropBox")[3], float)  # type: ignore[index]
                        )
                        and (
                            x.get("CropBox")[2] - x.get("CropBox")[0] < 3  # type: ignore[index]
                            or x.get("CropBox")[3] - x.get("CropBox")[1] < 3  # type: ignore[index]
                        )
                    )
                    or (
                        "MediaBox" in x
                        and isinstance(x.get("MediaBox"), list)
                        and len(x.get("MediaBox")) == 4  # type: ignore[arg-type]
                        and (
                            isinstance(x.get("MediaBox")[0], int)  # type: ignore[index]
                            or isinstance(x.get("MediaBox")[0], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("MediaBox")[1], int)  # type: ignore[index]
                            or isinstance(x.get("MediaBox")[1], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("MediaBox")[2], int)  # type: ignore[index]
                            or isinstance(x.get("MediaBox")[2], float)  # type: ignore[index]
                        )
                        and (
                            isinstance(x.get("MediaBox")[3], int)  # type: ignore[index]
                            or isinstance(x.get("MediaBox")[3], float)  # type: ignore[index]
                        )
                        and (
                            x.get("MediaBox")[2] - x.get("MediaBox")[0] < 3  # type: ignore[index]
                            or x.get("MediaBox")[3] - x.get("MediaBox")[1] < 3  # type: ignore[index]
                        )
                    )
                ),
                specification="ISO_19005_3",
                test_number=11,
            ),
            # [24/400] 6.1.13 (2) : A conforming file shall not contain any real number outside the range of +/-3.403 x 10^38
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any real number outside the range of +/-3.403 x 10^38",
                lambda_function_to_check_object=lambda x: isinstance(x, float)
                and x > 3.403e38
                or x < -3.403e38,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [25/400] 6.1.13 (3) : A conforming file shall not contain any string longer than 32767 bytes
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any string longer than 32767 bytes",
                lambda_function_to_check_object=lambda x: isinstance(x, str)
                and len(x) > 32767,
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [26/400] 6.1.13 (4) : A conforming file shall not contain any name longer than 127 bytes
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any name longer than 127 bytes",
                lambda_function_to_check_object=lambda x: isinstance(x, name)
                and len(str(x)) > 127,
                specification="ISO_19005_3",
                test_number=4,
            ),
            # [27/400] 6.1.13 (5) : A conforming file shall not contain any real number closer to zero than +/-1.175 x 10^(-38)
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any real number closer to zero than +/-1.175 x 10^(-38)",
                lambda_function_to_check_object=lambda x: isinstance(x, float)
                and abs(x) > 1.175e-38,
                specification="ISO_19005_3",
                test_number=5,
            ),
            # [28/400] 6.1.13 (7) : A conforming file shall not contain more than 8388607 indirect objects
            ConformanceCheck(
                clause="6.1.13",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain more than 8388607 indirect objects",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "XRef" in x
                and isinstance(x.get("XRef"), list)
                and len(x.get("XRef")) > 8388607,  # type: ignore[arg-type]
                specification="ISO_19005_3",
                test_number=7,
            ),
            # [31/400] 6.1.2 (1) : The % character of the file header shall occur at byte offset 0 of the file. The first line of a PDF file is a header identifying the version of the PDF specification to which the file conforms
            ConformanceCheck(
                clause="6.1.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The % character of the file header shall occur at byte offset 0 of the file. The first line of a PDF file is a header identifying the version of the PDF specification to which the file conforms",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [32/400] 6.1.2 (1) : The file header shall begin at byte zero and shall consist of "%PDF-1.n" followed by a single EOL marker, where 'n' is a single digit number between 0 (30h) and 7 (37h)
            ConformanceCheck(
                clause="6.1.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The file header shall begin at byte zero and shall consist of \"%PDF-1.n\" followed by a single EOL marker, where 'n' is a single digit number between 0 (30h) and 7 (37h)",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [33/400] 6.1.2 (1) : The file header shall begin at byte zero and shall consist of "%PDF-2.n" followed by a single EOL marker, where 'n' is a single digit number between 0 (30h) and 9 (39h)
            ConformanceCheck(
                clause="6.1.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The file header shall begin at byte zero and shall consist of \"%PDF-2.n\" followed by a single EOL marker, where 'n' is a single digit number between 0 (30h) and 9 (39h)",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [34/400] 6.1.2 (2) : The file header line shall be immediately followed by a comment consisting of a % character followed by at least four characters, each of whose encoded byte values shall have a decimal value greater than 127
            ConformanceCheck(
                clause="6.1.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The file header line shall be immediately followed by a comment consisting of a % character followed by at least four characters, each of whose encoded byte values shall have a decimal value greater than 127",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [35/400] 6.1.2 (2) : The aforementioned EOL marker shall be immediately followed by a % (25h) character followed by at least four bytes, each of whose encoded byte values shall have a decimal value greater than 127
            ConformanceCheck(
                clause="6.1.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="The aforementioned EOL marker shall be immediately followed by a % (25h) character followed by at least four bytes, each of whose encoded byte values shall have a decimal value greater than 127",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [36/400] 6.1.3 (1) : The file trailer dictionary shall contain the ID keyword. The file trailer referred to is either the last trailer dictionary in a PDF file, as described in PDF Reference 3.4.4 and 3.4.5, or the first page trailer in a linearized PDF file, as described in PDF Reference F.2
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The file trailer dictionary shall contain the ID keyword. The file trailer referred to is either the last trailer dictionary in a PDF file, as described in PDF Reference 3.4.4 and 3.4.5, or the first page trailer in a linearized PDF file, as described in PDF Reference F.2",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "ID" not in x.get("Trailer"),  # type: ignore[operator]
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [37/400] 6.1.3 (1) : The file trailer dictionary shall contain the ID keyword whose value shall be File Identifiers as defined in ISO 32000-1:2008, 14.4
            ConformanceCheck(
                clause="6.1.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The file trailer dictionary shall contain the ID keyword whose value shall be File Identifiers as defined in ISO 32000-1:2008, 14.4",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and (
                    ("Trailer" not in x)
                    or (not isinstance(x.get("Trailer"), dict))
                    or ("ID" not in x.get("Trailer"))  # type: ignore[operator]
                    or (not isinstance(x.get("Trailer").get("ID"), list))  # type: ignore[union-attr]
                    or (len(x.get("Trailer").get("ID")) != 2)  # type: ignore[union-attr]
                    or (not isinstance(x.get("Trailer").get("ID")[0], hexstr))  # type: ignore[union-attr]
                    or (not isinstance(x.get("Trailer").get("ID")[1], hexstr))  # type: ignore[union-attr]
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [38/400] 6.1.3 (1) : File identifiers shall be defined by the ID entry in a PDF file’s trailer dictionary
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="File identifiers shall be defined by the ID entry in a PDF file’s trailer dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and (
                    ("Trailer" not in x)
                    or (not isinstance(x.get("Trailer"), dict))
                    or ("ID" not in x.get("Trailer"))  # type: ignore[operator]
                    or (not isinstance(x.get("Trailer").get("ID"), list))  # type: ignore[union-attr]
                    or (len(x.get("Trailer").get("ID")) != 2)  # type: ignore[union-attr]
                    or (not isinstance(x.get("Trailer").get("ID")[0], hexstr))  # type: ignore[union-attr]
                    or (not isinstance(x.get("Trailer").get("ID")[1], hexstr))  # type: ignore[union-attr]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [39/400] 6.1.3 (2) : The keyword Encrypt shall not be used in the trailer dictionary
            ConformanceCheck(
                clause="6.1.3",
                conformance=[
                    Conformance.PDF_A_1A,
                    Conformance.PDF_A_1B,
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The keyword Encrypt shall not be used in the trailer dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Encrypt" in x.get("Trailer"),  # type: ignore[operator]
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [40/400] 6.1.3 (2) : The Encrypt key shall not be present in the trailer dictionary
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The Encrypt key shall not be present in the trailer dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Encrypt" in x.get("Trailer"),  # type: ignore[operator]
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [41/400] 6.1.3 (3) : No data shall follow the last end-of-file marker except a single optional end-of-line marker
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="No data shall follow the last end-of-file marker except a single optional end-of-line marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [42/400] 6.1.3 (3) : No data can follow the last end-of-file marker except a single optional end-of-line marker as described in ISO 32000-1:2008, 7.5.5
            ConformanceCheck(
                clause="6.1.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="No data can follow the last end-of-file marker except a single optional end-of-line marker as described in ISO 32000-1:2008, 7.5.5",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [43/400] 6.1.3 (3) : No data shall follow the last end-of-file marker as described in ISO 32000-2:2020, 7.5.5
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="No data shall follow the last end-of-file marker as described in ISO 32000-2:2020, 7.5.5",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [46/400] 6.1.3 (5) : If a document information dictionary is present, it shall only contain a ModDate entry
            ConformanceCheck(
                clause="6.1.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If a document information dictionary is present, it shall only contain a ModDate entry",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and any([y != "ModDate" for y in x.get("Trailer").get("Info").keys()]),  # type: ignore[union-attr]
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [47/400] 6.1.4 (1) : In a cross reference subsection header the starting object number and the range shall be separated by a single SPACE character (20h)
            ConformanceCheck(
                clause="6.1.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="In a cross reference subsection header the starting object number and the range shall be separated by a single SPACE character (20h)",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [48/400] 6.1.4 (1) : The xref keyword and the cross-reference subsection header shall be separated by a single EOL marker
            ConformanceCheck(
                clause="6.1.4",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The xref keyword and the cross-reference subsection header shall be separated by a single EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [49/400] 6.1.4 (2) : The xref keyword and the cross reference subsection header shall be separated by a single EOL marker
            ConformanceCheck(
                clause="6.1.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The xref keyword and the cross reference subsection header shall be separated by a single EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [50/400] 6.1.4 (2) : The xref keyword and the cross-reference subsection header shall be separated by a single EOL marker
            ConformanceCheck(
                clause="6.1.4",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The xref keyword and the cross-reference subsection header shall be separated by a single EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [51/400] 6.1.4 (3) : Xref streams shall not be used
            ConformanceCheck(
                clause="6.1.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Xref streams shall not be used",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "XRef",
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [52/400] 6.1.5 (1) : Hexadecimal strings shall contain an even number of non-white-space characters
            ConformanceCheck(
                clause="6.1.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="Hexadecimal strings shall contain an even number of non-white-space characters",
                lambda_function_to_check_object=lambda x: isinstance(x, hexstr)
                and len([y for y in x if not y.isspace()]) % 2 != 0,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [53/400] 6.1.5 (2) : A hexadecimal string is written as a sequence of hexadecimal digits (0–9 and either A–F or a–f)
            ConformanceCheck(
                clause="6.1.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A hexadecimal string is written as a sequence of hexadecimal digits (0–9 and either A–F or a–f)",
                lambda_function_to_check_object=lambda x: isinstance(x, hexstr)
                and any(
                    [y not in "0123456789ABCDEFabcdef" for y in x if not y.isspace()]
                ),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [54/400] 6.1.6 (1) : Hexadecimal strings shall contain an even number of non-white-space characters
            ConformanceCheck(
                clause="6.1.6",
                conformance=[
                    Conformance.PDF_A_1A,
                    Conformance.PDF_A_1B,
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="Hexadecimal strings shall contain an even number of non-white-space characters",
                lambda_function_to_check_object=lambda x: isinstance(x, hexstr)
                and len([y for y in x if not y.isspace()]) % 2 != 0,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [55/400] 6.1.6 (2) : All non-white-space characters in hexadecimal strings shall be in the range 0 to 9, A to F or a to f
            ConformanceCheck(
                clause="6.1.6",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="All non-white-space characters in hexadecimal strings shall be in the range 0 to 9, A to F or a to f",
                lambda_function_to_check_object=lambda x: isinstance(x, hexstr)
                and any(
                    [y not in "0123456789ABCDEFabcdef" for y in x if not y.isspace()]
                ),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [56/400] 6.1.6 (2) : A hexadecimal string is written as a sequence of hexadecimal digits (0–9 and either A–F or a–f)
            ConformanceCheck(
                clause="6.1.6",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A hexadecimal string is written as a sequence of hexadecimal digits (0–9 and either A–F or a–f)",
                lambda_function_to_check_object=lambda x: isinstance(x, hexstr)
                and any(
                    [y not in "0123456789ABCDEFabcdef" for y in x if not y.isspace()]
                ),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [57/400] 6.1.6.1 (1) : The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED (0Ah) character after the stream keyword and preceding the EOL marker before the endstream keyword
            ConformanceCheck(
                clause="6.1.6.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED (0Ah) character after the stream keyword and preceding the EOL marker before the endstream keyword",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and "Length" in x
                and isinstance(x.get("Length"), int)
                and "Bytes" in x
                and isinstance(x.get("Bytes"), bytes)
                and len(x.get("Bytes")) != x.get("Length"),  # type: ignore[arg-type]
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [58/400] 6.1.6.1 (2) : A stream dictionary shall not contain the F, FFilter, or FDecodeParms keys
            ConformanceCheck(
                clause="6.1.6.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A stream dictionary shall not contain the F, FFilter, or FDecodeParms keys",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and ("F" in x or "FFilter" in x or "FDecodeParms" in x),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [59/400] 6.1.6.1 (3) : The Subtype entry in a 3D stream dictionary (ISO 32000-2:2020, 13.6.3) shall have a value which is either U3D or PRC as described in Annex B
            ConformanceCheck(
                clause="6.1.6.1",
                conformance=[Conformance.PDF_A_4E],
                description="The Subtype entry in a 3D stream dictionary (ISO 32000-2:2020, 13.6.3) shall have a value which is either U3D or PRC as described in Annex B",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "3D"
                and x.get("Subtype") not in ["U3D", "PRC"],
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [60/400] 6.1.6.2 (1) : All standard stream filters listed in ISO 32000-2:2020, 7.4, Table 6 may be used, with the exception of LZWDecode. Filters that are not listed in ISO 32000-2:2020, 7.4, Table 6 shall not be used. In addition, the Crypt filter shall not be used unless the value of the Name key in the decode parameters dictionary is Identity
            ConformanceCheck(
                clause="6.1.6.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All standard stream filters listed in ISO 32000-2:2020, 7.4, Table 6 may be used, with the exception of LZWDecode. Filters that are not listed in ISO 32000-2:2020, 7.4, Table 6 shall not be used. In addition, the Crypt filter shall not be used unless the value of the Name key in the decode parameters dictionary is Identity",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and "Length" in x
                and isinstance(x.get("Length"), int)
                and "Bytes" in x
                and isinstance(x.get("Bytes"), bytes)
                and len(x.get("Bytes")) != x.get("Length"),  # type: ignore[arg-type]
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [61/400] 6.1.7 (1) : The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED character after the stream keyword and preceding the EOL marker before the endstream keyword
            ConformanceCheck(
                clause="6.1.7",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED character after the stream keyword and preceding the EOL marker before the endstream keyword",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and "Length" in x
                and isinstance(x.get("Length"), int)
                and "Bytes" in x
                and isinstance(x.get("Bytes"), bytes)
                and len(x.get("Bytes")) != x.get("Length"),  # type: ignore[arg-type]
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [63/400] 6.1.7 (2) : The stream keyword shall be followed either by a CARRIAGE RETURN (0Dh) and LINE FEED (0Ah) character sequence or by a single LINE FEED character. The endstream keyword shall be preceded by an EOL marker
            ConformanceCheck(
                clause="6.1.7",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The stream keyword shall be followed either by a CARRIAGE RETURN (0Dh) and LINE FEED (0Ah) character sequence or by a single LINE FEED character. The endstream keyword shall be preceded by an EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [64/400] 6.1.7 (3) : A stream object dictionary shall not contain the F, FFilter, or FDecodeParms keys
            ConformanceCheck(
                clause="6.1.7",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A stream object dictionary shall not contain the F, FFilter, or FDecodeParms keys",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and ("F" in x or "FFilter" in x or "FDecodeParms" in x),
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [65/400] 6.1.7.1 (1) : The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED (0Ah) character after the stream keyword and preceding the EOL marker before the endstream keyword
            ConformanceCheck(
                clause="6.1.7.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The value of the Length key specified in the stream dictionary shall match the number of bytes in the file following the LINE FEED (0Ah) character after the stream keyword and preceding the EOL marker before the endstream keyword",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and "Length" in x
                and isinstance(x.get("Length"), int)
                and "Bytes" in x
                and isinstance(x.get("Bytes"), bytes)
                and len(x.get("Bytes")) != x.get("Length"),  # type: ignore[arg-type]
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [66/400] 6.1.7.1 (2) : The stream keyword shall be followed either by a CARRIAGE RETURN (0Dh) and LINE FEED (0Ah) character sequence or by a single LINE FEED (0Ah) character. The endstream keyword shall be preceded by an EOL marker
            ConformanceCheck(
                clause="6.1.7.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The stream keyword shall be followed either by a CARRIAGE RETURN (0Dh) and LINE FEED (0Ah) character sequence or by a single LINE FEED (0Ah) character. The endstream keyword shall be preceded by an EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [67/400] 6.1.7.1 (3) : A stream dictionary shall not contain the F, FFilter, or FDecodeParms keys
            ConformanceCheck(
                clause="6.1.7.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A stream dictionary shall not contain the F, FFilter, or FDecodeParms keys",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and ("F" in x or "FFilter" in x or "FDecodeParms" in x),
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [70/400] 6.1.8 (1) : The object number and generation number shall be separated by a single white-space character. The generation number and obj keyword shall be separated by a single white-space character. The object number and endobj keyword shall each be preceded by an EOL marker. The obj and endobj keywords shall each be followed by an EOL marker
            ConformanceCheck(
                clause="6.1.8",
                conformance=[
                    Conformance.PDF_A_1A,
                    Conformance.PDF_A_1B,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="The object number and generation number shall be separated by a single white-space character. The generation number and obj keyword shall be separated by a single white-space character. The object number and endobj keyword shall each be preceded by an EOL marker. The obj and endobj keywords shall each be followed by an EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [71/400] 6.1.9 (1) : The object number and generation number shall be separated by a single white-space character. The generation number and obj keyword shall be separated by a single white-space character. The object number and endobj keyword shall each be preceded by an EOL marker. The obj and endobj keywords shall each be followed by an EOL marker
            ConformanceCheck(
                clause="6.1.9",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The object number and generation number shall be separated by a single white-space character. The generation number and obj keyword shall be separated by a single white-space character. The object number and endobj keyword shall each be preceded by an EOL marker. The obj and endobj keywords shall each be followed by an EOL marker",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [73/400] 6.10 (1) : There shall be no AlternatePresentations entry in the document's name dictionary
            ConformanceCheck(
                clause="6.10",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="There shall be no AlternatePresentations entry in the document's name dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and "Names" in x
                and isinstance(x.get("Names"), dict)
                and "AlternatePresentations" in x.get("Names"),  # type: ignore[operator]
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [75/400] 6.10 (2) : There shall be no PresSteps entry in any Page dictionary
            ConformanceCheck(
                clause="6.10",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="There shall be no PresSteps entry in any Page dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Page"
                and "PresSteps" in x,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [78/400] 6.11 (1) : The document catalog shall not contain the Requirements key
            ConformanceCheck(
                clause="6.11",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The document catalog shall not contain the Requirements key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "Requirements" in x,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [79/400] 6.11 (1) : There shall be no AlternatePresentations entry in the document's name dictionary
            ConformanceCheck(
                clause="6.11",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="There shall be no AlternatePresentations entry in the document's name dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and "Names" in x
                and isinstance(x.get("Names"), dict)
                and "AlternatePresentations" in x.get("Names"),  # type: ignore[operator]
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [80/400] 6.11 (2) : There shall be no PresSteps entry in any Page dictionary
            ConformanceCheck(
                clause="6.11",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="There shall be no PresSteps entry in any Page dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Page"
                and "PresSteps" in x,
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [81/400] 6.12 (1) : The document catalog shall not contain the Requirements key
            ConformanceCheck(
                clause="6.12",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The document catalog shall not contain the Requirements key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "Requirements" in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [85/400] 6.2.10.2 (1) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Type - name - (Required) The type of PDF object that this dictionary describes; must be Font for a font dictionary
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Type - name - (Required) The type of PDF object that this dictionary describes; must be Font for a font dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Subtype")
                in [
                    "Type1",
                    "MMType1",
                    "TrueType",
                    "Type3",
                    "Type0",
                    "CIDFontType0",
                    "CIDFontType2",
                ]
                and x.get("Type") != "Font",
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [86/400] 6.2.10.2 (2) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Subtype - name - (Required) The type of font; must be "Type1" for Type 1 fonts, "MMType1" for multiple master fonts, "TrueType" for TrueType fonts "Type3" for Type 3 fonts, "Type0" for Type 0 fonts and "CIDFontType0" or "CIDFontType2" for CID fonts
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Subtype - name - (Required) The type of font; must be "Type1" for Type 1 fonts, "MMType1" for multiple master fonts, "TrueType" for TrueType fonts "Type3" for Type 3 fonts, "Type0" for Type 0 fonts and "CIDFontType0" or "CIDFontType2" for CID fonts',
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and x.get("Subtype")
                not in [
                    "Type1",
                    "MMType1",
                    "TrueType",
                    "Type3",
                    "Type0",
                    "CIDFontType0",
                    "CIDFontType2",
                ],
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [87/400] 6.2.10.2 (3) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. BaseFont - name - (Required) The PostScript name of the font
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. BaseFont - name - (Required) The PostScript name of the font",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "BaseFont" not in x,
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [88/400] 6.2.10.2 (4) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("FirstChar"), int),
                specification="ISO_19005_4",
                test_number=4,
            ),
            # [89/400] 6.2.10.2 (5) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("LastChar"), int),
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [90/400] 6.2.10.2 (6) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths
            ConformanceCheck(
                clause="6.2.10.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-2:2020, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "FirstChar" in x
                and isinstance(x.get("FirstChar"), int)
                and "LastChar" in x
                and isinstance(x.get("LastChar"), int)
                and "Widths" in x
                and isinstance(x.get("Widths"), list)
                and len(x.get("Widths")) != x.get("LastChar") - x.get("FirstChar") + 1,  # type: ignore[arg-type, operator]
                specification="ISO_19005_4",
                test_number=6,
            ),
            # [109/400] 6.2.11.2 (3) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. BaseFont - name - (Required) The PostScript name of the font
            ConformanceCheck(
                clause="6.2.11.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. BaseFont - name - (Required) The PostScript name of the font",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "BaseFont" not in x,
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [110/400] 6.2.11.2 (4) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.2.11.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("FirstChar"), int),
                specification="ISO_19005_3",
                test_number=4,
            ),
            # [111/400] 6.2.11.2 (5) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.2.11.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("LastChar"), int),
                specification="ISO_19005_3",
                test_number=5,
            ),
            # [112/400] 6.2.11.2 (6) : All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths
            ConformanceCheck(
                clause="6.2.11.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All fonts and font programs used in a conforming file, regardless of rendering mode usage, shall conform to the provisions in ISO 32000-1:2008, 9.6 and 9.7, as well as to the font specifications referenced by these provisions. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "FirstChar" in x
                and isinstance(x.get("FirstChar"), int)
                and "LastChar" in x
                and isinstance(x.get("LastChar"), int)
                and "Widths" in x
                and isinstance(x.get("Widths"), list)
                and len(x.get("Widths")) != x.get("LastChar") - x.get("FirstChar") + 1,  # type: ignore[arg-type, operator]
                specification="ISO_19005_3",
                test_number=6,
            ),
            # [113/400] 6.2.11.2 (7) : All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. The subtype is the value of the Subtype key, if present, in the font file stream dictionary. The only valid values of this key in PDF 1.7 are Type1C - Type 1–equivalent font program represented in the Compact Font Format (CFF), CIDFontType0C - Type 0 CIDFont program represented in the Compact Font Format (CFF) and OpenType - OpenType® font program, as described in the OpenType Specification v.1.4
            ConformanceCheck(
                clause="6.2.11.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. The subtype is the value of the Subtype key, if present, in the font file stream dictionary. The only valid values of this key in PDF 1.7 are Type1C - Type 1–equivalent font program represented in the Compact Font Format (CFF), CIDFontType0C - Type 0 CIDFont program represented in the Compact Font Format (CFF) and OpenType - OpenType® font program, as described in the OpenType Specification v.1.4",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "Subtype" in x
                and x.get("Subtype") not in ["Type1C", "CIDFontType0C", "OpenType"],
                specification="ISO_19005_3",
                test_number=7,
            ),
            # [138/400] 6.2.2 (2) : If a file's OutputIntents array contains more than one entry, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream
            ConformanceCheck(
                clause="6.2.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If a file's OutputIntents array contains more than one entry, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "OutputIntents" in x
                and isinstance(x.get("OutputIntents"), list)
                and len(x.get("OutputIntents")) > 1  # type: ignore[arg-type]
                and any(
                    [y != x.get("OutputIntents")[0] for y in x.get("OutputIntents")]  # type: ignore[index, union-attr]
                ),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [143/400] 6.2.3 (2) : If a file's OutputIntents array contains more than one entry, as might be the case where a file is compliant with this part of ISO 19005 and at the same time with PDF/X-4 or PDF/E-1, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream
            ConformanceCheck(
                clause="6.2.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="If a file's OutputIntents array contains more than one entry, as might be the case where a file is compliant with this part of ISO 19005 and at the same time with PDF / X-4 or PDF / E-1, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "OutputIntents" in x
                and isinstance(x.get("OutputIntents"), list)
                and len(x.get("OutputIntents")) > 1  # type: ignore[arg-type]
                and any(
                    [y != x.get("OutputIntents")[0] for y in x.get("OutputIntents")]  # type: ignore[index, union-attr]
                ),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [144/400] 6.2.3 (2) : If any OutputIntents array contains more than one entry, as might be the case where a file is compliant with this part of ISO 19005 and at the same time with PDF/X or PDF/E, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream
            ConformanceCheck(
                clause="6.2.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If any OutputIntents array contains more than one entry, as might be the case where a file is compliant with this part of ISO 19005 and at the same time with PDF/X or PDF/E, then all entries that contain a DestOutputProfile key shall have as the value of that key the same indirect object, which shall be a valid ICC profile stream",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "OutputIntents" in x
                and isinstance(x.get("OutputIntents"), list)
                and len(x.get("OutputIntents")) > 1  # type: ignore[arg-type]
                and any(
                    [y != x.get("OutputIntents")[0] for y in x.get("OutputIntents")]  # type: ignore[index, union-attr]
                ),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [145/400] 6.2.3 (3) : In addition, the DestOutputProfileRef key, as defined in ISO 15930-7:2010, Annex A, shall not be present in any PDF/X OutputIntent
            ConformanceCheck(
                clause="6.2.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="In addition, the DestOutputProfileRef key, as defined in ISO 15930-7:2010, Annex A, shall not be present in any PDF/X OutputIntent",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "OutputIntent"
                    and "DestOutputProfileRef" in x
                ),
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [146/400] 6.2.3 (3) : The DestOutputProfileRef key, as defined in ISO 32000-2:2020, 14.11.5, Table 401, shall not be present in any output intent dictionary
            ConformanceCheck(
                clause="6.2.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The DestOutputProfileRef key, as defined in ISO 32000-2:2020, 14.11.5, Table 401, shall not be present in any output intent dictionary",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "OutputIntent"
                    and "DestOutputProfileRef" in x
                ),
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [152/400] 6.2.4 (1) : An Image dictionary shall not contain the Alternates key
            ConformanceCheck(
                clause="6.2.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An Image dictionary shall not contain the Alternates key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Alternates" in x,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [153/400] 6.2.4 (2) : An XObject dictionary (Image or Form) shall not contain the OPI key
            ConformanceCheck(
                clause="6.2.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An XObject dictionary (Image or Form) shall not contain the OPI key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and "OPI" in x,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [154/400] 6.2.4 (3) : If an Image dictionary contains the Interpolate key, its value shall be false
            ConformanceCheck(
                clause="6.2.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If an Image dictionary contains the Interpolate key, its value shall be false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Interpolate" in x
                and x.get("Interpolate") != False,
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [155/400] 6.2.4 (4) : If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4 or 8
            ConformanceCheck(
                clause="6.2.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4 or 8",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "BitsPerComponent" in x
                and isinstance(x.get("BitsPerComponent"), int)
                and x.get("BitsPerComponent") not in [1, 2, 4, 8],
                specification="ISO_19005_1",
                test_number=4,
            ),
            # [156/400] 6.2.4 (5) : If an image mask dictionary contains the BitsPerComponent key, its value shall be 1
            ConformanceCheck(
                clause="6.2.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If an image mask dictionary contains the BitsPerComponent key, its value shall be 1",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "XObject"
                    and x.get("Subtype") == "Image"
                    and x.get("ImageMask") is True
                    and isinstance(x.get("BitsPerComponent"), int)
                    and x.get("BitsPerComponent") != 1
                ),
                specification="ISO_19005_1",
                test_number=5,
            ),
            # [171/400] 6.2.5 (1) : A form XObject dictionary shall not contain the Subtype2 key with a value of PS or the PS key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A form XObject dictionary shall not contain the Subtype2 key with a value of PS or the PS key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Form"
                and (("Subtype2" in x and x.get("Subtype2") == "PS") or "PS" in x),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [172/400] 6.2.5 (1) : An ExtGState dictionary shall not contain the TR key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="An ExtGState dictionary shall not contain the TR key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict) and x.get("Type") == "ExtGState" and "TR" in x
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [173/400] 6.2.5 (1) : A graphics state parameter dictionary (ISO 32000-2:2020, 8.4.5) shall not contain the TR key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A graphics state parameter dictionary (ISO 32000-2:2020, 8.4.5) shall not contain the TR key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict) and x.get("Type") == "ExtGState" and "TR" in x
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [174/400] 6.2.5 (2) : An ExtGState dictionary shall not contain the TR2 key with a value other than Default
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="An ExtGState dictionary shall not contain the TR2 key with a value other than Default",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "ExtGState"
                    and "TR2" in x
                    and x.get("TR2") != "Default"
                ),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [175/400] 6.2.5 (2) : A graphics state parameter dictionary shall not contain the TR2 key with a value other than Default
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A graphics state parameter dictionary shall not contain the TR2 key with a value other than Default",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "ExtGState"
                    and "TR2" in x
                    and x.get("TR2") != "Default"
                ),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [176/400] 6.2.5 (3) : An ExtGState dictionary shall not contain the HTP key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="An ExtGState dictionary shall not contain the HTP key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict) and x.get("Type") == "ExtGState" and "HTP" in x
                ),
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [177/400] 6.2.5 (3) : A graphics state parameter dictionary shall not contain the HTO key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A graphics state parameter dictionary shall not contain the HTO key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict) and x.get("Type") == "ExtGState" and "HTP" in x
                ),
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [178/400] 6.2.5 (4) : All halftones in a conforming PDF/A-2 file shall have the value 1 or 5 for the HalftoneType key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                ],
                description="All halftones in a conforming PDF/A-2 file shall have the value 1 or 5 for the HalftoneType key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (
                        isinstance(x.get("HT"), dict)
                        and x.get("HT").get("HalftoneType") not in [1, 5]  # type: ignore[union-attr]
                    )
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(
                            [y.get("HalftoneType") not in [1, 5] for y in x.get("HT")]  # type: ignore[union-attr]
                        )
                    )
                ),
                specification="ISO_19005_2",
                test_number=4,
            ),
            # [179/400] 6.2.5 (4) : All halftones in a conforming PDF/A-3 file shall have the value 1 or 5 for the HalftoneType key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All halftones in a conforming PDF/A-3 file shall have the value 1 or 5 for the HalftoneType key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (
                        isinstance(x.get("HT"), dict)
                        and x.get("HT").get("HalftoneType") not in [1, 5]  # type: ignore[union-attr]
                    )
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(
                            [y.get("HalftoneType") not in [1, 5] for y in x.get("HT")]  # type: ignore[union-attr]
                        )
                    )
                ),
                specification="ISO_19005_3",
                test_number=4,
            ),
            # [180/400] 6.2.5 (4) : All halftones in a conforming PDF/A-4 file shall have the value 1 or 5 for the HalftoneType key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All halftones in a conforming PDF/A-4 file shall have the value 1 or 5 for the HalftoneType key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (
                        isinstance(x.get("HT"), dict)
                        and x.get("HT").get("HalftoneType") not in [1, 5]  # type: ignore[union-attr]
                    )
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(
                            [y.get("HalftoneType") not in [1, 5] for y in x.get("HT")]  # type: ignore[union-attr]
                        )
                    )
                ),
                specification="ISO_19005_4",
                test_number=4,
            ),
            # [181/400] 6.2.5 (5) : Halftones in a conforming PDF/A-2 file shall not contain a HalftoneName key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                ],
                description="Halftones in a conforming PDF/A-2 file shall not contain a HalftoneName key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (isinstance(x.get("HT"), dict) and "HalftoneName" in x.get("HT"))  # type: ignore[operator, union-attr]
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(["HalftoneName" in y for y in x.get("HT")])  # type: ignore[union-attr]
                    )
                ),
                specification="ISO_19005_2",
                test_number=5,
            ),
            # [182/400] 6.2.5 (5) : Halftones in a conforming PDF/A-3 file shall not contain a HalftoneName key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="Halftones in a conforming PDF/A-3 file shall not contain a HalftoneName key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (isinstance(x.get("HT"), dict) and "HalftoneName" in x.get("HT"))  # type: ignore[operator, union-attr]
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(["HalftoneName" in y for y in x.get("HT")])  # type: ignore[union-attr]
                    )
                ),
                specification="ISO_19005_3",
                test_number=5,
            ),
            # [183/400] 6.2.5 (5) : Halftones in a conforming PDF/A-4 file shall not contain a HalftoneName key
            ConformanceCheck(
                clause="6.2.5",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="Halftones in a conforming PDF/A-4 file shall not contain a HalftoneName key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "HT" in x
                and (
                    (isinstance(x.get("HT"), dict) and "HalftoneName" in x.get("HT"))  # type: ignore[operator, union-attr]
                    or (
                        (isinstance(x.get("HT"), list))
                        and all([isinstance(y, dict) for y in x.get("HT")])  # type: ignore[union-attr]
                        and any(["HalftoneName" in y for y in x.get("HT")])  # type: ignore[union-attr]
                    )
                ),
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [188/400] 6.2.7 (1) : A conforming file shall not contain any PostScript XObjects
            ConformanceCheck(
                clause="6.2.7",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A conforming file shall not contain any PostScript XObjects",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "PostScript",
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [189/400] 6.2.7.1 (1) : An Image dictionary shall not contain the Alternates key
            ConformanceCheck(
                clause="6.2.7.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="An Image dictionary shall not contain the Alternates key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Alternates" in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [190/400] 6.2.7.1 (2) : An Image dictionary shall not contain the OPI key
            ConformanceCheck(
                clause="6.2.7.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="An Image dictionary shall not contain the OPI key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "OPI" in x,
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [191/400] 6.2.7.1 (3) : If an Image dictionary contains the Interpolate key, its value shall be false. For an inline image, the I key, if present, shall have a value of false
            ConformanceCheck(
                clause="6.2.7.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If an Image dictionary contains the Interpolate key, its value shall be false. For an inline image, the I key, if present, shall have a value of false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Interpolate" in x
                and x.get("Interpolate") != False,
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [192/400] 6.2.7.1 (4) : If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4, 8 or 16
            ConformanceCheck(
                clause="6.2.7.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4, 8 or 16",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "BitsPerComponent" in x
                and isinstance(x.get("BitsPerComponent"), int)
                and x.get("BitsPerComponent") not in [1, 2, 4, 8, 16],
                specification="ISO_19005_4",
                test_number=4,
            ),
            # [193/400] 6.2.7.1 (5) : If an image mask dictionary contains the BitsPerComponent key, its value shall be 1
            ConformanceCheck(
                clause="6.2.7.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If an image mask dictionary contains the BitsPerComponent key, its value shall be 1",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "XObject"
                    and x.get("Subtype") == "Image"
                    and x.get("ImageMask") is True
                    and isinstance(x.get("BitsPerComponent"), int)
                    and x.get("BitsPerComponent") != 1
                ),
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [194/400] 6.2.7.3 (1) : The number of colour channels in the JPEG2000 data shall be 1, 3 or 4
            ConformanceCheck(
                clause="6.2.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The number of colour channels in the JPEG2000 data shall be 1, 3 or 4",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Subtype") == "Image"
                and x.get("Filter") == "JPXDecode"
                and "Bytes" in x
                and isinstance(x.get("Bytes"), bytes)
                and ConformanceChecks.__get_channel_count_from_jpg2000_image(  # type: ignore[operator]
                    x.get("Bytes")
                )
                not in [1, 3, 4],
                specification="ISO_19005_4",
                test_number=1,
            ),
            # TODO: [195/400] 6.2.7.3 (2) : If the number of colour space specifications in the JPEG2000 data is greater than 1, there shall be exactly one colour space specification that has the value 0x01 in the APPROX field
            ConformanceCheck(
                clause="6.2.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="If the number of colour space specifications in the JPEG2000 data is greater than 1, there shall be exactly one colour space specification that has the value 0x01 in the APPROX field",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=2,
            ),
            # TODO: [196/400] 6.2.7.3 (3) : The value of the METH entry in its 'colr' box shall be 0x01, 0x02 or 0x03. A conforming processor shall use only that colour space and shall ignore all other colour space specifications
            ConformanceCheck(
                clause="6.2.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The value of the METH entry in its 'colr' box shall be 0x01, 0x02 or 0x03. A conforming processor shall use only that colour space and shall ignore all other colour space specifications",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=3,
            ),
            # TODO: [197/400] 6.2.7.3 (4) : JPEG2000 enumerated colour space 19 (CIEJab) shall not be used
            ConformanceCheck(
                clause="6.2.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="JPEG2000 enumerated colour space 19 (CIEJab) shall not be used",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=4,
            ),
            # TODO: [198/400] 6.2.7.3 (5) : The bit-depth of the JPEG2000 data shall have a value in the range 1 to 38. All colour channels in the JPEG2000 data shall have the same bit-depth
            ConformanceCheck(
                clause="6.2.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The bit-depth of the JPEG2000 data shall have a value in the range 1 to 38. All colour channels in the JPEG2000 data shall have the same bit-depth",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [199/400] 6.2.8 (1) : An ExtGState dictionary shall not contain the TR key
            ConformanceCheck(
                clause="6.2.8",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An ExtGState dictionary shall not contain the TR key",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict) and x.get("Type") == "ExtGState" and "TR" in x
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [200/400] 6.2.8 (1) : An Image dictionary shall not contain the Alternates key
            ConformanceCheck(
                clause="6.2.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="An Image dictionary shall not contain the Alternates key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Alternates" in x,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [201/400] 6.2.8 (2) : An ExtGState dictionary shall not contain the TR2 key with a value other than Default
            ConformanceCheck(
                clause="6.2.8",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An ExtGState dictionary shall not contain the TR2 key with a value other than Default",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "ExtGState"
                    and "TR2" in x
                    and x.get("TR2") != "Default"
                ),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [202/400] 6.2.8 (2) : An Image dictionary shall not contain the OPI key
            ConformanceCheck(
                clause="6.2.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="An Image dictionary shall not contain the OPI key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "OPI" in x,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [203/400] 6.2.8 (3) : If an Image dictionary contains the Interpolate key, its value shall be false. For an inline image, the I key shall have a value of false
            ConformanceCheck(
                clause="6.2.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="If an Image dictionary contains the Interpolate key, its value shall be false. For an inline image, the I key shall have a value of false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "Interpolate" in x
                and x.get("Interpolate") != False,
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [204/400] 6.2.8 (4) : If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4, 8 or 16
            ConformanceCheck(
                clause="6.2.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="If an Image dictionary contains the BitsPerComponent key, its value shall be 1, 2, 4, 8 or 16",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Image"
                and "BitsPerComponent" in x
                and isinstance(x.get("BitsPerComponent"), int)
                and x.get("BitsPerComponent") not in [1, 2, 4, 8, 16],
                specification="ISO_19005_3",
                test_number=4,
            ),
            # [205/400] 6.2.8 (5) : If an image mask dictionary contains the BitsPerComponent key, its value shall be 1
            ConformanceCheck(
                clause="6.2.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="If an image mask dictionary contains the BitsPerComponent key, its value shall be 1",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "XObject"
                    and x.get("Subtype") == "Image"
                    and x.get("ImageMask") is True
                    and isinstance(x.get("BitsPerComponent"), int)
                    and x.get("BitsPerComponent") != 1
                ),
                specification="ISO_19005_3",
                test_number=5,
            ),
            # [206/400] 6.2.8.1 (1) : A form XObject dictionary shall not contain an OPI key
            ConformanceCheck(
                clause="6.2.8.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A form XObject dictionary shall not contain an OPI key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "Form"
                and "OPI" in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [218/400] 6.2.9 (3) : A conforming file shall not contain any PostScript XObjects
            ConformanceCheck(
                clause="6.2.9",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A conforming file shall not contain any PostScript XObjects",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and x.get("Subtype") == "PostScript",
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [219/400] 6.3.1 (1) : Annotation types not defined in ISO 32000-1 shall not be permitted. Additionally, the 3D, Sound, Screen and Movie types shall not be permitted
            ConformanceCheck(
                clause="6.3.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="Annotation types not defined in ISO 32000-1 shall not be permitted. Additionally, the 3D, Sound, Screen and Movie types shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "Annot"
                    and "Subtype" in x
                    and x.get("Subtype")
                    not in [
                        "Text",
                        "Link",
                        "FreeText",
                        "Line",
                        "Square",
                        "Circle",
                        "Polygon",
                        "PolyLine",
                        "Highlight",
                        "Underline",
                        "Squiggly",
                        "StrikeOut",
                        "Stamp",
                        "Caret",
                        "Ink",
                        "Popup",
                        "FileAttachment",
                        "Widget",
                        "PrinterMark",
                        "TrapNet",
                        "Watermark",
                        "Redact",
                    ]
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [220/400] 6.3.1 (1) : Annotation types not defined in ISO 32000-2:2020, 12.5.6.1, Table 171 shall not be permitted. Additionally, the Sound, Screen, Movie and FileAttachment types shall not be permitted. 3D and RichMedia types shall only be permitted in a PDF/A-4e compliant file as described in Annex B
            ConformanceCheck(
                clause="6.3.1",
                conformance=[Conformance.PDF_A_4E],
                description="Annotation types not defined in ISO 32000-2:2020, 12.5.6.1, Table 171 shall not be permitted. Additionally, the Sound, Screen, Movie and FileAttachment types shall not be permitted. 3D and RichMedia types shall only be permitted in a PDF/A-4e compliant file as described in Annex B",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "Annot"
                    and "Subtype" in x
                    and x.get("Subtype")
                    not in [
                        "3D",
                        "Text",
                        "Link",
                        "FreeText",
                        "Line",
                        "Square",
                        "Circle",
                        "Polygon",
                        "PolyLine",
                        "Highlight",
                        "Underline",
                        "Squiggly",
                        "StrikeOut",
                        "Stamp",
                        "Caret",
                        "Ink",
                        "Popup",
                        "Widget",
                        "PrinterMark",
                        "TrapNet",
                        "Watermark",
                        "Redact",
                    ]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [221/400] 6.3.1 (1) : Annotation types not defined in ISO 32000-2:2020, 12.5.6.1, Table 171 shall not be permitted. Additionally, the Sound, Screen, Movie, 3D and RichMedia types shall not be permitted. The FileAttachment type shall only be permitted in a PDF/A-4f compliant file as described in Annex A
            ConformanceCheck(
                clause="6.3.1",
                conformance=[Conformance.PDF_A_4F],
                description="Annotation types not defined in ISO 32000-2:2020, 12.5.6.1, Table 171 shall not be permitted. Additionally, the Sound, Screen, Movie, 3D and RichMedia types shall not be permitted. The FileAttachment type shall only be permitted in a PDF/A-4f compliant file as described in Annex A",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "Annot"
                    and "Subtype" in x
                    and x.get("Subtype")
                    not in [
                        "Text",
                        "Link",
                        "FreeText",
                        "Line",
                        "Square",
                        "Circle",
                        "Polygon",
                        "PolyLine",
                        "Highlight",
                        "Underline",
                        "Squiggly",
                        "StrikeOut",
                        "Stamp",
                        "Caret",
                        "Ink",
                        "Popup",
                        "Widget",
                        "PrinterMark",
                        "TrapNet",
                        "Watermark",
                        "Redact",
                    ]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [223/400] 6.3.2 (1) : Except for annotation dictionaries whose Subtype value is Popup, all annotation dictionaries shall contain the F key
            ConformanceCheck(
                clause="6.3.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="Except for annotation dictionaries whose Subtype value is Popup, all annotation dictionaries shall contain the F key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and x.get("Subtype") != "Popup"
                and "F" in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [226/400] 6.3.2 (3) : All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. BaseFont - name - (Required) The PostScript name of the font
            ConformanceCheck(
                clause="6.3.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. BaseFont - name - (Required) The PostScript name of the font",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and x.get("Subtype") in ["Type1", "TrueType"]
                and not ConformanceChecks.__is_standard_14_font(x)
                and "BaseFont" not in x,
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [227/400] 6.3.2 (4) : All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.3.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. FirstChar - integer - (Required except for the standard 14 fonts) The first character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and x.get("Subtype") in ["Type1", "TrueType"]
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("FirstChar"), int),
                specification="ISO_19005_1",
                test_number=4,
            ),
            # [228/400] 6.3.2 (5) : All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array
            ConformanceCheck(
                clause="6.3.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. LastChar - integer - (Required except for the standard 14 fonts) The last character code defined in the font's Widths array",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and x.get("Subtype") in ["Type1", "TrueType"]
                and not ConformanceChecks.__is_standard_14_font(x)
                and not isinstance(x.get("LastChar"), int),
                specification="ISO_19005_1",
                test_number=5,
            ),
            # [229/400] 6.3.2 (6) : All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths
            ConformanceCheck(
                clause="6.3.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="All fonts used in a conforming file shall conform to the font specifications defined in PDF Reference 5.5. Widths - array - (Required except for the standard 14 fonts; indirect reference preferred) An array of (LastChar − FirstChar + 1) widths",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Font"
                and "FirstChar" in x
                and isinstance(x.get("FirstChar"), int)
                and "LastChar" in x
                and isinstance(x.get("LastChar"), int)
                and "Widths" in x
                and isinstance(x.get("Widths"), list)
                and len(x.get("Widths"))  # type: ignore[arg-type]
                != x.get("LastChar")  # type: ignore[operator]
                - x.get("FirstChar")
                + 1,  # type: ignore[arg-type, operator]
                specification="ISO_19005_1",
                test_number=6,
            ),
            # [231/400] 6.3.3 (1) : Every annotation (including those whose Subtype value is Widget, as used for form fields), except for the two cases listed below, shall have at least one appearance dictionary: - annotations where the value of the Rect key consists of an array where value 1 is equal to value 3 and value 2 is equal to value 4; - annotations whose Subtype value is Popup or Link
            ConformanceCheck(
                clause="6.3.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="Every annotation (including those whose Subtype value is Widget, as used for form fields), except for the two cases listed below, shall have at least one appearance dictionary: - annotations where the value of the Rect key consists of an array where value 1 is equal to value 3 and value 2 is equal to value 4; - annotations whose Subtype value is Popup or Link",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and not (
                    (
                        "Rect" in x
                        and isinstance(x.get("Rect"), list)
                        and len(x.get("Rect")) == 4  # type: ignore[arg-type]
                        and x.get("Rect")[0] == x.get("Rect")[2]  # type: ignore[index]
                        and x.get("Rect")[1] == x.get("Rect")[3]  # type: ignore[index]
                    )
                    or x.get("Subtype") in ["Popup", "Link"]
                )
                and "AP" not in x,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [232/400] 6.3.3 (1) : Every annotation (including those whose Subtype value is Widget, as used for form fields), except for the two cases listed below, shall have at least one appearance dictionary: Annotations where the value of the Rect key consists of an array where the value at index 1 is equal to the value at index 3 and the value at index 2 is equal to the value at index 4; - annotations whose Subtype value is Popup, Link or Projection
            ConformanceCheck(
                clause="6.3.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="Every annotation (including those whose Subtype value is Widget, as used for form fields), except for the two cases listed below, shall have at least one appearance dictionary: Annotations where the value of the Rect key consists of an array where the value at index 1 is equal to the value at index 3 and the value at index 2 is equal to the value at index 4; - annotations whose Subtype value is Popup, Link or Projection",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and not (
                    (
                        "Rect" in x
                        and isinstance(x.get("Rect"), list)
                        and len(x.get("Rect")) == 4  # type: ignore[arg-type]
                        and x.get("Rect")[0] == x.get("Rect")[2]  # type: ignore[index]
                        and x.get("Rect")[1] == x.get("Rect")[3]  # type: ignore[index]
                    )
                    or x.get("Subtype") in ["Popup", "Link", "Projection"]
                )
                and "AP" not in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [233/400] 6.3.3 (2) : For all annotation dictionaries containing an AP key, the appearance dictionary that it defines as its value shall contain only the N key
            ConformanceCheck(
                clause="6.3.3",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="For all annotation dictionaries containing an AP key, the appearance dictionary that it defines as its value shall contain only the N key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and "AP" in x
                and isinstance(x.get("AP"), dict)
                and not (len(x.get("AP")) == 1 and "N" in x.get("AP")),  # type: ignore[arg-type, operator]
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [249/400] 6.4 (1) : If an SMask key appears in an ExtGState dictionary, its value shall be None
            ConformanceCheck(
                clause="6.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If an SMask key appears in an ExtGState dictionary, its value shall be None",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "SMask" in x
                and x.get("SMask") is not None,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [250/400] 6.4 (2) : An XObject dictionary shall not contain the SMask key
            ConformanceCheck(
                clause="6.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An XObject dictionary shall not contain the SMask key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "XObject"
                and "SMask" in x,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [252/400] 6.4 (4) : If a BM key is present in an ExtGState object, its value shall be Normal or Compatible
            ConformanceCheck(
                clause="6.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If a BM key is present in an ExtGState object, its value shall be Normal or Compatible",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "BM" in x
                and x.get("BM") not in ["Normal", "Compatible"],
                specification="ISO_19005_1",
                test_number=4,
            ),
            # [253/400] 6.4 (5) : If a CA key is present in an ExtGState object, its value shall be 1.0
            ConformanceCheck(
                clause="6.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If a CA key is present in an ExtGState object, its value shall be 1.0",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "CA" in x
                and x.get("CA") != 1,
                specification="ISO_19005_1",
                test_number=5,
            ),
            # [254/400] 6.4 (6) : If a ca key is present in an ExtGState object, its value shall be 1.0
            ConformanceCheck(
                clause="6.4",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="If a ca key is present in an ExtGState object, its value shall be 1.0",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "ExtGState"
                and "ca" in x
                and x.get("ca") != 1,
                specification="ISO_19005_1",
                test_number=6,
            ),
            # [255/400] 6.4.1 (1) : A Widget annotation dictionary shall not contain the A or AA keys
            ConformanceCheck(
                clause="6.4.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A Widget annotation dictionary shall not contain the A or AA keys",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and x.get("Subtype") == "Widget"
                and ("A" in x or "AA" in x),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [256/400] 6.4.1 (1) : A Widget annotation dictionary shall not contain the A key
            ConformanceCheck(
                clause="6.4.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="A Widget annotation dictionary shall not contain the A key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and x.get("Subtype") == "Widget"
                and "A" in x,
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [257/400] 6.4.1 (2) : A Field dictionary shall not contain the A or AA keys
            ConformanceCheck(
                clause="6.4.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="A Field dictionary shall not contain the A or AA keys",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [258/400] 6.4.1 (2) : The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false
            ConformanceCheck(
                clause="6.4.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and x.get("AcroForm").get("NeedAppearances") not in [None, False],  # type: ignore[union-attr]
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [259/400] 6.4.1 (3) : The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false
            ConformanceCheck(
                clause="6.4.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and x.get("AcroForm").get("NeedAppearances") not in [None, False],  # type: ignore[operator, union-attr]
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [260/400] 6.4.2 (1) : The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-2 file, if present, shall not contain the XFA key
            ConformanceCheck(
                clause="6.4.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                ],
                description="The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-2 file, if present, shall not contain the XFA key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and "XFA" in x.get("AcroForm"),  # type: ignore[operator]
                specification="ISO_19005_2",
                test_number=1,
            ),
            # [261/400] 6.4.2 (1) : The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-3 file, if present, shall not contain the XFA key
            ConformanceCheck(
                clause="6.4.2",
                conformance=[
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-3 file, if present, shall not contain the XFA key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and "XFA" in x.get("AcroForm"),  # type: ignore[operator]
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [262/400] 6.4.2 (1) : The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-4 file, if present, shall not contain the XFA key
            ConformanceCheck(
                clause="6.4.2",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The document's interactive form dictionary that forms the value of the AcroForm key in the document's Catalog of a PDF/A-4 file, if present, shall not contain the XFA key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and "XFA" in x.get("AcroForm"),  # type: ignore[operator]
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [263/400] 6.4.2 (2) : A document's Catalog shall not contain the NeedsRendering key
            ConformanceCheck(
                clause="6.4.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="A document's Catalog shall not contain the NeedsRendering key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "NeedsRendering" in x,
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [267/400] 6.5.1 (1) : The Launch, Sound, Movie, ResetForm, ImportData, Hide, SetOCGState, Rendition, Trans, GoTo3DView and JavaScript actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted
            ConformanceCheck(
                clause="6.5.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The Launch, Sound, Movie, ResetForm, ImportData, Hide, SetOCGState, Rendition, Trans, GoTo3DView and JavaScript actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S")
                    in [
                        "Launch",
                        "Sound",
                        "Movie",
                        "ResetForm",
                        "ImportData",
                        "Hide",
                        "SetOCGState",
                        "Rendition",
                        "Trans",
                        "GoTo3DView",
                        "JavaScript",
                        "SetState",  # deprecated
                        "NoOp",  # deprecated
                    ]
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [268/400] 6.5.1 (2) : Named actions other than NextPage, PrevPage, FirstPage, and LastPage shall not be permitted
            ConformanceCheck(
                clause="6.5.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="Named actions other than NextPage, PrevPage, FirstPage, and LastPage shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S") == "Named"
                    and x.get("N")
                    not in ["NextPage", "PrevPage", "FirstPage", "LastPage"]
                ),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [269/400] 6.5.2 (1) : Annotation types not defined in PDF Reference shall not be permitted. Additionally, the FileAttachment, Sound and Movie types shall not be permitted
            ConformanceCheck(
                clause="6.5.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Annotation types not defined in PDF Reference shall not be permitted. Additionally, the FileAttachment, Sound and Movie types shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("Type") == "Annot"
                    and "Subtype" in x
                    and x.get("Subtype")
                    not in [
                        "3D",
                        "Screen",
                        "Text",
                        "Link",
                        "FreeText",
                        "Line",
                        "Square",
                        "Circle",
                        "Polygon",
                        "PolyLine",
                        "Highlight",
                        "Underline",
                        "Squiggly",
                        "StrikeOut",
                        "Stamp",
                        "Caret",
                        "Ink",
                        "Popup",
                        "FileAttachment",
                        "Widget",
                        "PrinterMark",
                        "TrapNet",
                        "Watermark",
                        "Redact",
                    ]
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [270/400] 6.5.2 (1) : The document's Catalog shall not include an AA entry for an additional-actions dictionary
            ConformanceCheck(
                clause="6.5.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The document's Catalog shall not include an AA entry for an additional-actions dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AA" in x,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [271/400] 6.5.2 (2) : The Page dictionary shall not include an AA entry for an additional-actions dictionary
            ConformanceCheck(
                clause="6.5.2",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The Page dictionary shall not include an AA entry for an additional-actions dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Page"
                and "AA" in x,
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [272/400] 6.5.3 (1) : An annotation dictionary shall not contain the CA key with a value other than 1.0
            ConformanceCheck(
                clause="6.5.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="An annotation dictionary shall not contain the CA key with a value other than 1.0",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and "CA" in x
                and x.get("CA") != 1.0,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [275/400] 6.5.3 (4) : For all annotation dictionaries containing an AP key, the appearance dictionary that it defines as its value shall contain only the N key
            ConformanceCheck(
                clause="6.5.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="For all annotation dictionaries containing an AP key, the appearance dictionary that it defines as its value shall contain only the N key",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and "AP" in x
                and isinstance(x.get("AP"), dict)
                and not (len(x.get("AP")) == 1 and "N" in x.get("AP")),  # type: ignore[arg-type, operator]
                specification="ISO_19005_1",
                test_number=4,
            ),
            # [278/400] 6.6.1 (1) : The Launch, Sound, Movie, ResetForm, ImportData and JavaScript actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted. The Hide action shall not be permitted (Corrigendum 2)
            ConformanceCheck(
                clause="6.6.1",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The Launch, Sound, Movie, ResetForm, ImportData and JavaScript actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted. The Hide action shall not be permitted (Corrigendum 2)",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S")
                    in [
                        "Launch",
                        "Sound",
                        "Movie",
                        "ResetForm",
                        "ImportData",
                        "JavaScript",
                        "SetState",  # deprecated
                        "NoOp",  # deprecated
                        "Hide",
                    ]
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [279/400] 6.6.1 (1) : The Launch, Sound, Movie, ResetForm, ImportData, Hide, Rendition and Trans actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted. The SetOCGState and GoTo3DView actions shall only be permitted in a PDF/A-4e compliant file as described in Annex B
            ConformanceCheck(
                clause="6.6.1",
                conformance=[Conformance.PDF_A_4E],
                description="The Launch, Sound, Movie, ResetForm, ImportData, Hide, Rendition and Trans actions shall not be permitted. Additionally, the deprecated set-state and no-op actions shall not be permitted. The SetOCGState and GoTo3DView actions shall only be permitted in a PDF/A-4e compliant file as described in Annex B",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S")
                    in [
                        "Launch",
                        "Sound",
                        "Movie",
                        "ResetForm",
                        "ImportData",
                        "Hide",
                        "Rendition",
                        "Trans",
                        "SetState",  # deprecated
                        "NoOp",  # deprecated
                    ]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [280/400] 6.6.1 (1) : The Launch, Sound, Movie, ResetForm, ImportData, Hide, Rendition, Trans, SetOCGState and GoTo3DView actions shall not be permitted. Additionally, the obsoleted set-state and no-op actions shall not be permitted
            ConformanceCheck(
                clause="6.6.1",
                conformance=[Conformance.PDF_A_4F],
                description="The Launch, Sound, Movie, ResetForm, ImportData, Hide, Rendition, Trans, SetOCGState and GoTo3DView actions shall not be permitted. Additionally, the obsoleted set-state and no-op actions shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S")
                    in [
                        "Launch",
                        "Sound",
                        "Movie",
                        "ResetForm",
                        "ImportData",
                        "Hide",
                        "Rendition",
                        "Trans",
                        "SetOCGState",
                        "GoTo3DView",
                        "SetState",  # deprecated
                        "NoOp",  # deprecated
                    ]
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [281/400] 6.6.1 (2) : Named actions other than NextPage, PrevPage, FirstPage, and LastPage shall not be permitted
            ConformanceCheck(
                clause="6.6.1",
                conformance=[
                    Conformance.PDF_A_1A,
                    Conformance.PDF_A_1B,
                    Conformance.PDF_A_4E,
                    Conformance.PDF_A_4F,
                ],
                description="Named actions other than NextPage, PrevPage, FirstPage, and LastPage shall not be permitted",
                lambda_function_to_check_object=lambda x: (
                    isinstance(x, dict)
                    and x.get("S") == "Named"
                    and x.get("N")
                    not in ["NextPage", "PrevPage", "FirstPage", "LastPage"]
                ),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [283/400] 6.6.2 (1) : A Widget annotation dictionary shall not include an AA entry for an additional-actions dictionary
            ConformanceCheck(
                clause="6.6.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A Widget annotation dictionary shall not include an AA entry for an additional-actions dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Annot"
                and x.get("Subtype") == "Widget"
                and "AA" in x,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [284/400] 6.6.2 (2) : A Field dictionary shall not include an AA entry for an additional-actions dictionary
            ConformanceCheck(
                clause="6.6.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="A Field dictionary shall not include an AA entry for an additional-actions dictionary",
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [285/400] 6.6.2 (3) : The document catalog dictionary shall not include an AA entry for an additional-actions dictionary
            ConformanceCheck(
                clause="6.6.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The document catalog dictionary shall not include an AA entry for an additional-actions dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AA" in x,
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [286/400] 6.6.2.1 (1) : The Catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-1:2008, 14.3.2. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML
            ConformanceCheck(
                clause="6.6.2.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The Catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-1:2008, 14.3.2. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and not (
                    "Metadata" in x
                    and isinstance(x.get("Metadata"), stream)
                    and x.get("Metadata").get("Type") == "Metadata"  # type: ignore[union-attr]
                    and x.get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [287/400] 6.6.2.1 (2) : The bytes attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.6.2.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The bytes attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_bytes_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [288/400] 6.6.2.1 (3) : The encoding attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.6.2.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The encoding attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_encoding_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_3",
                test_number=3,
            ),
            # [289/400] 6.6.2.1 (4) : All metadata streams present in the PDF shall conform to the XMP Specification. All content of all XMP packets shall be well-formed, as defined by Extensible Markup Language (XML) 1.0 (Third Edition), 2.1, and the RDF/XML Syntax Specification (Revised)
            ConformanceCheck(
                clause="6.6.2.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All metadata streams present in the PDF shall conform to the XMP Specification. All content of all XMP packets shall be well-formed, as defined by Extensible Markup Language (XML) 1.0 (Third Edition), 2.1, and the RDF/XML Syntax Specification (Revised)",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_3",
                test_number=4,
            ),
            # [290/400] 6.6.2.1 (5) : All metadata streams present in the PDF shall conform to the XMP Specification. The XMP package must be encoded as UTF-8
            ConformanceCheck(
                clause="6.6.2.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All metadata streams present in the PDF shall conform to the XMP Specification. The XMP package must be encoded as UTF-8",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_3",
                test_number=5,
            ),
            # [291/400] 6.6.2.3.1 (1) : All properties specified in XMP form shall use either the predefined schemas defined in the XMP Specification, ISO 19005-1 or this part of ISO 19005, or any extension schemas that comply with 6.6.2.3.2
            ConformanceCheck(
                clause="6.6.2.3.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All properties specified in XMP form shall use either the predefined schemas defined in the XMP Specification, ISO 19005-1 or this part of ISO 19005, or any extension schemas that comply with 6.6.2.3.2",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [292/400] 6.6.2.3.1 (2) : All properties specified in XMP form shall use either the predefined schemas defined in the XMP Specification, ISO 19005-1 or this part of ISO 19005, or any extension schemas that comply with 6.6.2.3.2
            ConformanceCheck(
                clause="6.6.2.3.1",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="All properties specified in XMP form shall use either the predefined schemas defined in the XMP Specification, ISO 19005-1 or this part of ISO 19005, or any extension schemas that comply with 6.6.2.3.2",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [322/400] 6.7.11 (2) : The value of "pdfaid:part" shall be the part number of ISO 19005 to which the file conforms
            ConformanceCheck(
                clause="6.7.11",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of "pdfaid:part" shall be the part number of ISO 19005 to which the file conforms',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_part_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "1",
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [323/400] 6.7.11 (3) : A Level A conforming file shall specify the value of "pdfaid:conformance" as A
            ConformanceCheck(
                clause="6.7.11",
                conformance=[Conformance.PDF_A_1A],
                description='A Level A conforming file shall specify the value of "pdfaid:conformance" as A',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_conformance_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "A",
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [324/400] 6.7.11 (3) : A Level A conforming file shall specify the value of "pdfaid:conformance" as A. A Level B conforming file shall specify the value of "pdfaid:conformance" as B
            ConformanceCheck(
                clause="6.7.11",
                conformance=[Conformance.PDF_A_1B],
                description='A Level A conforming file shall specify the value of "pdfaid:conformance" as A. A Level B conforming file shall specify the value of "pdfaid:conformance" as B',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_conformance_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "B",
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [328/400] 6.7.2 (1) : The document catalog dictionary of a conforming file shall contain the Metadata key. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML
            ConformanceCheck(
                clause="6.7.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The document catalog dictionary of a conforming file shall contain the Metadata key. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and not (
                    "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                    and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                    and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                    == "Metadata"
                    and x.get("Trailer").get("Root").get("Metadata").get("Subtype")  # type: ignore[union-attr]
                    == "XML"
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [329/400] 6.7.2 (2) : The Metadata object stream dictionary in the document’s catalog shall not contain the Filter key
            ConformanceCheck(
                clause="6.7.2",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The Metadata object stream dictionary in the document’s catalog shall not contain the Filter key",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Filter" in x.get("Trailer").get("Root").get("Metadata"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [330/400] 6.7.2.1 (1) : The document catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-2:2020, 14.3.2. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML
            ConformanceCheck(
                clause="6.7.2.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The document catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-2:2020, 14.3.2. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and not (
                    "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                    and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                    and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                    == "Metadata"
                    and x.get("Trailer").get("Root").get("Metadata").get("Subtype")  # type: ignore[union-attr]
                    == "XML"
                ),
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [331/400] 6.7.2.1 (2) : The bytes attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.7.2.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The bytes attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_encoding_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [332/400] 6.7.2.1 (3) : The encoding attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.7.2.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The encoding attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_encoding_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [333/400] 6.7.2.1 (4) : All content of all XMP packets located in any metadata stream present in the PDF shall be well-formed as defined by XMP (ISO 16684-1)
            ConformanceCheck(
                clause="6.7.2.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All content of all XMP packets located in any metadata stream present in the PDF shall be well-formed as defined by XMP (ISO 16684-1)",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_4",
                test_number=4,
            ),
            # [334/400] 6.7.2.1 (5) : All metadata streams present in the PDF shall conform to the XMP Specification. The XMP package must be encoded as UTF-8
            ConformanceCheck(
                clause="6.7.2.1",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="All metadata streams present in the PDF shall conform to the XMP Specification. The XMP package must be encoded as UTF-8",
                lambda_function_to_check_object=lambda x: isinstance(x, stream)
                and x.get("Type") == "Metadata"
                and x.get("Subtype") == "XML"
                and not ConformanceChecks.__is_valid_xml(x.get("Bytes")),
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [335/400] 6.7.2.2 (1) : The document catalog dictionary shall include a MarkInfo dictionary containing an entry, Marked, whose value shall be true
            ConformanceCheck(
                clause="6.7.2.2",
                conformance=[Conformance.PDF_A_2A, Conformance.PDF_A_3A],
                description="The document catalog dictionary shall include a MarkInfo dictionary containing an entry, Marked, whose value shall be true",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and not (
                    "MarkInfo" in x
                    and isinstance(x.get("MarkInfo"), dict)
                    and "Marked" in x.get("MarkInfo")  # type: ignore[operator]
                    and x.get("MarkInfo").get("Marked") == True  # type: ignore[union-attr]
                ),
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [336/400] 6.7.3 (1) : The value of CreationDate entry from the document information dictionary, if present, and its analogous XMP property "xmp:CreateDate" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of CreationDate entry from the document information dictionary, if present, and its analogous XMP property "xmp:CreateDate" shall be equivalent',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "CreationDate" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and isinstance(
                    x.get("Trailer").get("Info").get("CreationDate"), datestr  # type: ignore[union-attr]
                )
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_creation_date_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("CreationDate").to_datetime(),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [338/400] 6.7.3 (2) : The value of Title entry from the document information dictionary, if present, and its analogous XMP property "dc:title['x-default']" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The value of Title entry from the document information dictionary, if present, and its analogous XMP property \"dc:title['x - default']\" shall be equivalent",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Title" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_title_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Title"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [339/400] 6.7.3 (2) : The value of "pdfaid:part" shall be the part number of ISO 19005 to which the file conforms
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='The value of "pdfaid:part" shall be the part number of ISO 19005 to which the file conforms',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_part_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "4",
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [340/400] 6.7.3 (3) : The value of Author entry from the document information dictionary, if present, and its analogous XMP property "dc:creator" shall be equivalent. dc:creator shall contain exactly one entry
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of Author entry from the document information dictionary, if present, and its analogous XMP property "dc:creator" shall be equivalent. dc:creator shall contain exactly one entry',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Author" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_author_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Author"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=3,
            ),
            # [341/400] 6.7.3 (3) : A PDF/A-4e conforming file (as described in Annex B) shall specify the value of "pdfaid:conformance" as E
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4E],
                description='A PDF/A-4e conforming file (as described in Annex B) shall specify the value of "pdfaid:conformance" as E',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_conformance_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "E",
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [342/400] 6.7.3 (3) : A PDF/A-4f conforming file (as described in Annex A) shall specify the value of "pdfaid:conformance" as F
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4F],
                description='A PDF/A-4f conforming file (as described in Annex A) shall specify the value of "pdfaid:conformance" as F',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_conformance_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != "F",
                specification="ISO_19005_4",
                test_number=3,
            ),
            # [343/400] 6.7.3 (4) : The value of Subject entry from the document information dictionary, if present, and its analogous XMP property "dc:description['x-default']" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The value of Subject entry from the document information dictionary, if present, and its analogous XMP property \"dc:description['x - default']\" shall be equivalent",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Subject" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_subject_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Subject"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=4,
            ),
            # TODO
            # TODO
            # TODO
            # [344/400] 6.7.3 (4) : Property "part" of the PDF/A Identification Schema shall have namespace prefix "pdfaid"
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='Property "part" of the PDF/A Identification Schema shall have namespace prefix "pdfaid"',
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=4,
            ),
            # [345/400] 6.7.3 (5) : The value of Keywords entry from the document information dictionary, if present, and its analogous XMP property "pdf:Keywords" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of Keywords entry from the document information dictionary, if present, and its analogous XMP property "pdf:Keywords" shall be equivalent',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Keywords" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_keywords_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Keywords"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=5,
            ),
            # [346/400] 6.7.3 (5) : The value of "pdfaid:rev" shall be the four digit year
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='The value of "pdfaid:rev" shall be the four digit year',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_pdfaid_revision_year(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                is not None,
                specification="ISO_19005_4",
                test_number=5,
            ),
            # [347/400] 6.7.3 (6) : The value of Creator entry from the document information dictionary, if present, and its analogous XMP property "xmp:CreatorTool" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of Creator entry from the document information dictionary, if present, and its analogous XMP property "xmp:CreatorTool" shall be equivalent',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Creator" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_creator_tool_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Creator"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=6,
            ),
            # [348/400] 6.7.3 (6) : Property "rev" of the PDF/A Identification Schema shall have namespace prefix "pdfaid"
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='Property "rev" of the PDF/A Identification Schema shall have namespace prefix "pdfaid"',
                lambda_function_to_check_object=lambda x: False,
                specification="ISO_19005_4",
                test_number=6,
            ),
            # [349/400] 6.7.3 (7) : The value of Producer entry from the document information dictionary, if present, and its analogous XMP property "pdf:Producer" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of Producer entry from the document information dictionary, if present, and its analogous XMP property "pdf:Producer" shall be equivalent',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "Producer" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_producer_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("Producer"),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=7,
            ),
            # [350/400] 6.7.3 (8) : The value of ModDate entry from the document information dictionary, if present, and its analogous XMP property "xmp:ModifyDate" shall be equivalent
            ConformanceCheck(
                clause="6.7.3",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description='The value of ModDate entry from the document information dictionary, if present, and its analogous XMP property "xmp:ModifyDate" shall be equivalent',
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Info" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Info"), dict)  # type: ignore[union-attr]
                and "ModDate" in x.get("Trailer").get("Info")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Info").get("ModDate"), datestr)  # type: ignore[union-attr]
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__get_modification_date_from_xmp(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                )
                != x.get("Trailer").get("Info").get("ModDate").to_datetime(),  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=8,
            ),
            # [351/400] 6.7.3.3 (1) : The logical structure of the conforming file shall be described by a structure hierarchy rooted in the StructTreeRoot entry of the document's Catalog dictionary, as described in ISO 32000-1:2008, 14.7
            ConformanceCheck(
                clause="6.7.3.3",
                conformance=[Conformance.PDF_A_2A, Conformance.PDF_A_3A],
                description="The logical structure of the conforming file shall be described by a structure hierarchy rooted in the StructTreeRoot entry of the document's Catalog dictionary, as described in ISO 32000 - 1: 2008, 14.7",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "StructTreeRoot" not in x,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [355/400] 6.7.4 (1) : If the Lang entry is present in the document's Catalog dictionary or in a structure element dictionary or property list, its value shall be a language identifier as described in ISO 32000-1:2008, 14.9.2. A language identifier shall either be the empty text string, to indicate that the language is unknown, or a Language-Tag as defined in RFC 3066, Tags for the Identification of Languages
            ConformanceCheck(
                clause="6.7.4",
                conformance=[Conformance.PDF_A_2A, Conformance.PDF_A_3A],
                description="If the Lang entry is present in the document's Catalog dictionary or in a structure element dictionary or property list, its value shall be a language identifier as described in ISO 32000 - 1: 2008, 14.9.2. A language identifier shall either be the empty text string, to indicate that the language is unknown, or a Language - Tag as defined in RFC3066, Tags for the Identification of Languages",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "Lang" in x
                and isinstance(x.get("Lang"), str)
                and re.match(r"^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*$", x.get("Lang"))  # type: ignore[arg-type]
                is None,
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [356/400] 6.7.5 (1) : The bytes attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.7.5",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The bytes attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_bytes_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [357/400] 6.7.5 (2) : The encoding attribute shall not be used in the header of an XMP packet
            ConformanceCheck(
                clause="6.7.5",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The encoding attribute shall not be used in the header of an XMP packet",
                lambda_function_to_check_object=lambda x: isinstance(x, Document)
                and "Trailer" in x
                and isinstance(x.get("Trailer"), dict)
                and "Root" in x.get("Trailer")  # type: ignore[operator]
                and isinstance(x.get("Trailer").get("Root"), dict)  # type: ignore[union-attr]
                and "Metadata" in x.get("Trailer").get("Root")  # type: ignore[union-attr]
                and isinstance(x.get("Trailer").get("Root").get("Metadata"), stream)  # type: ignore[union-attr]
                and x.get("Trailer").get("Root").get("Metadata").get("Type")  # type: ignore[union-attr]
                == "Metadata"
                and x.get("Trailer").get("Root").get("Metadata").get("Subtype") == "XML"  # type: ignore[union-attr]
                and "Bytes" in x.get("Trailer").get("Root").get("Metadata")  # type: ignore[union-attr]
                and ConformanceChecks.__xmp_has_forbidden_encoding_attribute(
                    x.get("Trailer")  # type: ignore[union-attr]
                    .get("Root")
                    .get("Metadata")
                    .get("Bytes")
                    .decode("utf8")
                ),
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [380/400] 6.8 (1) : The MIME type of an embedded file, or a subset of a file, shall be specified using the Subtype key of the file specification dictionary. If the MIME type is not known, the "application/octet-stream" shall be used
            ConformanceCheck(
                clause="6.8",
                conformance=[
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description='The MIME type of an embedded file, or a subset of a file, shall be specified using the Subtype key of the file specification dictionary. If the MIME type is not known, the "application/octet-stream" shall be used',
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Filespec"
                and x.get("Subtype")
                in [
                    "application/pdf",
                    "application/xml",
                    "application/json",
                    "application/zip",
                    "application/octet-stream",
                    "image/png",
                    "image/jpeg",
                    "image/tiff",
                    "text/plain",
                    "text/html",
                ],
                specification="ISO_19005_3",
                test_number=1,
            ),
            # [381/400] 6.8 (2) : The file specification dictionary for an embedded file shall contain the F and UF keys
            ConformanceCheck(
                clause="6.8",
                conformance=[
                    Conformance.PDF_A_2A,
                    Conformance.PDF_A_2B,
                    Conformance.PDF_A_2U,
                    Conformance.PDF_A_3A,
                    Conformance.PDF_A_3B,
                    Conformance.PDF_A_3U,
                ],
                description="The file specification dictionary for an embedded file shall contain the F and UF keys",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Filespec"
                and ("F" not in x or "UF" not in x),
                specification="ISO_19005_3",
                test_number=2,
            ),
            # [385/400] 6.8.2.2 (1) : The document catalog dictionary shall include a MarkInfo dictionary with a Marked entry in it, whose value shall be true
            ConformanceCheck(
                clause="6.8.2.2",
                conformance=[Conformance.PDF_A_1A],
                description="The document catalog dictionary shall include a MarkInfo dictionary with a Marked entry in it, whose value shall be true",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and not (
                    "MarkInfo" in x
                    and isinstance(x.get("MarkInfo"), dict)
                    and "Marked" in x.get("MarkInfo")  # type: ignore[operator]
                    and x.get("MarkInfo").get("Marked") == True  # type: ignore[union-attr]
                ),
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [386/400] 6.8.3.3 (1) : The logical structure of the conforming file shall be described by a structure hierarchy rooted in the StructTreeRoot entry of the document catalog dictionary, as described in PDF Reference 9.6
            ConformanceCheck(
                clause="6.8.3.3",
                conformance=[Conformance.PDF_A_1A],
                description="The logical structure of the conforming file shall be described by a structure hierarchy rooted in the StructTreeRoot entry of the document catalog dictionary, as described in PDF Reference 9.6",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "StructTreeRoot" not in x,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [389/400] 6.8.4 (1) : If the Lang entry is present in the document catalog dictionary or in a structure element dictionary or property list, its value shall be a language identifier as defined by RFC 1766, Tags for the Identification of Languages, as described in PDF Reference 9.8.1
            ConformanceCheck(
                clause="6.8.4",
                conformance=[Conformance.PDF_A_1A],
                description="If the Lang entry is present in the document catalog dictionary or in a structure element dictionary or property list, its value shall be a language identifier as defined by RFC 1766, Tags for the Identification of Languages, as described in PDF Reference 9.8.1",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "Lang" in x
                and isinstance(x.get("Lang"), str)
                and re.match(
                    r"^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*$", x.get("Lang")  # type: ignore[arg-type]
                )  # type: ignore[arg-type]
                is None,
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [390/400] 6.9 (1) : The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false
            ConformanceCheck(
                clause="6.9",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="The NeedAppearances flag of the interactive form dictionary shall either not be present or shall be false",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "AcroForm" in x
                and isinstance(x.get("AcroForm"), dict)
                and x.get("AcroForm").get("NeedAppearances") not in [None, False],  # type: ignore[union-attr]
                specification="ISO_19005_1",
                test_number=1,
            ),
            # [392/400] 6.9 (1) : The embedded file stream dictionary shall include a valid MIME type value for the Subtype key. If the MIME type is not known, the value "application/octet-stream" shall be used
            ConformanceCheck(
                clause="6.9",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description='The embedded file stream dictionary shall include a valid MIME type value for the Subtype key. If the MIME type is not known, the value "application/octet-stream" shall be used',
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Filespec"
                and x.get("Subtype")
                in [
                    "application/pdf",
                    "application/xml",
                    "application/json",
                    "application/zip",
                    "application/octet-stream",
                    "image/png",
                    "image/jpeg",
                    "image/tiff",
                    "text/plain",
                    "text/html",
                ],
                specification="ISO_19005_4",
                test_number=1,
            ),
            # [393/400] 6.9 (2) : Every form field shall have an appearance dictionary associated with the field's data
            ConformanceCheck(
                clause="6.9",
                conformance=[Conformance.PDF_A_1A, Conformance.PDF_A_1B],
                description="Every form field shall have an appearance dictionary associated with the field's data",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Subtype") == "Widget"
                and "AP" not in x,
                specification="ISO_19005_1",
                test_number=2,
            ),
            # [396/400] 6.9 (2) : The file specification dictionary for an embedded file shall contain the F and UF keys
            ConformanceCheck(
                clause="6.9",
                conformance=[Conformance.PDF_A_4E, Conformance.PDF_A_4F],
                description="The file specification dictionary for an embedded file shall contain the F and UF keys",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Filespec"
                and ("F" not in x or "UF" not in x),
                specification="ISO_19005_4",
                test_number=2,
            ),
            # [400/400] 6.9 (5) : A PDF/A-4f conforming file shall contain an EmbeddedFiles key in the name dictionary of the document catalog dictionary
            ConformanceCheck(
                clause="6.9",
                conformance=[Conformance.PDF_A_4F],
                description="A PDF/A-4f conforming file shall contain an EmbeddedFiles key in the name dictionary of the document catalog dictionary",
                lambda_function_to_check_object=lambda x: isinstance(x, dict)
                and x.get("Type") == "Catalog"
                and "Names" in x
                and isinstance(x.get("Names"), dict)
                and not "EmbeddedFiles" in x.get("Names"),  # type: ignore[operator]
                specification="ISO_19005_4",
                test_number=5,
            ),
        ]
