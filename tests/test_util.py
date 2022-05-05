import json
import logging
import os
import typing
from pathlib import Path

from PIL import Image as PILImage

logger = logging.getLogger(__name__)


def compare_visually_to_ground_truth(
    pdf_path: Path, maximum_normalized_difference: float = 0.004
) -> object:

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
        return None

    # load both images
    im1 = PILImage.open(png_path_001)
    im2 = PILImage.open(png_path_002)

    # compare images (excluding regions that may change)
    W: int = min(im1.width, im2.width)
    H: int = min(im1.height, im2.height)
    progress_raw: float = 0
    prev_percentage_displayed: int = 0
    diff: float = 0
    for i in range(0, W):
        for j in range(0, H):
            p1 = im1.getpixel((i, j))
            p2 = im2.getpixel((i, j))
            progress_raw += 1.0 / (W * H)
            progress_int = int(progress_raw * 100)

            # display progress
            if progress_int != prev_percentage_displayed:
                print(
                    "compare_visually_to_ground_truth %s %d"
                    % (pdf_path.name, progress_int)
                )
                prev_percentage_displayed = progress_int

            # green screen
            if p2 == (0, 255, 0):
                continue

            # count differences
            d: float = (
                (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
            ) / 195075
            if d > 0.01:
                diff += 1

    # delete output file
    os.remove(png_path_001)

    # normalize diff
    diff /= W * H

    # assert
    assert (
        diff <= maximum_normalized_difference
    ), "Visual difference (%f) exceeds tolerance (%f)!" % (
        diff,
        maximum_normalized_difference,
    )


def check_pdf_using_validator(
    pdf_path: Path,
    path_to_datalogics_executable: typing.Optional[Path] = None,
    path_to_datalogics_checker_profile: typing.Optional[Path] = None,
    keep_report_if_no_errors: bool = False,
):
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
    assert len(errors) == 0, "PDF %s has some errors: %s" % (pdf_path.name, str(errors))
