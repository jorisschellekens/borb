import datetime
import json
import logging
import os
import sys
import typing
import unittest
from _decimal import Decimal
from pathlib import Path

from PIL import Image as PILImage

from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Paragraph
from borb.pdf.canvas.layout.layout_element import LayoutElement

logger = logging.getLogger(__file__)


class TestCase(unittest.TestCase):
    def get_artifacts_directory(self, mkdir_if_not_exists: bool = True) -> Path:

        # <parent>
        inherited_test_file: Path = Path(
            sys.modules[self.__class__.__module__].__file__
        )
        parent_dir: Path = inherited_test_file.parent

        # <parent> / "artifacts_" <name>
        artifacts_dir: Path = parent_dir / ("artifacts_" + inherited_test_file.stem)
        if not artifacts_dir.exists() and mkdir_if_not_exists:
            artifacts_dir.mkdir()

        # return
        return artifacts_dir

    def get_first_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_001.pdf"

    def get_second_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_002.pdf"

    def get_third_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_003.pdf"

    def get_fourth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_004.pdf"

    def get_fifth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_005.pdf"

    def get_sixth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_006.pdf"

    def get_seventh_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_007.pdf"

    def get_eight_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_008.pdf"

    def get_nineth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_009.pdf"

    def get_tenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_010.pdf"

    def get_eleventh_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_011.pdf"

    def get_twelfth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_012.pdf"

    def get_thirteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_013.pdf"

    def get_fourteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_014.pdf"

    def get_fifteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_015.pdf"

    def get_sixteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_016.pdf"

    def get_seventeenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_017.pdf"

    def get_eighteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_018.pdf"

    def get_nineteenth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_019.pdf"

    def get_twentieth_output_file(self) -> Path:
        return self.get_artifacts_directory() / "output_020.pdf"

    def get_umpteenth_output_file(self, nr: int) -> Path:
        return self.get_artifacts_directory() / f"output_{nr:02d}.pdf"

    @staticmethod
    def _trim_text(s: str, n: int = 38) -> str:
        if len(s) < n:
            return s
        return s[0 : (n - 4) // 2] + " .. " + s[-((n - 4) // 2) :]

    def get_test_header(
        self, test_description: str = "", font_size: Decimal = Decimal(12)
    ) -> LayoutElement:

        # determine __file__ from calling code
        inherited_test_file: Path = Path(
            sys.modules[self.__class__.__module__].__file__
        )

        # return
        return (
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold", font_size=font_size))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                    font_size=font_size,
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold", font_size=font_size))
            .add(
                Paragraph(
                    TestCase._trim_text(inherited_test_file.stem), font_size=font_size
                )
            )
            .add(Paragraph("Description", font="Helvetica-Bold", font_size=font_size))
            .add(Paragraph(test_description, font_size=font_size))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

    def compare_visually_to_ground_truth(
        self,
        pdf_path: Path,
        maximum_normalized_difference: float = 0.0006,
    ) -> None:
        assert pdf_path.exists()
        assert 0 <= maximum_normalized_difference <= 1

        # execute GhostScript (to convert PDF to PNG)
        png_path_001: Path = pdf_path.parent / pdf_path.name.replace(".pdf", ".png")
        command: str = 'gs -dNOPAUSE -dBATCH -sDEVICE=png16m -sOutputFile="%s" %s' % (
            png_path_001,
            pdf_path,
        )
        os.system(command)

        # if ground_truth is present, compare
        png_path_002: Path = png_path_001.parent / png_path_001.name.replace(
            ".png", "_ground_truth.png"
        )
        if not png_path_002.exists():
            return

        # load both images
        im1 = PILImage.open(png_path_001)
        im2 = PILImage.open(png_path_002)

        # compare images (excluding regions that may change)
        W: int = min(im1.width, im2.width)
        H: int = min(im1.height, im2.height)
        progress_raw: float = 0
        prev_progress_int: int = 0
        diff: float = 0
        for i in range(0, W):
            for j in range(0, H):
                p1 = im1.getpixel((i, j))
                p2 = im2.getpixel((i, j))
                progress_raw += 1.0 / (W * H)
                progress_int = int(progress_raw * 100)

                # display progress
                if progress_int != prev_progress_int:
                    print("comparing visually: %d%% complete" % progress_int)
                    prev_progress_int = progress_int

                # green screen
                if p2 == (0, 255, 0):
                    continue

                # count differences
                d: float = (
                    (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
                ) / 195075
                if d > 0.01:
                    diff += 1

        # normalize diff
        diff /= W * H

        # delete output file
        if diff <= maximum_normalized_difference:
            os.remove(png_path_001)

        # assert
        assert (
            diff <= maximum_normalized_difference
        ), "Visual difference (%f) exceeds tolerance (%f)!" % (
            diff,
            maximum_normalized_difference,
        )

    def check_pdf_using_validator(
        self,
        pdf_path: Path,
        path_to_datalogics_executable: typing.Optional[Path] = None,
        path_to_datalogics_checker_profile: typing.Optional[Path] = None,
        keep_report_if_no_errors: bool = False,
    ) -> None:
        """
        This method checks the syntax of a given PDF using the Datalogics command line pdfchecker utility
        :param pdf_path:                            path to the PDF
        :param path_to_datalogics_executable:       path to the datalogics executable
        :param path_to_datalogics_checker_profile:  path to the checker profile (default ISO32000)
        :param keep_report_if_no_errors:            whether to keep the JSON report if there are no errors (default false)
        :return:                                    None
        """
        assert pdf_path.exists()
        if path_to_datalogics_executable is None:
            # fmt: off
            path_to_datalogics_executable = Path("/home/joris/Downloads/PDF-CHECKER-Lin64/PDF_Checker/pdfchecker")
            path_to_datalogics_checker_profile = (path_to_datalogics_executable.parent / "CheckerProfiles") / "iso_32000.json"
            # fmt: on
        if not path_to_datalogics_executable.exists():
            logger.debug("Missing path to datalogics executable, aborting check.")
            return
        if not path_to_datalogics_checker_profile.exists():
            logger.debug("Missing path to datalogics checker profile, aborting check")
            return

        # build path to json output
        json_output_path = pdf_path.parent / pdf_path.name.replace(
            ".pdf", "_validation.json"
        )

        # execute command
        command: str = '%s -j "%s" -i "%s" -s "%s"' % (
            path_to_datalogics_executable,
            path_to_datalogics_checker_profile,
            pdf_path,
            json_output_path,
        )
        os.system(command)

        # open json
        with open(json_output_path, "r") as json_file_handle:
            json_report = json.loads(json_file_handle.read())

        # get errors
        errors = json_report["analysis-summary"]["errors"]
        if len(errors) == 0 and not keep_report_if_no_errors:
            os.remove(json_output_path)

        # assert
        assert len(errors) == 0, "PDF %s has some errors: %s" % (
            pdf_path.name,
            str(errors),
        )
