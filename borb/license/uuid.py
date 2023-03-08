#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A universally unique identifier (UUID) is a 128-bit label used for information in computer systems.
The term globally unique identifier (GUID) is also used.
When generated according to the standard methods, UUIDs are, for practical purposes, unique.
Their uniqueness does not depend on a central registration authority or coordination between the parties generating them,
unlike most other numbering schemes.
While the probability that a UUID will be duplicated is not zero, it is close enough to zero to be negligible.
"""

import random


class UUID:
    """
    A universally unique identifier (UUID) is a 128-bit label used for information in computer systems.
    The term globally unique identifier (GUID) is also used.
    When generated according to the standard methods, UUIDs are, for practical purposes, unique.
    Their uniqueness does not depend on a central registration authority or coordination between the parties generating them,
    unlike most other numbering schemes.
    While the probability that a UUID will be duplicated is not zero, it is close enough to zero to be negligible.
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
    def get() -> str:
        """
        This function returns a randomly generated UUID
        :return:    a randomly generated UUID
        """
        return "".join(
            [
                "".join([random.choice("0123456789abcdef") for _ in range(0, l)]) + "-"
                for l in [8, 4, 4, 4, 12]
            ]
        )[:-1]
