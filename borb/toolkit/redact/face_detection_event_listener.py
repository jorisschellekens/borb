#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for analyzing a PDF document to detect faces.
This event listener processes the pages of the PDF, utilizing face detection algorithms,
and triggers events or provides information based on the identified faces.
"""

import typing
from decimal import Decimal
import pathlib

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent

from borb.pdf.canvas.event.event_listener import EventListener, Event
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle


class FaceDetectionEventListener(EventListener):
    """
    A class for analyzing a PDF document to detect faces.
    This event listener processes the pages of the PDF, utilizing face detection algorithms,
    and triggers events or provides information based on the identified faces.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._current_page: int = -1
        self._face_information_per_page: typing.Dict[int, typing.List[Rectangle]] = {}
        resources_dir: pathlib.Path = pathlib.Path(__file__).parent / "resources"
        self._haar_cascade_detector_files: typing.List[pathlib.Path] = [
            resources_dir / "haar_cascade_frontal_face_default.xml",
            resources_dir / "haar_cascade_profile_face_default.xml",
        ]
        assert all([x.exists() for x in self._haar_cascade_detector_files])
        import cv2  # type: ignore[import]

        self._haar_cascade_face_detectors: typing.List[cv2.CascadeClassifier] = [
            cv2.CascadeClassifier(str(x.absolute()))
            for x in self._haar_cascade_detector_files
        ]

    #
    # PRIVATE
    #

    def _detect_faces(self, event: ImageRenderEvent) -> None:

        # convert to grayscale
        import cv2  # type: ignore[import]
        import numpy as np  # type: ignore[import]

        grayscale_image = cv2.cvtColor(
            np.asarray(event.get_image()), cv2.COLOR_BGR2GRAY
        )

        # determine y_top of event
        event_y_top: Decimal = event.get_y() + event.get_height()

        # find faces
        faces: typing.List[typing.List[int]] = []
        for detector in self._haar_cascade_face_detectors:
            faces += [
                list(f)
                for f in detector.detectMultiScale(
                    grayscale_image,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE,
                )
            ]

        # determine scale
        hscale: Decimal = event.get_width() / event.get_image().width
        vscale: Decimal = event.get_height() / event.get_image().height

        # determine faces
        for face in faces:
            x: int = int(face[0] * hscale)
            w: int = int(face[2] * hscale)
            h: int = int(face[3] * vscale)

            # the image library places the (0, 0) coordinate at the top left corner
            # PDF places the (0, 0) coordinate at the bottom left corner
            # we start by calculating the top_y coordinate (scaling the y-coordinate)
            top_y: int = int(face[1] * vscale)

            # we now calculate the bottom_y coordinate of the face
            # simply by taking top_y and adding the height
            bottom_y: int = top_y + h

            # now we need to express how far this coordinate is from the
            # bottom of the image (for which we need the image height)
            y: int = int(event.get_height() - bottom_y)

            # we need to add the x/y of the image itself
            # to ensure we get the location ON THE PAGE (rather than IN THE IMAGE)
            x_on_page = Decimal(x + event.get_x())
            y_on_page = Decimal(y + event.get_y())

            # trigger _face_occurred
            self._face_occurred(
                event,
                Rectangle(Decimal(x), Decimal(y), Decimal(w), Decimal(h)),
                Rectangle(
                    Decimal(x_on_page), Decimal(y_on_page), Decimal(w), Decimal(h)
                ),
            )

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._current_page += 1
        if isinstance(event, ImageRenderEvent):
            self._detect_faces(event)

    def _face_occurred(
        self,
        event: ImageRenderEvent,
        rectangle_in_image: Rectangle,
        rectangle_on_page: Rectangle,
    ) -> None:
        # init dictionary entry if needed
        if self._current_page not in self._face_information_per_page:
            self._face_information_per_page[self._current_page] = []
        # update dictionary
        self._face_information_per_page[self._current_page].append(rectangle_on_page)

    #
    # PUBLIC
    #

    def get_faces(self) -> typing.Dict[int, typing.List[Rectangle]]:
        """
        This function returns a typing.List[Rectangle] on a given page,
        representing the coordinates of the face(s) in the Image(s)
        """
        return self._face_information_per_page
