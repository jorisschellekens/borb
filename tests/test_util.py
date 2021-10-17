import os
from pathlib import Path

from PIL import Image as PILImage


def compare_visually_to_ground_truth(
    pdf_path: Path, maximum_normalized_difference: float = 0.004
):

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
    progress_int: int = 0
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
