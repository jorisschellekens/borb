#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class is responsible for getting/setting an anonymous (GDPR-compliant) ID
"""
import sysconfig
import typing
from pathlib import Path

from borb.license.uuid import UUID


class AnonymousUserID:
    """
    This class is responsible for getting/setting an anonymous (GDPR-compliant) ID
    """

    USER_ID_FILE_NAME: str = "anonymous_user_id"
    USER_ID: typing.Optional[str] = None

    @staticmethod
    def _get_borb_installation_dir() -> typing.Optional[Path]:
        for path_name in sysconfig.get_path_names():
            # check whether the installation path directory exists
            installation_path: Path = Path(sysconfig.get_path(path_name))
            if not installation_path.exists():
                continue
            # check whether the borb directory exists
            borb_dir: Path = installation_path / "borb"
            if borb_dir.exists():
                return borb_dir
        return None

    @staticmethod
    def _get_user_id_file_from_borb_dir() -> typing.Optional[Path]:
        borb_dir: typing.Optional[Path] = AnonymousUserID._get_borb_installation_dir()
        if borb_dir is None:
            return None
        # check whether the USER_ID_FILE_NAME file exists
        user_id_file: Path = borb_dir / AnonymousUserID.USER_ID_FILE_NAME
        if user_id_file.exists():
            return user_id_file
        # return
        return None

    @staticmethod
    def disable() -> None:
        """
        This method disables the anonymous user ID.
        This clears the hidden file in the borb installation directory.
        When this file is empty, an empty user ID is passed in the get function
        :return:    None
        """
        if (
            AnonymousUserID._get_borb_installation_dir() is not None
            and AnonymousUserID._get_borb_installation_dir().exists()
        ):
            try:
                # fmt: off
                with open(AnonymousUserID._get_borb_installation_dir() / AnonymousUserID.USER_ID_FILE_NAME, "w") as fh:
                    fh.write("")
                # fmt: on
            except:
                pass

    @staticmethod
    def enable() -> None:
        """
        This method enables the anonymous user ID.
        This resets the hidden file in the borb installation directory.
        When this file is reset, a new user ID is created and passed in the get function
        :return:    None
        """
        if (
            AnonymousUserID._get_user_id_file_from_borb_dir() is not None
            and AnonymousUserID._get_user_id_file_from_borb_dir().exists()
        ):
            try:
                AnonymousUserID._get_user_id_file_from_borb_dir().unlink()
            except:
                pass
        AnonymousUserID.get()

    @staticmethod
    def get() -> typing.Optional[str]:
        """
        This function (creates and then) returns an anonymous user ID.
        This ID is stored in a file in the borb installation directory to ensure consistency between calls.
        :return:    an anonymous user ID
        """
        # IF borb installation directory exists, but the file does not exist (yet)
        # THEN create the file, return the uuid
        if (
            AnonymousUserID._get_borb_installation_dir() is not None
            and AnonymousUserID._get_borb_installation_dir().exists()
            and (
                AnonymousUserID._get_user_id_file_from_borb_dir() is None
                or not AnonymousUserID._get_user_id_file_from_borb_dir().exists()
            )
        ):
            try:
                # fmt: off
                uuid: str = UUID.get()
                with open(AnonymousUserID._get_borb_installation_dir() / AnonymousUserID.USER_ID_FILE_NAME, "w") as fh:
                    fh.write(uuid)
                return uuid
                # fmt: on
            except:
                pass

        # IF the borb installation directory exists, and the user_id file exists
        # THEN read the user_id file, and return its content
        if (
            AnonymousUserID._get_user_id_file_from_borb_dir() is not None
            and AnonymousUserID._get_user_id_file_from_borb_dir().exists()
        ):
            uuid: typing.Optional[str] = None
            try:
                with open(AnonymousUserID._get_user_id_file_from_borb_dir(), "r") as fh:
                    uuid = fh.read()
            except:
                pass
            return uuid

        # default
        return None
