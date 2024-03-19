#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class is responsible for getting/setting an anonymous (GDPR-compliant) ID
"""
import sysconfig
import typing
import pathlib

from borb.license.uuid import UUID


class PersistentRandomUserID:
    """
    This class is responsible for getting/setting an anonymous (GDPR-compliant) ID
    """

    USER_ID: typing.Optional[str] = None
    USER_ID_FILE_NAME: str = "anonymous_user_id"

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _get_borb_installation_dir() -> typing.Optional[pathlib.Path]:
        for path_name in sysconfig.get_path_names():
            # check whether the installation path directory exists
            installation_path: pathlib.Path = pathlib.Path(
                sysconfig.get_path(path_name)
            )
            if not installation_path.exists():
                continue
            # check whether the borb directory exists
            borb_dir: pathlib.Path = installation_path / "borb"
            if borb_dir.exists():
                return borb_dir
        return None

    @staticmethod
    def _get_user_id_file_from_borb_dir() -> typing.Optional[pathlib.Path]:
        installation_dir: typing.Optional[
            pathlib.Path
        ] = PersistentRandomUserID._get_borb_installation_dir()
        if installation_dir is None:
            return None
        # check whether the USER_ID_FILE_NAME file exists
        user_id_file: pathlib.Path = (
            installation_dir / PersistentRandomUserID.USER_ID_FILE_NAME
        )
        if user_id_file.exists():
            return user_id_file
        # return
        return None

    #
    # PUBLIC
    #

    @staticmethod
    def get() -> typing.Optional[str]:
        """
        This function (creates and then) returns an anonymous user ID.
        This ID is stored in a file in the borb installation directory to ensure consistency between calls.
        :return:    an anonymous user ID
        """
        # IF borb installation directory exists, but the file does not exist (yet)
        # THEN create the file, return the uuid
        installation_dir: typing.Optional[
            pathlib.Path
        ] = PersistentRandomUserID._get_borb_installation_dir()
        user_id_file: typing.Optional[
            pathlib.Path
        ] = PersistentRandomUserID._get_user_id_file_from_borb_dir()
        if (
            installation_dir is not None
            and installation_dir.exists()
            and (user_id_file is None or not user_id_file.exists())
        ):
            try:
                # fmt: off
                new_uuid: str = UUID.get()
                with open(installation_dir / PersistentRandomUserID.USER_ID_FILE_NAME, "w") as fh:
                    fh.write(new_uuid)
                return new_uuid
                # fmt: on
            except:
                pass

        # IF the borb installation directory exists, and the user_id file exists
        # THEN read the user_id file, and return its content
        if user_id_file is not None and user_id_file.exists():
            prev_uuid: typing.Optional[str] = None
            try:
                with open(user_id_file, "r") as fh:
                    prev_uuid = fh.read()
            except:
                pass
            return prev_uuid

        # default
        return None
