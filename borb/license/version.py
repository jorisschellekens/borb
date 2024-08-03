#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class contains the basics for getting/setting version and license information
within the borb project
"""


class Version:
    """
    This class contains the basics for getting/setting version and license information
    within the borb project
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def get_author() -> str:
        """
        This function returns the author of the borb library
        :return:    the author of the borb library
        """
        return "Joris Schellekens"

    @staticmethod
    def get_producer() -> str:
        """
        This function returns the producer line added to each PDF made by borb
        :return:    the PDF producer
        """
        return "borb"

    @staticmethod
    def get_version() -> str:
        """
        This function returns the current borb version
        :return:    the current borb version
        """
        return "2.1.25"
