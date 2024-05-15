#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Subclass of FaceDetectionEventListener that focuses on blurring detected faces in a PDF document.
When a face is identified, this class applies a blur effect to protect privacy or anonymize individuals within the document.
"""
from decimal import Decimal

from PIL import Image as PILImageModule
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.toolkit import FaceDetectionEventListener


class FaceEraserEventListener(FaceDetectionEventListener):
    """
    Subclass of FaceDetectionEventListener that focuses on blurring detected faces in a PDF document.
    When a face is identified, this class applies a blur effect to protect privacy or anonymize individuals within the document.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _face_occurred(
        self,
        event: ImageRenderEvent,
        rectangle_in_image: Rectangle,
        rectangle_on_page: Rectangle,
    ) -> None:
        super(FaceEraserEventListener, self)._face_occurred(
            event=event,
            rectangle_in_image=rectangle_in_image,
            rectangle_on_page=rectangle_on_page,
        )

        # grab the original image
        img: PILImageModule.Image = event.get_image()

        # determine the coordinates to modify
        x: int = int(rectangle_in_image.get_x())
        y: int = int(
            event.get_height()
            - rectangle_in_image.get_y()
            - rectangle_in_image.get_height()
        )
        w: int = int(rectangle_in_image.get_width())
        h: int = int(rectangle_in_image.get_height())

        # determine scale
        hscale: Decimal = event.get_width() / event.get_image().width
        vscale: Decimal = event.get_height() / event.get_image().height

        # apply scale
        x = int(x / hscale)
        y = int(y / vscale)
        w = int(w / hscale)
        h = int(h / vscale)

        # exception
        if w == 0 or h == 0:
            return

        # replace the pixels in the face
        block_size: int = w // 10
        for i in range(x, x + w, block_size):
            for j in range(y, y + h, block_size):

                # determine average color of a (large) block
                avg_r: int = 0
                avg_g: int = 0
                avg_b: int = 0
                for i2 in range(0, block_size):
                    for j2 in range(0, block_size):
                        if i + i2 >= img.width or j + j2 >= img.height:
                            continue
                        avg_r += img.getpixel((i + i2, j + j2))[0]
                        avg_g += img.getpixel((i + i2, j + j2))[1]
                        avg_b += img.getpixel((i + i2, j + j2))[2]
                avg_r //= block_size * block_size
                avg_g //= block_size * block_size
                avg_b //= block_size * block_size

                # replace pixel in the (large) block
                # with the average color
                for i2 in range(0, block_size):
                    for j2 in range(0, block_size):
                        if i + i2 >= img.width or j + j2 >= img.height:
                            continue
                        img.putpixel((i + i2, j + j2), (avg_r, avg_g, avg_b))

    #
    # PUBLIC
    #
