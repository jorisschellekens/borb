#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class to represent and compare software version numbers using semantic versioning.

Version numbers are expected in the format `major.minor.patch` (e.g., "1.2.3").
"""


class Version:
    """
    A class to represent and compare software version numbers using semantic versioning.

    Version numbers are expected in the format `major.minor.patch` (e.g., "1.2.3").
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, s: str):
        """
        Initialize a `Version` instance by parsing a version string.

        :param s: str - The version string in the format `major.minor.patch`.
        """
        self.__major: int = int(s.split(".")[0])
        self.__minor: int = int(s.split(".")[1])
        self.__patch: int = int(s.split(".")[2])

    #
    # PRIVATE
    #

    def __eq__(self, other):
        """
        Check if this version is equal to another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if both versions are equal, False otherwise.
        """
        if not isinstance(other, Version):
            return False
        return (
            (other.__major == self.__major)
            and (other.__minor == self.__minor)
            and (other.__patch == self.__patch)
        )

    def __ge__(self, other):
        """
        Determine if this version is greater than or equal to another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if this version is greater than or equal to the other, False otherwise.
        """
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other):
        """
        Determine if this version is greater than another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if this version is greater than the other, False otherwise.
        :raises AssertionError: If the `other` is not a `Version` instance.
        """
        assert isinstance(other, Version)
        return (
            (self.__major > other.__major)
            or (self.__major == other.__major and self.__minor > other.__minor)
            or (
                self.__major == other.__major
                and self.__minor == other.__minor
                and self.__patch > other.__patch
            )
        )

    def __le__(self, other):
        """
        Determine if this version is less than or equal to another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if this version is less than or equal to the other, False otherwise.
        """
        return self.__lt__(other) or self.__eq__(other)

    def __lt__(self, other):
        """
        Determine if this version is less than another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if this version is less than the other, False otherwise.
        :raises AssertionError: If the `other` is not a `Version` instance.
        """
        assert isinstance(other, Version)
        return (
            (self.__major < other.__major)
            or (self.__major == other.__major and self.__minor < other.__minor)
            or (
                self.__major == other.__major
                and self.__minor == other.__minor
                and self.__patch < other.__patch
            )
        )

    def __ne__(self, other):
        """
        Check if this version is not equal to another version.

        :param other: Version - The other `Version` object to compare against.
        :return: bool - True if both versions are not equal, False otherwise.
        """
        if not isinstance(other, Version):
            return True
        return (
            (other.__major != self.__major)
            or (other.__minor != self.__minor)
            or (other.__patch != self.__patch)
        )

    def __repr__(self):
        """
        Return a string representation of the version.

        :return: str - The version string in the format `major.minor.patch`.
        """
        return f"{self.__major}.{self.__minor}.{self.__patch}"

    #
    # PUBLIC
    #

    @staticmethod
    def get_current_version() -> "Version":
        """
        Retrieve the current version of the application.

        :return: Version - A `Version` object representing the current version.
        """
        # Python 3.8+
        try:
            from importlib.metadata import (
                version as get_installed_version,
                PackageNotFoundError,
            )

            return Version(get_installed_version("borb"))
        except:
            pass

        # Python <3.8 (backport)
        try:
            from importlib_metadata import (  # type: ignore[import-not-found, no-redef]
                version as get_installed_version,
                PackageNotFoundError,
            )

            return Version(get_installed_version("borb"))
        except:
            pass

        # default
        return Version("3.0.2")
