#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This factory implementation provides access to the unsplash API for retrieving images.
This class expects `keyring.get_password("unsplash", "access_key")` to have been set.
"""

import json
import typing
from decimal import Decimal

import keyring as keyring
import urllib.request

from borb.pdf.canvas.layout.image.image import Image


class Unsplash:
    """
    This factory implementation provides access to the unsplash API for retrieving images.
    This class expects `keyring.get_password("unsplash", "access_key")` to have been set.
    """

    @staticmethod
    def get_image(
        keywords: typing.List[str],
        width: typing.Optional[Decimal],
        height: typing.Optional[Decimal],
    ) -> Image:
        """
        This function returns the best-matching Image (in terms of its dimensions) for a given list of keywords
        :param keywords:    the keywords to be searched
        :param width:       the desired width
        :param height:      the desired height
        :return:            an Image
        """
        R: typing.Optional[Decimal] = None
        if width is not None and height is not None:
            R = width / height

        # build keyword str
        keyword_str: str = "".join([(k + "+") for k in keywords])[:-1]

        # get access_key
        unsplash_access_key: typing.Optional[str] = keyring.get_password(
            "unsplash", "access_key"
        )
        assert (
            unsplash_access_key is not None
        ), "An access key must be specified to use the unsplash API."

        # fetch json
        min_delta: typing.Optional[Decimal] = None
        min_image: typing.Optional[typing.Any] = None
        url: str = (
            "https://api.unsplash.com/search/photos?page=1&query=%s&client_id=%s"
            % (keyword_str, unsplash_access_key)
        )
        with urllib.request.urlopen(url) as response:
            for result in json.loads(response.read().decode())["results"]:
                if "width" not in result:
                    continue
                if "height" not in result:
                    continue
                if "urls" not in result:
                    continue
                if "regular" not in result["urls"]:
                    continue
                w: Decimal = Decimal(result["width"])
                h: Decimal = Decimal(result["height"])
                r: Decimal = w / h

                delta: Decimal = round(abs(r - R), 3)
                if min_delta is None or delta < min_delta:
                    min_image = result

        # return
        return Image(min_image["urls"]["regular"], width=width, height=height)
