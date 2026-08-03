#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility class for visual regression testing of PDFs and images.

This class provides static methods to compare rendered PDF files
and image files by converting them into PNGs (if necessary) and
computing pixel-wise differences. The comparison is parallelized
across multiple threads for efficiency.

Typical responsibilities include:

* Converting PDF files to PNG images using Ghostscript.
* Loading and resizing images to a fixed resolution for consistent
  comparisons.
* Splitting the pixel grid into column ranges and comparing them
  across threads to compute average differences.
* Providing an assertion-like ``assert_equals`` method that returns
  a floating-point similarity score between two inputs.

The ``VisualAssert`` class is primarily intended for automated
testing, ensuring that generated PDFs visually match expected
output (ground truth). It supports both direct image-to-image and
PDF-to-PDF comparisons.
"""

import datetime
import os
import pathlib
import subprocess
import threading
import typing
from subprocess import CompletedProcess

from PIL import Image  # type: ignore[import-not-found]


class VisualAssert:
    """Utility class for visual regression testing of PDFs and images.

    This class provides static methods to compare rendered PDF files
    and image files by converting them into PNGs (if necessary) and
    computing pixel-wise differences. The comparison is parallelized
    across multiple threads for efficiency.

    Typical responsibilities include:

    * Converting PDF files to PNG images using Ghostscript.
    * Loading and resizing images to a fixed resolution for consistent
      comparisons.
    * Splitting the pixel grid into column ranges and comparing them
      across threads to compute average differences.
    * Providing an assertion-like ``assert_equals`` method that returns
      a floating-point similarity score between two inputs.

    The ``VisualAssert`` class is primarily intended for automated
    testing, ensuring that generated PDFs visually match expected
    output (ground truth). It supports both direct image-to-image and
    PDF-to-PDF comparisons.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __compare_in_thread(
        from_col: int,
        image_0: Image.Image,
        image_1: Image.Image,
        results_per_thread: typing.List[float],
        thread_index: int,
        to_col: int,
    ) -> None:
        delta: float = 0
        norm: float = 0
        for i in range(from_col, to_col):
            for j in range(0, image_0.height):
                pixel0: typing.Tuple[int, int, int] = image_0.getpixel(xy=(i, j))  # type: ignore[assignment]
                pixel1: typing.Tuple[int, int, int] = image_1.getpixel(xy=(i, j))  # type: ignore[assignment]
                d: float = 0
                d += (pixel0[0] - pixel1[0]) ** 2 / 255**2
                d += (pixel0[1] - pixel1[1]) ** 2 / 255**2
                d += (pixel0[2] - pixel1[2]) ** 2 / 255**2
                d /= 3
                delta += d
                norm += 1
        results_per_thread[thread_index] = delta / norm

    @staticmethod
    def __convert_pdf_to_png(pdf: pathlib.Path) -> typing.Tuple[pathlib.Path, int]:
        today: datetime.date = datetime.date.today()
        day: int = today.day
        month: int = today.month
        year: int = today.year
        png: pathlib.Path = pdf.parent / f"{pdf.stem}_{year}_{month}_{day}_tmp.png"
        cmd = [
            "gs",
            "-dSAFER",  # security sandbox
            "-dBATCH",  # exit after processing
            "-dNOPAUSE",  # no pause after each page
            "-sDEVICE=png16m",  # 24-bit RGB PNG
            f"-r{300}",  # resolution
            "-dFirstPage=1",  # first page
            "-dLastPage=1",  # only first page
            f"-sOutputFile={png}",  # output filename
            str(pdf),  # input PDF
        ]
        cmp: CompletedProcess = subprocess.run(cmd, check=True)
        return png, cmp.returncode

    #
    # PUBLIC
    #

    @staticmethod
    def assert_equals(
        pdf_or_image_0: typing.Union[str, pathlib.Path],
        pdf_or_image_1: typing.Union[str, pathlib.Path],
        create_ground_truth_if_missing: bool = True,
    ) -> float:
        """
        Compare two PDFs or images and return their visual difference.

        This method performs a pixel-wise comparison between two inputs,
        which may be either PDF files or image files. If a PDF is
        provided, it is converted to a PNG image of the first page using
        Ghostscript before comparison. Both images are resized to a
        consistent resolution to ensure fair comparison.

        The comparison is computed in parallel across multiple threads,
        each handling a slice of the image columns. The result is a
        floating-point score representing the average normalized difference
        between corresponding pixels in the two images.

        A score of ``0.0`` indicates perfect equality, while higher scores
        indicate greater visual differences.

        :param pdf_or_image_0: The first PDF or image to compare, given as a path or string.
        :param pdf_or_image_1: The second PDF or image to compare, given as a path or string.
        :returns: The average normalized pixel difference as a float.
        """
        # IF pdf_or_image_0 is a str
        # THEN convert to a pathlib.Path
        if isinstance(pdf_or_image_0, str):
            pdf_or_image_0 = pathlib.Path(pdf_or_image_0)
        assert isinstance(pdf_or_image_0, pathlib.Path)

        # useful for creating the ground truth files
        if not pdf_or_image_0.exists() and create_ground_truth_if_missing:
            tmp_file, err_code = VisualAssert.__convert_pdf_to_png(
                pdf=pathlib.Path(pdf_or_image_1)
            )
            if not pdf_or_image_0.parent.exists():
                pdf_or_image_0.parent.mkdir()
            tmp_file.rename(pdf_or_image_0.parent / (pdf_or_image_0.stem + ".png"))

        assert pdf_or_image_0.exists()

        # IF pdf_or_image_1 is a str
        # THEN convert to a pathlib.Path
        if isinstance(pdf_or_image_1, str):
            pdf_or_image_1 = pathlib.Path(pdf_or_image_1)
        assert isinstance(pdf_or_image_1, pathlib.Path)
        assert pdf_or_image_1.exists()

        # IF pdf_or_image_0 is a PDF
        # THEN convert to an image
        delete_pdf_or_image_0: bool = False
        if pdf_or_image_0.suffix == ".pdf":
            pdf_or_image_0, err_code_0 = VisualAssert.__convert_pdf_to_png(
                pdf=pdf_or_image_0
            )
            delete_pdf_or_image_0 = True

        # IF pdf_or_image_1 is a PDF
        # THEN convert to an image
        delete_pdf_or_image_1: bool = False
        if pdf_or_image_1.suffix == ".pdf":
            pdf_or_image_1, err_code_1 = VisualAssert.__convert_pdf_to_png(
                pdf=pdf_or_image_1
            )
            delete_pdf_or_image_1 = True

        # load pdf_or_image_0
        image_0: Image.Image = Image.open(pdf_or_image_0)
        image_0 = image_0.resize(size=(248, 351))

        # load pdf_or_image_1
        image_1: Image.Image = Image.open(pdf_or_image_1)
        image_1 = image_1.resize(size=(248, 351))

        # compare pixels
        number_of_threads: int = os.cpu_count() or 1
        cols_per_thread: int = image_0.width // number_of_threads
        results_per_thread: typing.List[float] = [
            0 for _ in range(0, number_of_threads)
        ]
        threads: typing.List[threading.Thread] = [
            threading.Thread(
                target=VisualAssert.__compare_in_thread,
                args=(
                    cols_per_thread * i,
                    image_0,
                    image_1,
                    results_per_thread,
                    i,
                    (
                        cols_per_thread * (i + 1)
                        if i < number_of_threads - 1
                        else image_0.width
                    ),
                ),
            )
            for i in range(0, number_of_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # delete tmp files
        if delete_pdf_or_image_0 and False:
            try:
                pdf_or_image_0.unlink()
            except:
                pass
        if delete_pdf_or_image_1:
            try:
                pdf_or_image_1.unlink()
            except:
                pass

        # return
        return sum(results_per_thread)
